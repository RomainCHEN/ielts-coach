"""Regression tests for the ielts-coach scripts (stdlib unittest).

Run from the repository root:  python -m unittest discover -s tests -v
The PDF parser test runs only when the season PDF is present locally
(the PDF itself is not committed).
"""
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "ielts-coach"
sys.path.insert(0, str(SKILL / "scripts"))

import build_complete_bank as bcb  # noqa: E402
import build_summary_site as bss  # noqa: E402
import migrate_season as ms  # noqa: E402

BANK_PATH = SKILL / "references" / "question_bank_complete.json"
DEMO = REPO / "tests" / "fixtures" / "demo"


def quiet(fn, *args):
    with redirect_stdout(io.StringIO()):
        return fn(*args)


class BankShape(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))

    def test_counts_match_metadata(self):
        tt = self.bank["metadata"]["total_topics"]
        for key in ms.SECTION_KEYS:
            self.assertEqual(len(self.bank[key]), tt[key], key)
        self.assertEqual(sum(tt[k] for k in ms.SECTION_KEYS), tt["total"])

    def test_topic_fields(self):
        for key in ms.SECTION_KEYS:
            for t in self.bank[key]:
                self.assertTrue(t["topic_id"].endswith(f"-{t['id']}"))
                self.assertTrue(t["name_en"] and t["name_cn"], f"{key}#{t['id']} names")
                if key.startswith("part1"):
                    self.assertGreaterEqual(len(t["questions"]), 3)
                else:
                    self.assertTrue(t["cue_card"].startswith("Describe"))
                    self.assertGreaterEqual(len(t["cue_points"]), 3)
                    self.assertGreaterEqual(len(t["part3"]), 3)

    def test_ids_unique_per_part(self):
        for part in ("part1", "part23"):
            ids = [t["topic_id"] for k in ms.SECTION_KEYS if k.startswith(part + "_")
                   for t in self.bank[k]]
            self.assertEqual(len(ids), len(set(ids)), part)

    def test_markdown_in_sync(self):
        md = (SKILL / "references" / "question-bank.md").read_text(encoding="utf-8")
        self.assertIn(f"**Total: {self.bank['metadata']['total_topics']['total']} topics**", md)
        self.assertEqual(md.count("\n### "), self.bank["metadata"]["total_topics"]["total"])


class Parser(unittest.TestCase):
    def test_wrapped_lines_are_joined(self):
        self.assertEqual(bcb.join_wrapped(["Do you spend your mornings on both weekends and",
                                           "weekdays? Why?", "Next?"]),
                         ["Do you spend your mornings on both weekends and weekdays? Why?", "Next?"])

    def test_derive_name(self):
        self.assertEqual(bcb.derive_name_en("Describe a public building you enjoy visiting (e.g. a library)"),
                         "A Public Building You Enjoy Visiting")

    def test_small_synthetic_pdf_text(self):
        pages = ["目录 skipped", "一、 大陆地区新题\nPart 1  9 月在考新题（1 道）\n1  P1  Shoes\n"
                 "Do you like shoes?\nHow often do you buy\nshoes?\nWhy?\n"
                 "Part 2&3  9 月在考新题（1 道）\n1  P2  嘈杂地\nDescribe a noisy place\n"
                 "You should say：\nWhere it is\nWhen you went there\nAnd explain why\nP3\n"
                 "Is noise bad?\nWhy?\nWho cares?\n"]
        bank, declared = bcb.parse_bank(bcb.clean_lines(pages))
        self.assertEqual(declared, {"part1_new": 1, "part23_new": 1})
        self.assertEqual(bank["part1_new"][0]["questions"][1], "How often do you buy shoes?")
        self.assertEqual(bank["part23_new"][0]["cue_points"][-1], "And explain why")
        self.assertEqual(bcb.validate(bank, declared), [])

    @unittest.skipUnless(list(REPO.glob("2026年9-12月*.pdf")), "season PDF not present")
    def test_real_pdf_matches_committed_bank(self):
        pdf = next(REPO.glob("2026年9-12月*.pdf"))
        bank, declared = bcb.parse_bank(bcb.clean_lines(bcb.extract_pages(pdf)))
        self.assertEqual(bcb.validate(bank, declared), [])
        committed = json.loads(BANK_PATH.read_text(encoding="utf-8"))
        for key in ms.SECTION_KEYS:
            self.assertEqual([t.get("questions", t.get("part3")) for t in bank[key]],
                             [t.get("questions", t.get("part3")) for t in committed[key]], key)


class MigrationAndSite(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in DEMO.iterdir():
            shutil.copy2(f, self.tmp / f.name)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_migration_dry_run_then_apply_is_idempotent(self):
        before = (self.tmp / "progress.json").read_text(encoding="utf-8")
        quiet(ms.main, ["--root", str(self.tmp)])
        self.assertEqual((self.tmp / "progress.json").read_text(encoding="utf-8"), before)

        quiet(ms.main, ["--root", str(self.tmp), "--apply"])
        prog = json.loads((self.tmp / "progress.json").read_text(encoding="utf-8"))
        by_name = {e["topic_name"]: e for e in prog["topics_completed"]}
        self.assertEqual(by_name["Music"]["topic_id"], "retained-1")          # P1 new-1 -> retained-1
        self.assertEqual(by_name["An Interesting Video"]["topic_id"], "retained-2")
        self.assertTrue(by_name["Food"]["retired"])                          # dropped this season
        self.assertEqual(by_name["Hometown"]["topic_id"], "essential-3")
        self.assertNotIn("legacy_topic_id", by_name["Public Transport Funding"])
        self.assertTrue(list(self.tmp.glob("progress.json.bak-*")))

        snapshot = (self.tmp / "progress.json").read_text(encoding="utf-8")
        quiet(ms.main, ["--root", str(self.tmp), "--apply"])
        self.assertEqual((self.tmp / "progress.json").read_text(encoding="utf-8"), snapshot)

    def test_malformed_state_is_reported_not_rewritten(self):
        (self.tmp / "study_plan.json").write_text('{"schedule": [ }', encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            ms.main(["--root", str(self.tmp), "--apply"])
        self.assertIn("malformed", out.getvalue())
        self.assertEqual((self.tmp / "study_plan.json").read_text(encoding="utf-8"), '{"schedule": [ }')

    def test_summary_site(self):
        out_dir = self.tmp / "site"
        quiet(bss.main, ["--root", str(self.tmp), "--out", str(out_dir)])
        names = {p.name for p in out_dir.iterdir()}
        self.assertTrue({"index.html", "review.html", "speaking_sprint.html", "task1_templates.html",
                         "task2_templates.html", "ielts_answers.html"} <= names)
        for p in out_dir.glob("*.html"):
            self.assertNotIn("{{", p.read_text(encoding="utf-8"), p.name)
        review = (out_dir / "review.html").read_text(encoding="utf-8")
        self.assertIn("keeps me going", review)
        self.assertIn("Public Transport Funding", review)
        index = (out_dir / "index.html").read_text(encoding="utf-8")
        self.assertIn("7.0 / 6.5", index)
        sprint = (out_dir / "speaking_sprint.html").read_text(encoding="utf-8")
        self.assertIn("Hangzhou", sprint)  # default material card from profile

    def test_agent_content_is_escaped(self):
        (self.tmp / "summary_content.json").write_text(json.dumps({
            "materials": [{"title": "<b>x</b>", "tags": ["t"], "items": ["<script>alert(1)</script>"]}],
            "tip": "<img src=x onerror=alert(1)>"}), encoding="utf-8")
        out_dir = self.tmp / "site"
        quiet(bss.main, ["--root", str(self.tmp), "--out", str(out_dir)])
        self.assertNotIn("<script>alert", (out_dir / "speaking_sprint.html").read_text(encoding="utf-8"))
        self.assertNotIn("<img src=x", (out_dir / "index.html").read_text(encoding="utf-8"))


class TemplatesArePublicSafe(unittest.TestCase):
    """Shipped assets must not carry anyone's personal material."""

    def test_no_personal_markers(self):
        for p in (SKILL / "assets" / "summary_site").glob("*.html"):
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("material-card\"><div class=\"mc-title\"", text, p.name)
            self.assertNotRegex(text, r"目标 Band \d|目标 \d\.\d|距离考试 \d+ 天", p.name)


if __name__ == "__main__":
    unittest.main()
