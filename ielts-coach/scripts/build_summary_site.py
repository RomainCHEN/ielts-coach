"""
One-click prep summary website for the end of a study cycle.

Reads the learner's state (user_profile.json, progress.json, study_plan.json),
the answer page (ielts_answers.html) and the current question bank, then
writes a self-contained static site:

  summary_site/
    index.html             hub: countdown, targets, stats, links
    speaking_sprint.html   answer rhythm + logic chains + YOUR material cards
    task2_templates.html   Task 2 templates (generic)
    task1_templates.html   Task 1 templates (generic)
    review.html            progress review, bank coverage gaps, expression bank
    ielts_answers.html     copy of every model answer
    task1_charts/          copied when the answers page references charts

  python build_summary_site.py [--root .] [--out summary_site]
                               [--content summary_content.json] [--lang zh|en]

`summary_content.json` (optional, written by the agent) supplies what a program
cannot judge: personal material cards and the final tip. Shape:
  {"materials": [{"title": "...", "tags": ["..."], "items": ["..."]}],
   "tip": "...", "title": "..."}
Without it, material cards are derived from the profile and the Part 2 topics
already practised.

The site contains personal data. It is written locally only; publishing it is
a separate, explicit decision by the learner.
"""
import argparse
import html
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets" / "summary_site"
BANK = SKILL / "references" / "question_bank_complete.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_season import build_maps, SECTION_KEYS  # noqa: E402

E = html.escape
SECTION_LABEL = {
    "part1_new": "Part 1 新题", "part23_new": "Part 2&3 新题",
    "part1_retained": "Part 1 保留题", "part1_essential": "Part 1 万年老题",
    "part23_retained": "Part 2&3 保留题", "part1_nonmainland": "Part 1 非大陆新题",
    "part23_nonmainland": "Part 2&3 非大陆新题",
}
PART_LABEL = {"p1": "Part 1", "p2": "Part 2", "p3": "Part 3", "wt1": "Task 1", "wt2": "Task 2"}


# --------------------------------------------------------------------------- #
# Inputs
# --------------------------------------------------------------------------- #
def load_json(path, warnings):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        warnings.append(f"{path.name} is malformed (line {e.lineno}); ignored")
        return None


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse_answers(path):
    """Extract answer cards: part, title, expressions, word count."""
    if not path.exists():
        return []
    s = path.read_text(encoding="utf-8")
    cards = []
    for chunk in s.split('<article class="answer-card"')[1:]:
        chunk = chunk.split("</article>", 1)[0]
        m = re.search(r'class="topic-type (\w+)">[^<]*</span>\s*([^<]+)', chunk)
        if not m:
            continue
        exps = [(strip_tags(a), strip_tags(b)) for a, b in re.findall(
            r'<span class="exp">(.*?)</span>\s*<span class="meaning">(.*?)</span>', chunk, re.S)]
        wc = re.search(r"(\d{2,4})\s*words", chunk)
        cards.append({"part": m.group(1), "title": strip_tags(m.group(2)),
                      "expressions": exps, "words": int(wc.group(1)) if wc else None})
    return cards


def completed_keys(progress, bank):
    """Current-season keys the learner has completed (maps old IDs if needed)."""
    entries = (progress or {}).get("topics_completed", [])
    old_to_new, current = build_maps(bank)
    same_season = (progress or {}).get("bank_season") == bank["metadata"]["season_code"]
    done = set()
    for e in entries:
        if isinstance(e, str):  # legacy state_manager format "part:topic_id"
            part, _, tid = e.partition(":")
            e = {"part": part, "topic_id": tid}
        if e.get("part") not in ("part1", "part23") or not e.get("topic_id") or e.get("retired"):
            continue
        k = f"{e['part']}:{e['topic_id']}"
        if same_season or "legacy_topic_id" in e:
            if k in current:
                done.add(k)
        elif k in old_to_new:
            done.add(f"{e['part']}:{old_to_new[k][0]}")
    return done


def days_left(exam):
    try:
        return (datetime.strptime(exam, "%Y-%m-%d").date() - date.today()).days
    except (TypeError, ValueError):
        return None


def countdown_text(n):
    if n is None:
        return "考试日期未设置"
    if n > 0:
        return f"距考试 {n} 天"
    return "考试日" if n == 0 else "备考周期已结束"


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def fill(template, mapping):
    for k, v in mapping.items():
        template = template.replace("{{" + k + "}}", v)
    return template


def back_link(page):
    return page.replace('<div class="header-inner">',
                        '<div class="header-inner"><a href="index.html" style="color:#fff;opacity:.8;'
                        'font-size:.8rem;text-decoration:none">← 冲刺中心</a>', 1)


def default_materials(profile, progress):
    personal = (profile or {}).get("personal") or (profile or {}).get("personal_info") or {}
    cards = []
    bio = []
    for k, v in personal.items():
        if k in ("name", "preferences") or not v:
            continue
        v = "、".join(map(str, v)) if isinstance(v, list) else str(v)
        bio.append(f"{k.replace('_', ' ')}: {v}")
    if bio:
        cards.append({"title": "📖 我的背景（万能开头）", "tags": ["身份", "万能素材"], "items": bio[:8]})
    stories = [e.get("topic_name") for e in (progress or {}).get("topics_completed", [])
               if isinstance(e, dict) and e.get("part") == "part23" and e.get("topic_name")]
    if stories:
        cards.append({"title": "🎙️ 已打磨的 Part 2 故事", "tags": ["可迁移", "人物/地点/经历"],
                      "items": stories[-12:]})
    return cards


def render_materials(cards):
    out = ['    <div id="materials">',
           '        <h2 class="section-title">🎒 我的个人素材库（考场上直接调用）</h2>',
           '        <p style="color:var(--text-secondary); font-size:0.85rem; margin-bottom:1rem;">'
           '遇到新题先想"哪个故事最接近"，再套用对应逻辑链条。</p>',
           '        <div class="material-grid">']
    for c in cards:
        tags = "".join(f'<span class="mc-tag">{E(t)}</span>' for t in c.get("tags", []))
        items = "".join(f"<li>{E(i)}</li>" for i in c.get("items", []))
        out.append(f'            <div class="material-card"><div class="mc-title">{E(c.get("title", ""))}</div>'
                   f'<div class="mc-tags">{tags}</div><div class="mc-body"><ul>{items}</ul></div></div>')
    out += ["        </div>", "    </div>"]
    return "\n".join(out)


BASE_CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#1a237e;--navy-light:#283593;--gold:#ffc107;--coral:#e91e63;--teal:#00897b;
--purple:#6a1b9a;--bg:#f5f6fa;--card:#fff;--text:#212121;--text2:#616161;--border:#e0e0e0;
--shadow:0 2px 10px rgba(26,35,126,.08);--radius:16px}
body{font-family:'Segoe UI','PingFang SC','Microsoft YaHei',system-ui,sans-serif;background:var(--bg);
color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}
.hero{background:linear-gradient(135deg,#1a237e 0%,#3949ab 60%,#e65100 160%);color:#fff;
padding:2rem 1.2rem 1.6rem;text-align:center}
.hero h1{font-size:1.5rem;font-weight:800;letter-spacing:-.5px}.hero p{font-size:.85rem;opacity:.9;margin-top:.4rem}
.hero a{color:#fff;opacity:.8;font-size:.8rem;text-decoration:none}
.countdown{display:inline-block;margin-top:.9rem;background:rgba(255,255,255,.15);
border:1px solid rgba(255,255,255,.3);padding:.4rem 1.2rem;border-radius:99px;font-size:.85rem;font-weight:700}
.gold{color:var(--gold)}
.main{max-width:640px;margin:0 auto;padding:1.2rem 1rem 2.5rem}.main.wide{max-width:1000px}
.section-label{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text2);margin:1.4rem 0 .6rem}
.card{display:flex;align-items:center;gap:.9rem;background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);
padding:1rem 1.1rem;margin-bottom:.7rem;text-decoration:none;color:var(--text);border:1px solid rgba(224,224,224,.5);
transition:transform .15s}
.card:hover{transform:translateY(-2px)}
.card .icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0}
.card .body{flex:1;min-width:0}.card .title{font-size:.98rem;font-weight:700;color:var(--navy)}
.card .desc{font-size:.78rem;color:var(--text2);margin-top:.15rem}.card .arrow{font-size:1.2rem;color:#bbb}
.i1{background:#fff3e0}.i2{background:#e8f5e9}.i3{background:#e3f2fd}.i4{background:#f3e5f5}.i5{background:#fce4ec}
.tip-box{background:#fff8e1;border:1px solid #ffe082;border-radius:var(--radius);padding:1rem 1.1rem;font-size:.82rem;color:#795548;margin-top:1.4rem}
.tip-box b{color:#e65100}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(95px,1fr));gap:.6rem;margin-top:1rem}
.stat{background:var(--card);border-radius:12px;box-shadow:var(--shadow);padding:.8rem;text-align:center;border:1px solid var(--border)}
.stat b{display:block;font-size:1.4rem;color:var(--navy)}.stat span{font-size:.72rem;color:var(--text2)}
.section-title{font-size:1.2rem;font-weight:800;color:var(--navy);margin:2rem 0 .9rem;padding-bottom:.4rem;border-bottom:3px solid var(--gold)}
.cov{background:var(--card);border-radius:12px;box-shadow:var(--shadow);padding:.9rem 1rem;margin-bottom:.7rem;border:1px solid var(--border)}
.cov-head{display:flex;justify-content:space-between;font-weight:700;color:var(--navy);font-size:.9rem}
.bar{height:8px;background:#e8eaf6;border-radius:99px;margin:.45rem 0 .5rem;overflow:hidden}
.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--teal),var(--gold))}
.todo{display:flex;flex-wrap:wrap;gap:.35rem}.todo span{font-size:.72rem;background:#fce4ec;color:#ad1457;padding:.15rem .6rem;border-radius:99px}
.todo span.ok{background:#e0f2f1;color:#00695c}
.expr-tools{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.8rem}
.expr-tools input{flex:1;min-width:200px;padding:.55rem .8rem;border:1px solid var(--border);border-radius:10px;font-size:.9rem}
.expr-tools button{border:1px solid var(--border);background:var(--card);border-radius:99px;padding:.3rem .8rem;font-size:.78rem;cursor:pointer}
.expr-tools button.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.expr-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.45rem}
.expr{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:.5rem .75rem;font-size:.84rem}
.expr b{color:var(--navy)}.expr small{display:block;color:var(--text2);font-size:.74rem}
.expr em{display:block;font-style:normal;font-size:.66rem;color:var(--teal);font-weight:700;margin-bottom:.1rem}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden;box-shadow:var(--shadow);font-size:.84rem}
th,td{padding:.5rem .7rem;border-bottom:1px solid var(--border);text-align:left}th{background:#e8eaf6;color:var(--navy)}
.footer{text-align:center;padding:1.5rem;font-size:.78rem;color:var(--text2)}
@media print{.expr-tools{display:none}}
"""


def page(title, body, wide=False):
    return (f'<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"<title>{E(title)}</title>\n<style>{BASE_CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n")


def render_index(ctx):
    link = lambda href, icon, cls, title, desc: (
        f'    <a class="card" href="{href}"><div class="icon {cls}">{icon}</div><div class="body">'
        f'<div class="title">{E(title)}</div><div class="desc">{E(desc)}</div></div><span class="arrow">›</span></a>')
    s = ctx["stats"]
    body = [
        '<div class="hero">',
        f'    <h1>🎯 {E(ctx["title"])}</h1>',
        f'    <p>{E(ctx["season"])} 题库 · 目标 Band {E(ctx["ts"])} / {E(ctx["tw"])}</p>',
        f'    <div class="countdown">📅 {E(ctx["exam_label"])} · <span class="gold">{E(ctx["countdown"])}</span></div>',
        "</div>", '<main class="main">',
        '    <div class="stats">'
        f'<div class="stat"><b>{s["days"]}</b><span>练习天数</span></div>'
        f'<div class="stat"><b>{s["topics"]}</b><span>已备口语话题</span></div>'
        f'<div class="stat"><b>{s["essays"]}</b><span>作文范文</span></div>'
        f'<div class="stat"><b>{s["exprs"]}</b><span>亮点表达</span></div></div>',
        '    <div class="section-label">🔴 优先看</div>',
        link("speaking_sprint.html", "🎤", "i1", "口语最后冲刺", "答题节奏 + 逻辑链条 + 我的素材库"),
        link("review.html", "🧭", "i4", "备考复盘", f"题库覆盖 {s['coverage']} · 补漏清单 · 表达库"),
        '    <div class="section-label">✍️ 写作模板</div>',
        link("task2_templates.html", "📝", "i2", "Task 2 模板速查", "5 大题型 + 反 AI 味 + Band 7 衔接"),
        link("task1_templates.html", "📊", "i3", "Task 1 模板速查", "6 大题型模板 + 万能表达"),
    ]
    if ctx["has_answers"]:
        body += ['    <div class="section-label">📚 我的答案库</div>',
                 link("ielts_answers.html", "🗂️", "i5", "全部模型答案",
                      f"{s['p1']} 个 Part 1 + {s['p23']} 个 Part 2&3 + {s['essays']} 篇作文")]
    body += [f'    <div class="tip-box">{ctx["tip"]}</div>', "</main>",
             f'<footer class="footer">Generated by ielts-coach · {date.today().isoformat()}</footer>']
    return page(ctx["title"], "\n".join(body))


def render_review(ctx):
    s = ctx["stats"]
    out = ['<div class="hero">', '    <a href="index.html">← 冲刺中心</a>',
           '    <h1>🧭 备考复盘</h1>',
           f'    <p>{E(ctx["season"])} 题库覆盖情况 · 未准备的话题 · 全部亮点表达</p>', "</div>",
           '<main class="main wide">',
           '    <div class="stats">'
           f'<div class="stat"><b>{s["days"]}</b><span>练习天数</span></div>'
           f'<div class="stat"><b>{s["coverage"]}</b><span>当季题库覆盖</span></div>'
           f'<div class="stat"><b>{s["answers"]}</b><span>答案卡片</span></div>'
           f'<div class="stat"><b>{s["exprs"]}</b><span>亮点表达</span></div></div>',
           '    <h2 class="section-title">📋 当季题库覆盖 & 补漏清单</h2>',
           '    <p style="font-size:.8rem;color:var(--text2);margin-bottom:.7rem">红色 = 还没准备，考前优先补；'
           '绿色 = 已有范文。保留题可沿用上季度答案。</p>']
    for sec in ctx["coverage"]:
        pct = int(100 * sec["done"] / sec["total"]) if sec["total"] else 0
        pills = "".join(f'<span class="{"ok" if ok else ""}">{E(n)}</span>' for n, ok in sec["topics"])
        out.append(f'    <div class="cov"><div class="cov-head"><span>{E(sec["label"])}</span>'
                   f'<span>{sec["done"]}/{sec["total"]}</span></div><div class="bar"><i style="width:{pct}%"></i></div>'
                   f'<div class="todo">{pills}</div></div>')
    out.append('    <h2 class="section-title">🌟 亮点表达库</h2>')
    if ctx["expressions"]:
        buttons = "".join(f'<button data-p="{p}">{PART_LABEL.get(p, p)}</button>'
                          for p in sorted({e[2] for e in ctx["expressions"]}))
        out.append('    <div class="expr-tools"><input id="q" placeholder="搜索表达或中文释义…" aria-label="搜索表达">'
                   f'<button data-p="" class="on">全部</button>{buttons}</div>')
        out.append('    <div class="expr-grid" id="exprs">')
        for exp, meaning, part, topic in ctx["expressions"]:
            out.append(f'        <div class="expr" data-p="{part}"><em>{PART_LABEL.get(part, part)} · {E(topic)}</em>'
                       f'<b>{E(exp)}</b><small>{E(meaning)}</small></div>')
        out.append("    </div>")
        out.append("""    <script>
    (function(){var q=document.getElementById('q'),p='',items=[].slice.call(document.querySelectorAll('.expr'));
    function run(){var t=q.value.toLowerCase();items.forEach(function(el){
      el.style.display=((!p||el.dataset.p===p)&&el.textContent.toLowerCase().indexOf(t)>-1)?'':'none';});}
    q.addEventListener('input',run);
    [].forEach.call(document.querySelectorAll('.expr-tools button'),function(b){b.addEventListener('click',function(){
      p=b.dataset.p;[].forEach.call(document.querySelectorAll('.expr-tools button'),function(x){x.classList.remove('on');});
      b.classList.add('on');run();});});})();
    </script>""")
    else:
        out.append('    <p style="font-size:.85rem;color:var(--text2)">ielts_answers.html 里还没有亮点表达。</p>')
    if ctx["essays"]:
        out.append('    <h2 class="section-title">✍️ 作文范文清单</h2>')
        rows = "".join(f"<tr><td>{PART_LABEL.get(p, p)}</td><td>{E(t)}</td><td>{w or '—'}</td></tr>"
                       for p, t, w in ctx["essays"])
        out.append(f"    <table><tr><th>类型</th><th>题目</th><th>词数</th></tr>{rows}</table>")
    if ctx["warnings"]:
        out.append('    <div class="tip-box"><b>⚠️ 生成提示：</b>' + "；".join(map(E, ctx["warnings"])) + "</div>")
    out += ["</main>", f'<footer class="footer">Generated by ielts-coach · {date.today().isoformat()}</footer>']
    return page("IELTS 备考复盘", "\n".join(out), wide=True)


# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default=None, help="output dir (default <root>/summary_site)")
    ap.add_argument("--content", default=None, help="agent-written summary_content.json")
    ap.add_argument("--bank", default=str(BANK))
    ap.add_argument("--include-nonmainland", action="store_true")
    a = ap.parse_args(argv)

    root = Path(a.root).resolve()
    out = Path(a.out).resolve() if a.out else root / "summary_site"
    warnings = []
    profile = load_json(root / "user_profile.json", warnings)
    progress = load_json(root / "progress.json", warnings)
    load_json(root / "study_plan.json", warnings)  # only validated; plan is not rendered
    bank = json.loads(Path(a.bank).read_text(encoding="utf-8"))
    content_path = Path(a.content) if a.content else root / "summary_content.json"
    content = load_json(content_path, warnings) or {}
    if not profile:
        warnings.append("user_profile.json not found; targets and countdown are blank")
    profile = profile or {}

    answers_path = root / "ielts_answers.html"
    cards = parse_answers(answers_path)

    done = completed_keys(progress, bank)
    keys = SECTION_KEYS if a.include_nonmainland else [k for k in SECTION_KEYS if "nonmainland" not in k]
    coverage, total, total_done = [], 0, 0
    for key in keys:
        part = "part1" if key.startswith("part1") else "part23"
        topics = [((t.get("name_en") if part == "part1" else t.get("name_cn")) or t["topic_id"],
                   f"{part}:{t['topic_id']}" in done) for t in bank.get(key, [])]
        n_done = sum(ok for _, ok in topics)
        coverage.append({"label": SECTION_LABEL[key], "done": n_done, "total": len(topics),
                         "topics": sorted(topics, key=lambda x: x[1])})
        total += len(topics)
        total_done += n_done

    seen, expressions = set(), []
    for c in cards:
        for exp, meaning in c["expressions"]:
            k = exp.lower()
            if k not in seen:
                seen.add(k)
                expressions.append((exp, meaning, c["part"], c["title"]))
    essays = [(c["part"], c["title"], c["words"]) for c in cards if c["part"] in ("wt1", "wt2")]
    completed = [e for e in (progress or {}).get("topics_completed", []) if isinstance(e, dict)]
    dates = {e.get("completed_date") for e in completed if e.get("completed_date")}
    parts = defaultdict(set)
    for c in cards:
        parts[c["part"]].add(c["title"])

    n_left = days_left(profile.get("exam_date"))
    ts = str(profile.get("target_speaking", "—"))
    tw = str(profile.get("target_writing", "—"))
    stats = {"days": len(dates) or (progress or {}).get("days_completed", 0),
             "topics": len({(e.get("part"), e.get("topic_name")) for e in completed
                            if e.get("part") in ("part1", "part23")}),
             "essays": len(essays), "exprs": len(expressions), "answers": len(cards),
             "p1": len(parts["p1"]), "p23": len(parts["p2"]),
             "coverage": f"{int(100 * total_done / total) if total else 0}%"}
    tip = ("<b>💡 考前建议：</b>先过一遍 <b>口语冲刺</b>的素材库和逻辑链条，"
           "再到 <b>备考复盘</b>补齐红色话题；写作只背结构和反 AI 味清单。")
    ctx = {"title": content.get("title", "IELTS 冲刺中心"), "season": bank["metadata"]["season"],
           "ts": ts, "tw": tw, "countdown": countdown_text(n_left),
           "exam_label": f"考试日 {profile.get('exam_date', '未设置')}", "stats": stats,
           "has_answers": answers_path.exists(),
           "tip": E(content["tip"]) if content.get("tip") else tip,
           "coverage": coverage, "expressions": expressions, "essays": essays, "warnings": warnings}

    out.mkdir(parents=True, exist_ok=True)
    common = {"TARGET_SPEAKING": E(ts), "TARGET_WRITING": E(tw), "COUNTDOWN": E(countdown_text(n_left))}
    materials = content.get("materials") or default_materials(profile, progress)
    sprint = (ASSETS / "speaking_sprint.html").read_text(encoding="utf-8")
    (out / "speaking_sprint.html").write_text(
        back_link(fill(sprint, {**common, "MATERIALS": render_materials(materials)})), encoding="utf-8")
    for name in ("task1_templates.html", "task2_templates.html"):
        t = (ASSETS / name).read_text(encoding="utf-8")
        (out / name).write_text(back_link(fill(t, common)), encoding="utf-8")
    (out / "index.html").write_text(render_index(ctx), encoding="utf-8")
    (out / "review.html").write_text(render_review(ctx), encoding="utf-8")
    if answers_path.exists():
        shutil.copy2(answers_path, out / "ielts_answers.html")
        charts = root / "task1_charts"
        if charts.is_dir() and "task1_charts/" in answers_path.read_text(encoding="utf-8"):
            shutil.copytree(charts, out / "task1_charts", dirs_exist_ok=True)

    print(f"summary site written to {out}")
    print(f"  coverage {stats['coverage']} ({total_done}/{total}) | answers {len(cards)} | "
          f"expressions {len(expressions)} | essays {len(essays)}")
    for w in warnings:
        print(f"  WARNING: {w}")
    print("  open index.html in a browser. It contains personal data: publish only if you mean to.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
