# IELTS Speaking & Writing Coach

This project contains an AI agent skill for deeply customized IELTS preparation.
The skill generates personalized model answers, manages a dynamic study plan, and renders
all content to a beautiful local HTML page.

## Project Structure

```
skill/
├── SKILL.md                              # Core agent behavior instructions
├── references/
│   ├── question-bank.md                  # Part 1 + P2&3 New topics (full detail)
│   ├── question_bank_complete.json       # All P2&3 Retained + Non-mainland topics
│   ├── band-descriptors.md               # IELTS band criteria reference
│   ├── writing-resources.md              # Task 1 chart language, Task 2 templates
│   └── sample-answers.md                 # Calibrated example answers for quality
├── scripts/
│   ├── state_manager.py                  # JSON state file management
│   └── build_complete_bank.py            # Complete question bank builder
└── assets/
    └── answer_template.html              # HTML template for answer display
```

## Agent Compatibility

This skill uses standard MCP protocol and OpenAI-compatible APIs. It works with:

- **Claude Code** — copy `skill/` into `.claude/skills/ielts-coach/`
- **Cursor, Codex CLI, Gemini CLI, OpenCode, Antigravity** — copy `skill/` into the agent's skill directory
- **Any agent** supporting MCP — the vision bridge server is standard MCP

## How to Use

Invoke the skill by mentioning IELTS preparation, asking for speaking/writing practice,
or referencing your exam date or target scores. The skill triggers automatically.

Session state is managed through these JSON files (created during onboarding):
- `user_profile.json` — Exam date, target scores, personal background
- `study_plan.json` — Day-by-day study plan with assigned topics
- `progress.json` — Topics completed, answers generated, daily log

Generated model answers: `ielts_answers.html` — Open in browser.

## Question Bank

Covers the **May-August 2026** IELTS season:
- Part 1: 38 topics | Part 2&3 New: 29 | Part 2&3 Retained: 27 | Non-mainland: 8
- **Total: 102 speaking topics** (94 for mainland candidates)

Extracted using PyMuPDF + MinerU API.

## Key Design Decisions

- **No topic repetition** — Each session covers unique topics unless user requests review
- **Personalization first** — Every answer uses the user's background, not generic content
- **Band calibration** — Vocabulary density, sentence complexity, and cohesive devices match target band
- **HTML-first output** — All answers rendered in a responsive, printable page with highlights
- **Stateful sessions** — Progress tracked across conversations via JSON state files
- **Provider-agnostic** — Works with any agent platform, not just Claude Code

## Edge Cases Handled

- First session without profile → auto-onboarding
- User skips personalization → generic version offered, customization available
- Exam date passed → alert + recalculation
- All topics exhausted → review cycle with user consent
- Missed sessions → gap acknowledged, options offered
- File corruption → partial recovery + targeted re-onboarding
- Non-vision models → MCP vision bridge auto-setup
