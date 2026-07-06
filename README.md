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
| 🗣️ **Topic Discovery** | Before each topic, the agent interviews you about *your* experiences, memories, and opinions. Your answer starts from *your* content. |
| 📝 **Band-Calibrated** | Vocabulary, sentence complexity, and cohesion match your target band (6 / 7 / 8). Polished, not overwritten. |
| 🖼️ **HTML Output** | Every answer is rendered to a responsive, printable page with highlighted expressions and copy buttons. |
| 🔄 **Self-Evolving** | The plan adapts — missed sessions are rescheduled, weak areas get priority, topics never repeat without your consent. |
| ✍️ **Charts** | Drop Task 1 chart images into `task1_charts/` and the agent analyzes them for you. |

## 🚀 Quick Start

```bash
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach
```

The skill triggers automatically when you mention IELTS in Claude Code:

> "Start my IELTS preparation" · "Practice speaking Part 2 today" · "I have a writing question…"

**First session** → onboarding. **Daily sessions** → Topic Discovery + model answers → `ielts_answers.html`.

## 📁 Structure

```
ielts-coach/
├── .claude/skills/ielts-coach/
│   ├── SKILL.md                         # Agent behavior
│   ├── references/
│   │   ├── question-bank.md             # Part 1 + P2&3 New topics
│   │   ├── question_bank_complete.json  # P2&3 Retained + Non-mainland
│   │   ├── band-descriptors.md          # IELTS scoring criteria
│   │   ├── writing-resources.md         # Task 1 language + Task 2 templates
│   │   └── sample-answers.md            # Calibrated examples
│   ├── scripts/                         # State manager + bank builder
│   └── assets/                          # HTML template
├── task1_charts/                        # ← Drop your chart images here
├── ielts_answers.html                   # Auto-generated answers
└── README.md
```

## 🧠 Philosophy

| Principle | Meaning |
|---|---|
| **Progressive Personalization** | General background is only the start. Every new topic triggers a mini-interview. |
| **Polish, Don't Replace** | The agent elevates *your* raw thoughts to band-appropriate English. Your voice stays. |
| **Memorization-Friendly** | Answers built around your own experiences are far easier to recall under exam pressure. |
| **Band-Appropriate, Not Inflated** | An authentic Band 6 answer beats a Band 8 answer that sounds like a dictionary. |

## 📜 License

MIT — use freely for your IELTS preparation.

---

<p align="center">Good luck on your exam! 🎯</p>
