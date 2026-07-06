# 🎓 IELTS Coach — Speaking & Writing AI Preparation Agent

A deeply personalized Claude Code skill for IELTS exam preparation. This agent generates customized model answers for IELTS Speaking (Parts 1, 2, 3) and Writing (Task 1 & 2), tailored to your background, target band score, and exam timeline.

## Features

- **📋 Complete Question Bank** — 102 speaking topics covering the **May-August 2026** IELTS season
  - Part 1: 38 topics (16 new + 17 retained + 5 essential)
  - Part 2&3: 64 topics (29 new + 27 retained + 8 non-mainland)
  - Extracted from official IELTS question bank using PyMuPDF + MinerU API
- **🎯 Personalized Study Plan** — Onboarding flow collects your exam date, target scores, personal background, and availability, then generates a day-by-day study schedule
- **📝 Customized Model Answers** — Every answer uses YOUR experiences, hobbies, and opinions — making them far easier to memorize than generic templates
- **📊 Band-Score Calibrated** — Language complexity matches your target band (6/7/8) with vocabulary density, sentence structure, and cohesive devices adjusted accordingly
- **🖼️ Beautiful HTML Output** — All answers rendered in a modern, responsive, printable HTML page with highlighted vocabulary, structure notes, and copy buttons
- **🔄 Self-Evolving Plan** — The study plan adapts based on your progress, rescheduling topics and adjusting for missed sessions
- **✍️ Writing Task 1 Support** — Place chart images in `task1_charts/` and the agent analyzes them to generate model Task 1 responses

## Quick Start

### Prerequisites
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.10+ (for state management scripts)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ielts-coach.git
cd ielts-coach

# Or if you already have a project, just copy the skill:
cp -r .claude/skills/ielts-coach ~/your-project/.claude/skills/
```

### Usage

The skill triggers automatically when you mention IELTS-related topics. Just say things like:

- "Start my IELTS preparation"
- "I want to practice speaking Part 2 today"
- "Show me my study plan"
- "I have a writing task 2 question..."
- "How many days until my exam?"

**First session**: The agent will run onboarding — asking about your exam date, target scores, hobbies, work/study background, and more. This information personalizes ALL future answers.

**Daily sessions**: The agent greets you with progress stats, delivers today's unique topics, asks background questions, and generates model answers saved to `ielts_answers.html`.

## Project Structure

```
ielts-coach/
├── .claude/skills/ielts-coach/
│   ├── SKILL.md                              # Core agent behavior instructions
│   ├── references/
│   │   ├── question-bank.md                  # Part 1 + P2&3 New topics (full detail)
│   │   ├── question_bank_complete.json       # All P2&3 Retained + Non-mainland topics
│   │   ├── band-descriptors.md               # IELTS band criteria reference
│   │   ├── writing-resources.md              # Task 1 language, Task 2 templates
│   │   └── sample-answers.md                 # Calibrated example answers
│   ├── scripts/
│   │   ├── state_manager.py                  # JSON state file management
│   │   └── build_complete_bank.py            # Question bank builder from PDF data
│   └── assets/
│       └── answer_template.html              # HTML template for answer display
├── references/
│   └── question-bank.md                      # Copy for quick access
├── task1_charts/                             # Place Writing Task 1 chart images here
├── ielts_answers.html                        # Generated model answers (auto-updated)
├── CLAUDE.md                                 # Project documentation for Claude
└── README.md
```

## State Files (Auto-Generated)

After onboarding, these files manage your progress:

| File | Purpose |
|------|---------|
| `user_profile.json` | Exam date, target scores, personal info |
| `study_plan.json` | Day-by-day topic schedule |
| `progress.json` | Topics completed, answers generated, daily log |

## Topic Distribution Strategy

The agent ensures no topic repeats across sessions:

| Session Type | Topics per Session | Priority |
|-------------|-------------------|----------|
| Speaking-focused | 1-2 Part 1 + 1 Part 2&3 | Essential topics first, then new, then retained |
| Writing-focused | 1-2 essays (user-provided prompts) | Task 2 prioritized over Task 1 |
| Mixed | 1 Part 1 + 1 essay | Alternate speaking/writing each session |

## PDF Extraction

The question bank was extracted from the official 50-page IELTS speaking question bank PDF using:

1. **PyMuPDF** — Initial text extraction and topic identification
2. **[MinerU](https://github.com/opendatalab/MinerU)** (`npx skills add tanis90/pdf-converter-mineru`) — High-quality Chinese document conversion via `mineru-open-api flash-extract`

## Design Philosophy

- **Personalization over templates** — Generic answers are forgettable. Answers built around YOUR life are memorable.
- **Progressive disclosure** — The skill reveals topics day-by-day, never overwhelming you with all 102 topics at once.
- **Band-appropriate, not band-inflated** — A Band 6 answer that's authentic is better than a Band 8 answer that sounds like a dictionary.
- **Memorization-friendly** — Answers are concise, well-structured, and rich with highlighted expressions for quick pre-exam review.

## Contributing

This is a personal preparation tool, but improvements are welcome:
- Report topic inaccuracies or missing questions
- Suggest HTML design improvements
- Add more sample answers for calibration

## License

MIT — Use freely for your IELTS preparation.

---

**Good luck on your IELTS exam! 🎯**
