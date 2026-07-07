<p align="center">
  <a href="README.md">🇬🇧 English</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="README_zh.md">🇨🇳 简体中文</a>
</p>

---

<h1 align="center">🎓 IELTS Coach</h1>
<h3 align="center">Speaking &amp; Writing AI Preparation Agent</h3>

<p align="center">
  <em>A deeply personalized <a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> skill that generates IELTS model answers <strong>in your voice</strong>.</em>
</p>

<p align="center">
  <strong>📅 May–Aug 2026</strong> &nbsp;·&nbsp;
  <strong>102 topics</strong> &nbsp;·&nbsp;
  <strong>Speaking + Writing</strong> &nbsp;·&nbsp;
  <strong>HTML output</strong>
</p>

---

## ✨ What It Does

| | |
|---|---|
| 🎯 **Personalized Study Plan** | Onboarding captures your exam date, target scores, and schedule. A day-by-day plan is built automatically. |
| 🗣️ **Progressive Topic Discovery** | General background is only the start. For every new topic — whether it's "describe a law" or "your favorite childhood memory" — the agent conducts a structured mini-interview to mine *your* specific experiences, memories, and opinions before generating anything. Your answer starts from *your* content, not a template. |
| 📝 **Band-Calibrated Answers** | Vocabulary, sentence complexity, and cohesion are calibrated to your target band (6 / 7 / 8) — polishing your raw thoughts, not overwriting them. |
| 📋 **Official Scoring Alignment** | Writing answers are calibrated against the official IELTS Writing Band Descriptors (updated May 2023) across all four criteria: Task Response, Coherence & Cohesion, Lexical Resource, and Grammatical Range & Accuracy. |
| 🚫 **Human-Writer Test** | Writing answers are explicitly screened against AI-detection patterns — no em dashes, no "not only... but also..." overuse, no mechanical "Firstly/Secondly/Finally" chains, no "This essay will discuss..." clichés. The output reads like polished human writing, not generated text. |
| 🖼️ **HTML Output** | Every answer rendered to a responsive, printable page with highlighted expressions, structure notes, and copy buttons. |
| 🔄 **Self-Evolving Plan** | The plan adapts — missed sessions are rescheduled, weak areas get priority, topics never repeat without your consent. |
| ✍️ **Task 1 Charts** | Drop chart images into `task1_charts/` and the agent analyzes them for you. |
| 👁️ **Vision Bridge** | Running on DeepSeek or a non-vision model? The skill includes an MCP server that proxies image analysis through Alibaba Cloud Bailian's free qwen-vl model (or your own provider). When chart reading fails, the agent guides you through a one-time setup instead of leaving you stuck. |

## 🚀 Quick Start

```bash
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach
```

The skill triggers automatically when you mention IELTS in Claude Code:

> "Start my IELTS preparation" · "Practice speaking Part 2 today" · "I have a writing question…"

**First session** → onboarding (exam date, target scores, personal background). **Every session thereafter** → Topic Discovery conversation for each new topic → personalized model answers → rendered to `ielts_answers.html`.

## 📁 Structure

```
.claude/skills/ielts-coach/
├── SKILL.md                              # Agent behavior + full workflow
├── references/
│   ├── question-bank.md                  # Part 1 + P2&3 New topics
│   ├── question_bank_complete.json       # P2&3 Retained + Non-mainland
│   ├── band-descriptors.md               # Speaking band criteria
│   ├── writing-band-descriptors.md       # Official Writing descriptors (Task 1 & 2, Bands 5-9)
│   ├── writing-resources.md              # Task 1 chart language + Task 2 templates
│   └── sample-answers.md                 # Calibrated examples
├── scripts/
│   ├── state_manager.py                  # JSON state file management
│   ├── build_complete_bank.py            # Question bank builder
│   └── vision_mcp_server.py             # MCP vision bridge for non-vision models
└── assets/
    └── answer_template.html              # HTML template for answer display
```

> **💡 Just copy `.claude/skills/ielts-coach/` into your own project.** The skill reads and writes state files (`user_profile.json`, `study_plan.json`, `progress.json`, `ielts_answers.html`) in your project root — none of which are tracked in this repo.

## 🧠 Philosophy

| Principle | Meaning |
|---|---|
| **Progressive Personalization** | General background is only the start. Every new topic triggers a mini-interview to mine *that specific* experience from your life. |
| **Polish, Don't Replace** | The agent elevates *your* raw thoughts to band-appropriate English. Your voice, your memories, your opinions. |
| **Memorization-Friendly** | Answers built around your own experiences are far easier to recall under exam pressure. |
| **Official-Standard Writing** | All writing output is calibrated against the public IELTS Writing Band Descriptors. Band 6→7→8 progression is tracked separately for each of the four scoring criteria. |
| **Human, Not AI** | Model essays are explicitly de-AI-ized: natural cohesion instead of mechanical linkers, direct opinions instead of hedging, your vocabulary elevated instead of a thesaurus dump. |

## 📜 License

MIT — use freely for your IELTS preparation.

---

<p align="center">Good luck on your exam! 🎯</p>
