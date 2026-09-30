"""
Build the IELTS speaking question bank from a season PDF.

Parses the 雅思哥-style season PDF (native text layer) and writes:
  references/question_bank_complete.json   machine-readable, ALL topics
  references/question-bank.md              human-readable, ALL topics

Usage:
  python build_complete_bank.py --pdf "<season>.pdf" --season "2026年9-12月" \
      --season-code 2026-09-12 --cutoff 2026-09-24 \
      [--previous-json old.json] [--previous-md old.md] [--dry-run]

  --previous-*   previous season's bank; carried-over topics get a
                 `carried_over_from` key so progress can be migrated
                 (see migrate_season.py).
  --text FILE    use pre-extracted text instead of opening the PDF.

Extraction: PyMuPDF (fitz) first; pdfplumber, when installed, is used as an
independent cross-check of the question count. Scanned PDFs without a text
layer are rejected with a clear message (use an OCR tool such as MinerU first
and pass its text output with --text).

Only the Python standard library is required besides one PDF library.
"""
import argparse
import difflib
import json
import re
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # ielts-coach/
REFS = BASE / "references"

# Section keys in output order: (json key, part, id prefix, human label)
SECTIONS = [
    ("part1_new", "part1", "new", "Part 1 New Topics (大陆新题)"),
    ("part23_new", "part23", "new", "Part 2&3 New Topics (大陆新题)"),
    ("part1_retained", "part1", "retained", "Part 1 Retained Topics (保留题)"),
    ("part1_essential", "part1", "essential", "Part 1 Essential Topics (万年老题)"),
    ("part23_retained", "part23", "retained", "Part 2&3 Retained Topics (保留题)"),
    ("part1_nonmainland", "part1", "nonmainland", "Part 1 Non-mainland New Topics (非大陆新题)"),
    ("part23_nonmainland", "part23", "nonmainland", "Part 2&3 Non-mainland New Topics (非大陆新题)"),
]
MAINLAND_KEYS = ["part1_new", "part23_new", "part1_retained", "part1_essential", "part23_retained"]

# Chinese glosses for Part 1 topics (the PDF lists Part 1 in English only).
# Missing entries fall back to the previous season, then to "" with a warning.
P1_CN = {
    "travelling": "旅行", "rubbish and recycling": "垃圾与回收", "tiredness": "疲惫",
    "shoes": "鞋子", "politeness": "礼貌", "fruit and vegetables": "水果和蔬菜",
    "advertisement": "广告", "paper": "纸", "secondary school": "中学", "name": "名字",
    "opportunities": "机会", "lost and found": "失物招领", "computers/tablets": "电脑/平板",
    "collecting things": "收藏物品", "street market": "街边市场", "feeling bored": "感到无聊",
    "friends": "朋友", "music": "音乐", "teachers": "老师", "social media": "社交媒体",
    "tidiness": "整洁", "websites": "网站", "watch": "手表", "shopping": "购物",
    "cars": "汽车", "public gardens and parks": "公园和花园", "science": "科学",
    "mirrors": "镜子", "outer space and stars": "外太空和星星", "singing": "唱歌",
    "clothing": "服装", "jokes & comedies": "笑话和喜剧", "headphones": "耳机",
    "morning time": "早晨", "work or studies": "工作或学习", "home/accommodation": "住所",
    "hometown": "家乡", "the area you live in": "居住区域", "the city you live in": "居住的城市",
}

SMALL_WORDS = {"a", "an", "the", "and", "or", "but", "nor", "of", "in", "on", "at",
               "to", "for", "by", "with", "from", "as", "into", "than", "that"}


# --------------------------------------------------------------------------- #
# Extraction
# --------------------------------------------------------------------------- #
def extract_pages(pdf_path):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        fitz = None
    if fitz is not None:
        with fitz.open(pdf_path) as doc:
            return [p.get_text() for p in doc]
    try:
        import pdfplumber
    except ImportError:
        sys.exit("No PDF library found. Install one: pip install pymupdf")
    with pdfplumber.open(pdf_path) as pdf:
        return [(p.extract_text() or "") for p in pdf.pages]


def count_question_lines(pages):
    return sum(1 for t in pages for l in t.splitlines() if l.strip().endswith(("?", "？")))


def cross_check(pdf_path, primary_pages):
    """Independent second parser; returns a message, never aborts."""
    try:
        import pdfplumber
    except ImportError:
        return "cross-check skipped (pdfplumber not installed)"
    with pdfplumber.open(pdf_path) as pdf:
        other = [(p.extract_text() or "") for p in pdf.pages]
    a, b = count_question_lines(primary_pages), count_question_lines(other)
    status = "OK" if a == b else "MISMATCH - inspect the PDF manually"
    return f"cross-check question lines: primary={a} pdfplumber={b} {status}"


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #
def norm(s):
    s = s.replace("：", ":").replace("？", "?").replace("’", "'").replace("‘", "'")
    s = s.replace("（", "(").replace("）", ")").replace("\u3000", " ")
    return re.sub(r"\s+", " ", s).strip()


def clean_lines(pages):
    """Body lines from the first content page, page numbers dropped."""
    lines = []
    started = False
    for text in pages:
        for raw in text.splitlines():
            line = norm(raw)
            if not line or re.fullmatch(r"\d{1,3}", line):
                continue
            if not started:
                # the TOC repeats the headings with dotted leaders; skip until
                # the real section heading (no leader dots) appears
                if not re.match(r"^一、\s*大陆地区新题$", line):
                    continue
                started = True
            lines.append(line)
    return lines


RE_REGION = re.compile(r"^(一|二|三)、\s*(.+)$")
RE_GROUP = re.compile(r"^Part\s*(1|2&3)\s+(.+?)\((\d+)\s*道\)$")
RE_P1 = re.compile(r"^(\d+)\s*P1\s+(.+)$")
RE_P2 = re.compile(r"^(\d+)\s*P2\s+(.+)$")
RE_ESS = re.compile(r"^万年老题\s+(.+)$")
SENT_END = ("?", ".", "!", ")", "。")


def join_wrapped(items):
    """Merge PDF line-wraps: a line that does not end a sentence continues."""
    out, buf = [], ""
    for it in items:
        buf = f"{buf} {it}".strip() if buf else it
        if buf.endswith(SENT_END):
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return out


def section_key(region, part, group):
    if region == "三":
        return "part1_nonmainland" if part == "1" else "part23_nonmainland"
    if "万年" in group:
        return "part1_essential"
    if "保留" in group:
        return "part1_retained" if part == "1" else "part23_retained"
    return "part1_new" if part == "1" else "part23_new"


def parse_p2_body(body):
    """body: lines after the P2 header -> cue_card, cue_points, part3."""
    try:
        i_say = next(i for i, l in enumerate(body) if l.lower().startswith("you should say"))
        i_p3 = next(i for i, l in enumerate(body) if l == "P3")
    except StopIteration:
        raise ValueError(f"malformed cue card: {body[:3]}")
    cue_card = " ".join(body[:i_say])
    points = []
    for l in body[i_say + 1:i_p3]:
        if points and l[:1].islower():
            points[-1] += " " + l  # wrapped cue point
        else:
            points.append(l)
    return cue_card, points, join_wrapped(body[i_p3 + 1:])


def parse_bank(lines):
    bank = {k: [] for k, *_ in SECTIONS}
    declared = {}
    region = part = group = None
    current = None  # (key, header, body_lines)

    def flush():
        if not current:
            return
        key, header, body = current
        sec = next(s for s in SECTIONS if s[0] == key)
        num = len(bank[key]) + 1
        topic = {"id": num, "topic_id": f"{sec[2]}-{num}"}
        if sec[1] == "part1":
            topic.update(name_en=header, name_cn="", questions=join_wrapped(body))
        else:
            cue, pts, p3 = parse_p2_body(body)
            topic.update(name_cn=header, name_en="", cue_card=cue, cue_points=pts, part3=p3)
        bank[key].append(topic)

    for line in lines:
        m = RE_REGION.match(line)
        if m:
            flush(); current = None
            region = m.group(1)
            continue
        m = RE_GROUP.match(line)
        if m:
            flush(); current = None
            part, group = m.group(1), m.group(2)
            key = section_key(region, part, group)
            declared[key] = int(m.group(3))
            continue
        m = RE_P1.match(line) or RE_P2.match(line) or RE_ESS.match(line)
        if m and region:
            flush()
            key = section_key(region, part, group)
            current = (key, m.groups()[-1].strip(), [])
            continue
        if current:
            current[2].append(line)
    flush()
    return bank, declared


# --------------------------------------------------------------------------- #
# Previous season (carry-over mapping)
# --------------------------------------------------------------------------- #
def key_text(s):
    s = re.sub(r"\(.*?\)", " ", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def load_previous_md(path):
    """Parse question-bank.md (this builder's format or the legacy one)."""
    out = []
    key = None
    cur = None
    text = Path(path).read_text(encoding="utf-8")
    for line in text.splitlines():
        h2 = re.match(r"^## (Part 1|Part 2&3) (.+)$", line)
        if h2:
            label = h2.group(2).lower()
            p = "part1" if h2.group(1) == "Part 1" else "part23"
            kind = ("essential" if "essential" in label else "retained" if "retained" in label
                    else "nonmainland" if "non-mainland" in label else "new")
            key = (p, kind)
            continue
        h3 = re.match(r"^### (?:(\d+)\. )?(.+)$", line)
        if h3 and key:
            p, kind = key
            idx = len([t for t in out if (t["part"], t["kind"]) == key]) + 1
            title = h3.group(2)
            m = re.match(r"^(.*?) \((.+)\)$", title)
            a, b = (m.group(1), m.group(2)) if m else (title, "")
            name_en, name_cn = (a, b) if p == "part1" else (b, a)
            cur = {"part": p, "kind": kind, "topic_id": f"{kind}-{idx}",
                   "name_en": name_en, "name_cn": name_cn, "cue_card": ""}
            out.append(cur)
            continue
        if cur and line.startswith("**Cue Card:**"):
            cur["cue_card"] = line.split("**Cue Card:**", 1)[1].strip()
    return out


def load_previous_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for key, p, kind, _ in SECTIONS:
        for t in data.get(key, []):
            out.append({"part": p, "kind": kind,
                        "topic_id": t.get("topic_id") or f"{kind}-{t['id']}",
                        "name_en": t.get("name_en", ""), "name_cn": t.get("name_cn", ""),
                        "cue_card": t.get("cue_card", "")})
    return data.get("metadata", {}), out


def map_previous(bank, previous, prev_code):
    """Attach carried_over_from + reuse previous names for continuity."""
    carried = 0
    for key, p, *_ in SECTIONS:
        pool = [t for t in previous if t["part"] == p]
        for t in bank[key]:
            t["carried_over_from"] = None
            probe = key_text(t["name_en"] if p == "part1" else t["cue_card"])
            best, score = None, 0.0
            for old in pool:
                cand = key_text(old["name_en"] if p == "part1" else old["cue_card"])
                if not cand:
                    continue
                r = 1.0 if cand == probe else difflib.SequenceMatcher(None, probe, cand).ratio()
                if r > score:
                    best, score = old, r
            if best and score >= (0.95 if p == "part1" else 0.88):
                t["carried_over_from"] = f"{prev_code}:{p}:{best['topic_id']}"
                carried += 1
                if p == "part1" and not t["name_cn"]:
                    t["name_cn"] = best["name_cn"]
                if p == "part23" and not t["name_en"]:
                    t["name_en"] = best["name_en"]
    return carried


# --------------------------------------------------------------------------- #
# Enrichment, validation, rendering
# --------------------------------------------------------------------------- #
def title_case(s):
    words = s.split()
    return " ".join(w if (i and w.lower() in SMALL_WORDS) else w[:1].upper() + w[1:]
                    for i, w in enumerate(words))


def derive_name_en(cue_card):
    s = re.sub(r"\(.*?\)", "", cue_card)
    s = re.sub(r"^Describe\s+", "", s, flags=re.I).strip(" .")
    return title_case(re.sub(r"\s+", " ", s))


def enrich(bank):
    missing = []
    for key, p, *_ in SECTIONS:
        for t in bank[key]:
            if p == "part1" and not t["name_cn"]:
                t["name_cn"] = P1_CN.get(t["name_en"].lower(), "")
                if not t["name_cn"]:
                    missing.append(t["name_en"])
            if p == "part23" and not t["name_en"]:
                t["name_en"] = derive_name_en(t["cue_card"])
    return missing


def validate(bank, declared):
    errors = []
    for key, p, *_ in SECTIONS:
        got = len(bank[key])
        if key in declared and declared[key] != got:
            errors.append(f"{key}: PDF declares {declared[key]}, parsed {got}")
        for t in bank[key]:
            tag = f"{key}#{t['id']}"
            if p == "part1" and len(t["questions"]) < 3:
                errors.append(f"{tag} has only {len(t['questions'])} questions")
            if p == "part23":
                if not t["cue_card"].lower().startswith("describe"):
                    errors.append(f"{tag} cue card does not start with Describe")
                if len(t["cue_points"]) < 3 or len(t["part3"]) < 3:
                    errors.append(f"{tag} cue points/Part 3 look truncated")
    return errors


def totals(bank):
    t = {k: len(bank[k]) for k, *_ in SECTIONS}
    t["mainland"] = sum(t[k] for k in MAINLAND_KEYS)
    t["total"] = sum(len(bank[k]) for k, *_ in SECTIONS)
    return t


def render_md(bank, meta):
    tt = meta["total_topics"]
    L = [f"# IELTS Speaking Question Bank ({meta['season']})", "",
         f"Source: `{meta['source_file']}` (cut-off {meta['cutoff']}). "
         f"Generated by `scripts/build_complete_bank.py` - do not edit by hand; "
         f"`question_bank_complete.json` holds the same data for scheduling.", "",
         "## Structure Overview", ""]
    for key, _, _, label in SECTIONS:
        L.append(f"- **{label}**: {tt[key]}")
    L += [f"- **Total: {tt['total']} topics** (mainland candidates: {tt['mainland']}; "
          f"non-mainland candidates: {tt['total']})", "",
          "> Mainland candidates skip the two non-mainland sections. "
          "Topics marked ♻️ were carried over from the previous season.", ""]
    for key, p, _, label in SECTIONS:
        L += [f"## {label} ({tt[key]})", ""]
        for t in bank[key]:
            mark = " ♻️" if t.get("carried_over_from") else ""
            if p == "part1":
                head = f"{t['name_en']} ({t['name_cn']})" if t["name_cn"] else t["name_en"]
                L.append(f"### {t['id']}. {head}{mark}")
                L += [f"- {q}" for q in t["questions"]]
            else:
                L.append(f"### {t['id']}. {t['name_cn']} ({t['name_en']}){mark}")
                L.append(f"**Cue Card:** {t['cue_card']}")
                L.append("You should say: " + " | ".join(t["cue_points"]))
                L += ["", "**Part 3:**"] + [f"- {q}" for q in t["part3"]]
            L.append("")
    return "\n".join(L).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--text", help="pre-extracted text file (one page per '\\f')")
    ap.add_argument("--season", required=True, help='e.g. "2026年9-12月"')
    ap.add_argument("--season-code", required=True, help="e.g. 2026-09-12")
    ap.add_argument("--cutoff", default=date.today().isoformat(), help="bank cut-off date")
    ap.add_argument("--previous-json")
    ap.add_argument("--previous-md")
    ap.add_argument("--out-dir", default=str(REFS))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    if a.text:
        pages = Path(a.text).read_text(encoding="utf-8").split("\f")
        check = "cross-check skipped (--text input)"
    else:
        pages = extract_pages(a.pdf)
        if sum(len(p.strip()) for p in pages) < 500:
            sys.exit("PDF has no usable text layer (scanned?). Run OCR (e.g. MinerU) "
                     "and pass the text with --text.")
        check = cross_check(a.pdf, pages)
    print(check)

    bank, declared = parse_bank(clean_lines(pages))

    prev_code, previous = None, []
    if a.previous_json:
        pmeta, pj = load_previous_json(a.previous_json)
        prev_code = pmeta.get("season_code")
        if not prev_code:  # legacy bank: derive "2026-05-08" from "2026年5-8月"
            m = re.search(r"(\d{4})年(\d{1,2})-(\d{1,2})月", pmeta.get("season", ""))
            prev_code = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" if m else "previous"
        previous += pj
    if a.previous_md:
        seen = {(t["part"], t["topic_id"]) for t in previous}
        previous += [t for t in load_previous_md(a.previous_md) if (t["part"], t["topic_id"]) not in seen]
        prev_code = prev_code or "previous"
    carried = map_previous(bank, previous, prev_code) if previous else 0
    if not previous:
        for k, *_ in SECTIONS:
            for t in bank[k]:
                t["carried_over_from"] = None

    missing_cn = enrich(bank)
    errors = validate(bank, declared)

    meta = {
        "season": a.season,
        "season_code": a.season_code,
        "cutoff": a.cutoff,
        "source_file": Path(a.pdf).name,
        "source": "IELTS speaking season PDF, parsed by scripts/build_complete_bank.py",
        "extracted_with": "PyMuPDF (+ pdfplumber cross-check)",
        "previous_season": prev_code,
        "carried_over_topics": carried,
        "last_updated": date.today().isoformat(),
        "total_topics": totals(bank),
    }
    out = {"metadata": meta, **{k: bank[k] for k, *_ in SECTIONS}}

    for key, *_ in SECTIONS:
        print(f"  {key:<20} {len(bank[key]):>3}  (declared {declared.get(key, '-')})")
    print(f"  total {meta['total_topics']['total']} | mainland {meta['total_topics']['mainland']} "
          f"| carried over {carried}")
    if missing_cn:
        print("WARNING: add Chinese names to P1_CN for: " + ", ".join(missing_cn))
    if errors:
        print("VALIDATION FAILED:\n  " + "\n  ".join(errors))
        return 1
    if a.dry_run:
        print("dry run: nothing written")
        return 0
    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    (od / "question_bank_complete.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (od / "question-bank.md").write_text(render_md(bank, meta), encoding="utf-8")
    print(f"wrote {od / 'question_bank_complete.json'} and {od / 'question-bank.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
