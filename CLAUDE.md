# IELTS Speaking & Writing Coach

This project contains an AI agent skill for deeply customized IELTS preparation.
The skill generates personalized model answers, manages a dynamic study plan, renders
all content to a local HTML page, and builds a prep summary website at the end of a cycle.

## Project Structure

```
ielts-coach/
├── SKILL.md                              # Main flow (season check, onboarding, sessions, summary site)
├── references/
│   ├── question_bank_complete.json       # Complete bank, all sections (generated - do not hand-edit)
│   ├── question-bank.md                  # Same bank, human-readable (generated)
│   ├── topic-discovery.md                # Web form + interview frameworks
│   ├── answer-formats.md                 # Part 1/2/3 + Task 1/2 formats, band tables, anti-AI rules
│   ├── html-rendering.md                 # ielts_answers.html layout rules
│   ├── vision-fallback.md                # MCP vision bridge setup for non-vision models
│   ├── band-descriptors.md               # Speaking band criteria
│   ├── writing-band-descriptors.md       # Official Writing descriptors (May 2023)
│   ├── writing-resources.md              # Task 1 chart language, Task 2 templates
│   └── sample-answers.md                 # Calibrated example answers
├── scripts/
│   ├── build_complete_bank.py            # Season PDF -> bank files (validated, cross-checked)
│   ├── migrate_season.py                 # Carry progress over to a new bank season
│   ├── build_summary_site.py             # One-click prep summary website
│   ├── topic_form_server.py              # Topic Discovery web form
│   ├── state_manager.py                  # JSON state helpers
│   └── vision_mcp_server.py              # MCP vision bridge
└── assets/
    ├── answer_template.html              # Answer page template
    └── summary_site/                     # Generic sprint + Task 1/2 template sheets
tests/                                    # python -m unittest discover -s tests
```

## Question Bank

Covers the **Sep-Dec 2026** IELTS season (cut-off 2026-09-24):
- Part 1: 11 new | 17 retained | 5 essential
- Part 2&3: 28 new | 27 retained
- Non-mainland: 6 Part 1 + 6 Part 2&3
- **Total: 100 speaking topics** (88 for mainland candidates); 48 carried over from May-Aug 2026

Parsed with PyMuPDF, cross-checked with pdfplumber. Rebuild with `scripts/build_complete_bank.py`.

## Public vs local

The repository is public. Never commit learner data: `user_profile.json`, `study_plan.json`,
`progress.json`, `ielts_answers.html`, `summary_content.json`, `summary_site/`, topic form
answers, root-level personal HTML pages, `task1_charts/`, `.claude/`, `.mcp.json`, PDFs.
All are git-ignored. Screenshots for docs must come from `tests/fixtures/demo` (fictional).

## Key Design Decisions

- **No topic repetition** - unique topics per session; season migration keeps this across banks
- **Personalization first** - every answer uses the learner's own content
- **Band calibration** - vocabulary, structures and cohesion match the target band
- **Programs for deterministic steps** - parsing, migration and site assembly are scripts; judgement stays with the agent
- **Stateful sessions** - progress tracked via JSON state files
- **Provider-agnostic** - works with any agent platform
