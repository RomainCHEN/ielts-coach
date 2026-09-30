<p align="center">
  <img src="docs/readme/hero.svg" width="100%" alt="IELTS Coach: interviews you first, then writes band-calibrated model answers in your own voice. 2026 Sep-Dec bank, 100 topics.">
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/RomainCHEN/ielts-coach?style=flat-square&color=yellow" alt="Stars">
  <img src="https://img.shields.io/github/license/RomainCHEN/ielts-coach?style=flat-square&color=blue" alt="License">
  <img src="https://img.shields.io/badge/version-v4.0-1a237e?style=flat-square" alt="Version 4.0">
  <img src="https://img.shields.io/badge/bank-2026%20Sep--Dec%20·%20100%20topics-ffc107?style=flat-square" alt="Question bank: 2026 Sep-Dec, 100 topics">
</p>

<p align="center"><a href="README_zh.md">简体中文</a> · English</p>

IELTS Coach is an agent skill for IELTS Speaking and Writing. It asks about your own experiences before writing anything, then turns your raw answers into model answers at your target band, collected in a local HTML page you can revise from. When the cycle ends, it builds a prep summary website from everything you practised.

## What you get

<table>
<tr>
<td width="50%"><img src="docs/screenshots/site_hub.png" alt="Summary site hub on a phone: countdown, targets, practice stats and links to the sprint sheets"></td>
<td width="50%"><img src="docs/screenshots/site_review.png" alt="Review page: current bank coverage per section, unprepared topics in red"><br><br><img src="docs/screenshots/site_materials.png" alt="Personal material cards: reusable stories tagged by topic type"></td>
</tr>
</table>

<sub>Screenshots use the fictional demo learner in <code>tests/fixtures/demo</code>.</sub>

- **Model answers in your voice.** Every topic starts with Topic Discovery: a local web form (or chat) that asks what you actually think and remember. The answer is a polished version of that, so it is easy to memorise.
- **Band calibration.** Vocabulary, structures and cohesion follow the IELTS descriptors for your target band; writing answers are checked against the official Writing Band Descriptors (May 2023) and an anti-AI-flavour list (no em dashes, no "Firstly/Secondly/Finally").
- **A plan that never repeats.** Topics are spread over your available days and tracked in JSON state files across sessions.
- **The current bank.** 2026 Sep-Dec (cut-off 24 Sep), 100 speaking topics, parsed straight from the season PDF.
- **Season migration.** When a new bank arrives, topics you already prepared keep counting if they were carried over.
- **One-click summary site.** Countdown hub, speaking sprint sheet with your own story cards, Task 1/Task 2 template sheets, a coverage review with a gap list, and a searchable bank of every highlight expression.

## How it works

<p align="center"><img src="docs/readme/workflow.svg" width="100%" alt="Onboard, plan, discover, polish, review; each session loops discover and polish. New season: PDF, build_complete_bank, migrate_season, plan goes on."></p>

<p align="center"><img src="docs/screenshots/form_overview.png" width="70%" alt="Topic Discovery web form opened in the browser"></p>

## Quick start

1. Give this repository URL to your agent and ask it to install the skill, or copy the folder yourself:
   ```bash
   git clone https://github.com/RomainCHEN/ielts-coach.git
   cp -r ielts-coach/ielts-coach <your-project>/.claude/skills/   # Claude Code
   # other agents: copy ielts-coach/ into the agent's skills directory
   ```
2. In your project, say "Start my IELTS preparation" (or "开始备考"). The agent asks for your exam date, target bands and background, then proposes a plan.
3. Each day, say "Start today's practice". Open `ielts_answers.html` to review.
4. At the end, say "Make my summary site" and open `summary_site/index.html`.

Requirements: Python 3.10+ for the scripts. `pip install pymupdf` is needed only to rebuild the bank from a PDF (`pdfplumber`, if installed, adds a cross-check). The vision bridge for non-vision models needs `pip install mcp httpx`.

## Question bank

| Section | Topics |
|---|---|
| Part 1 new / retained / essential | 11 / 17 / 5 |
| Part 2&3 new / retained | 28 / 27 |
| Non-mainland Part 1 / Part 2&3 | 6 / 6 |
| **Mainland candidates / all** | **88 / 100** |

The bank lives in [`ielts-coach/references/question_bank_complete.json`](ielts-coach/references/question_bank_complete.json) (for the agent) and [`question-bank.md`](ielts-coach/references/question-bank.md) (for you). 48 topics are marked as carried over from May-Aug 2026.

### Updating to a new season

<p align="center"><img src="docs/readme/terminal.svg" width="100%" alt="Terminal: the bank builder parses 100 topics with a matching pdfplumber cross-check, the migration dry run carries topics over, the site builder reports coverage."></p>

```bash
python ielts-coach/scripts/build_complete_bank.py --pdf "<season>.pdf" \
  --season "2027年1-4月" --season-code 2027-01-04 --cutoff 2027-01-20 \
  --previous-json old/question_bank_complete.json --previous-md old/question-bank.md
python ielts-coach/scripts/migrate_season.py --root .          # dry run, then --apply
```

The builder refuses to write if any section count differs from the count printed in the PDF. Scanned PDFs have no text layer: OCR them first (for example with MinerU) and pass the text with `--text`.

## Your data stays local

`user_profile.json`, `study_plan.json`, `progress.json`, `ielts_answers.html`, `summary_content.json` and `summary_site/` are created in your project and are git-ignored. The summary site contains your personal stories; publishing it is your call. The optional vision bridge sends chart images to the provider you configure.

## Project structure

```
ielts-coach/                      the skill (copy this folder)
├── SKILL.md                      main flow: season check → onboarding → sessions → summary site
├── references/                   loaded on demand
│   ├── question_bank_complete.json · question-bank.md
│   ├── topic-discovery.md · answer-formats.md · html-rendering.md · vision-fallback.md
│   └── band-descriptors.md · writing-band-descriptors.md · writing-resources.md · sample-answers.md
├── scripts/
│   ├── build_complete_bank.py    season PDF → bank files (validated, cross-checked)
│   ├── migrate_season.py         carry progress over to a new season
│   ├── build_summary_site.py     one-click prep summary website
│   ├── topic_form_server.py      Topic Discovery web form
│   ├── state_manager.py          JSON state helpers
│   └── vision_mcp_server.py      MCP vision bridge for non-vision models
└── assets/
    ├── answer_template.html      answer page template
    └── summary_site/             generic sprint and template sheets
tests/                            python -m unittest discover -s tests
```

## Non-vision models

If your model cannot read Task 1 charts (DeepSeek, for example), the agent sets up a small MCP server that forwards the image to a vision model: Alibaba Cloud Bailian `qwen3.7-plus` by default, or any OpenAI-compatible endpoint. You provide the API key and restart the agent. Details: [`references/vision-fallback.md`](ielts-coach/references/vision-fallback.md). The key is stored in the agent's MCP config file in plain text, so keep that file out of version control.

## Contributing

Issues and PRs are welcome: wrong or missing questions, parser failures on a new season PDF, design fixes for the HTML pages, AI-flavour patterns that slipped through. Run the tests before opening a PR.

## License

MIT © [Romain Chen](https://github.com/RomainCHEN)
