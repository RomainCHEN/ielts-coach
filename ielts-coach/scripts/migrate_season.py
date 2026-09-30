"""
Migrate a learner's progress to a new question-bank season.

When the bank is rebuilt for a new season, topic IDs are renumbered
(e.g. last season's `part23:new-2` is this season's `part23:retained-2`).
This script rewrites the IDs in progress.json / study_plan.json using the
`carried_over_from` links written by build_complete_bank.py, so the
"never repeat a completed topic" rule keeps working across seasons.

  python migrate_season.py                 # dry run: report only
  python migrate_season.py --apply         # write (backups *.bak-<season> first)
  python migrate_season.py --root <dir>    # project dir holding the state files

Idempotent: once progress.json carries `bank_season` == current season, it
does nothing. Completed topics that left the bank are kept for history and
marked `"retired": true`; pending plan items that left the bank are marked
`"needs_replan": true` so the agent can swap in a current topic.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
BANK = SKILL / "references" / "question_bank_complete.json"
SECTION_KEYS = ["part1_new", "part23_new", "part1_retained", "part1_essential",
                "part23_retained", "part1_nonmainland", "part23_nonmainland"]


def load(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        # never guess-repair a learner's file; report and leave it untouched
        print(f"WARNING: {path.name} is malformed (line {e.lineno}, col {e.colno}: {e.msg}); "
              f"skipped. Fix it (see SKILL.md 'File Corruption') and re-run.")
        return None


def build_maps(bank):
    """old key 'part:topic_id' -> (new topic_id, name) and set of current keys."""
    old_to_new, current = {}, set()
    for key in SECTION_KEYS:
        part = "part1" if key.startswith("part1") else "part23"
        for t in bank.get(key, []):
            current.add(f"{part}:{t['topic_id']}")
            src = t.get("carried_over_from")
            if src:
                _, p, tid = src.split(":", 2)
                old_to_new[f"{p}:{tid}"] = (t["topic_id"], t.get("name_en") or t.get("name_cn"))
    return old_to_new, current


def remap(entries, old_to_new, pending_flag):
    """Rewrite topic_id in place. Returns counts."""
    moved = gone = kept = 0
    for e in entries:
        if not isinstance(e, dict) or e.get("part") not in ("part1", "part23") or "topic_id" not in e:
            kept += 1  # writing tasks and free-form entries have no bank id
            continue
        if "legacy_topic_id" in e:
            kept += 1
            continue
        k = f"{e['part']}:{e['topic_id']}"
        if k in old_to_new:
            e["legacy_topic_id"] = e["topic_id"]
            e["topic_id"] = old_to_new[k][0]
            moved += 1
        else:
            e["legacy_topic_id"] = e["topic_id"]
            e[pending_flag] = True
            gone += 1
    return moved, gone, kept


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="directory holding progress.json/study_plan.json")
    ap.add_argument("--bank", default=str(BANK))
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)

    root = Path(a.root)
    bank = load(Path(a.bank))
    if not bank:
        sys.exit(f"bank not found: {a.bank}")
    season = bank["metadata"]["season_code"]
    prev = bank["metadata"].get("previous_season")
    progress = load(root / "progress.json")
    plan = load(root / "study_plan.json")
    if progress is None and plan is None:
        print("no state files found - nothing to migrate (first session runs onboarding)")
        return 0
    if progress and progress.get("bank_season") == season:
        print(f"already on season {season} - nothing to do")
        return 0
    if not prev:
        sys.exit("bank has no previous_season links; rebuild it with --previous-json/--previous-md")

    old_to_new, _ = build_maps(bank)
    report = []
    if progress:
        m, g, k = remap(progress.get("topics_completed", []), old_to_new, "retired")
        report.append(f"progress.json topics_completed: {m} carried over, {g} retired, {k} untouched")
        progress["bank_season"] = season
    if plan:
        m1, g1, _ = remap(plan.get("topics_used", []), old_to_new, "retired")
        pend_m = pend_g = 0
        for day in plan.get("schedule", []):
            done = day.get("status") in ("completed", "done")
            m, g, _ = remap(day.get("topics", []), old_to_new, "retired" if done else "needs_replan")
            if not done:
                pend_m, pend_g = pend_m + m, pend_g + g
        report.append(f"study_plan.json topics_used: {m1} carried over, {g1} retired")
        report.append(f"study_plan.json pending items: {pend_m} carried over, {pend_g} need re-planning")
        plan["bank_season"] = season

    print(f"migrating {prev} -> {season}")
    print("\n".join("  " + r for r in report))
    if not a.apply:
        print("dry run: re-run with --apply to write (backups are made first)")
        return 0
    for name, data in (("progress.json", progress), ("study_plan.json", plan)):
        if data is None:
            continue
        p = root / name
        shutil.copy2(p, root / f"{name}.bak-{prev}")
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  wrote {p} (backup: {name}.bak-{prev})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
