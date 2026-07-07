<p align="center">
  <picture>
    <img src="https://img.shields.io/badge/May--Aug_2026-IELTS-blue?style=for-the-badge&logo=ielts&logoColor=white" alt="Season">
  </picture>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/RomainCHEN/ielts-coach?style=flat-square&color=yellow" alt="Stars">
  <img src="https://img.shields.io/github/license/RomainCHEN/ielts-coach?style=flat-square&color=blue" alt="License">
  <img src="https://img.shields.io/badge/version-v2.0-1a237e?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/topics-102-ffc107?style=flat-square" alt="Topics">
  <img src="https://img.shields.io/badge/skills-Claude%20Code-orange?style=flat-square" alt="Claude Code">
</p>

<h1 align="center">🎓 IELTS Coach</h1>
<h3 align="center">The Most Personalized IELTS Speaking & Writing AI Coach</h3>

<p align="center">
  <strong>A Claude Code skill that doesn't just generate model answers —<br>it interviews you first, writes in <em>your</em> voice, and calibrates every sentence<br>to official IELTS band descriptors.</strong>
</p>

<p align="center">
  <a href="README_zh.md">🇨🇳 简体中文</a>
</p>

---

## 📑 Table of Contents

- [🧠 What Makes This Different](#-what-makes-this-different)
- [✨ Features](#-features)
- [⚡ Quick Start](#-quick-start)
- [🔄 The Workflow](#-the-workflow)
- [📁 Project Structure](#-project-structure)
- [🎯 The 4D Personalization Engine](#-the-4d-personalization-engine)
- [👁️ Vision Bridge for Non-Vision Models](#%EF%B8%8F-vision-bridge-for-non-vision-models)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🧠 What Makes This Different

Most IELTS AI tools work like this:

```
User: "Write me an essay about climate change."
AI:   [Generic 250-word essay with "Firstly, Secondly, In conclusion"]
```

**IELTS Coach works like this:**

```
Agent: "Before I write anything — what's YOUR take on this topic?"
       [5-minute mini-interview: mines memories, opinions, personal examples]
Agent: "Let me summarize what I've captured. You believe X because of your
       experience with Y. I'll build your answer around that. Sound right?"
User:  "Yes, but also mention Z."
Agent: [Polished essay IN THE USER'S VOICE, band-calibrated, zero AI flavor]
```

| | Generic AI | IELTS Coach |
|---|---|---|
| Personalization | Vague "some people believe..." | Specific: "When I was working at [your company]..." |
| AI detection risk | High (dashes, clichés, mechanical linkers) | Near-zero (natural cohesion, human voice) |
| Memorability | Hard to remember because it's not yours | Easy — it literally IS you, just polished |
| Scoring alignment | Random | Calibrated to official IELTS descriptors per band |
| Vision support | Depends on model | Works on ANY model (DeepSeek included) via MCP bridge |
| Topic discovery | None | Structured 5-step interview per topic |

---

## ✨ Features

<table>
<tr>
  <td width="48"><strong>🎯</strong></td>
  <td><strong>Progressive Topic Discovery</strong><br>Not just onboarding. Every new topic triggers a structured mini-interview — the agent mines <em>your</em> specific memories, opinions, and experiences before writing a single word. 102 topics, 102 personalized answers.</td>
</tr>
<tr>
  <td width="48"><strong>📋</strong></td>
  <td><strong>Official Band Descriptor Alignment</strong><br>Writing answers calibrated against the public IELTS Writing Band Descriptors (updated May 2023). Task Response, Coherence & Cohesion, Lexical Resource, and Grammatical Range & Accuracy — all four criteria tuned to your target band.</td>
</tr>
<tr>
  <td width="48"><strong>🚫</strong></td>
  <td><strong>Anti-AI-Flavor Enforcement</strong><br>Explicitly screens for and eliminates AI patterns: no em dashes, no scare quotes, no "not only... but also..." repetition, no "Firstly/Secondly/Finally" chains, no "This essay will discuss..." clichés. Reads like polished human writing.</td>
</tr>
<tr>
  <td width="48"><strong>👁️</strong></td>
  <td><strong>Vision Bridge for Non-Vision Models</strong><br>Running on DeepSeek? Your agent can't see charts. The included MCP server proxies images through Alibaba Cloud Bailian's free qwen-vl model (or any provider you choose). Agent auto-configures everything — you just provide the API key.</td>
</tr>
<tr>
  <td width="48"><strong>🖼️</strong></td>
  <td><strong>Beautiful HTML Output</strong><br>Responsive, printable, navigable. Highlighted vocabulary, structure notes, copy buttons. Navy + gold IELTS-themed design.</td>
</tr>
<tr>
  <td width="48"><strong>🔄</strong></td>
  <td><strong>Self-Evolving Study Plan</strong><br>Reschedules missed sessions, prioritizes weak areas, tracks progress across sessions via JSON state files. 102 topics never repeat unless you ask.</td>
</tr>
</table>

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach

# 2. Copy the skill into your project (or use this repo directly)
cp -r .claude/skills/ielts-coach /path/to/your-project/.claude/skills/

# 3. Start Claude Code and just talk — the skill triggers automatically
```

> 💡 **No configuration needed.** Say "Start my IELTS preparation" and the agent handles everything. Onboarding → Study Plan → Daily sessions with Topic Discovery → Model answers in HTML.

**For DeepSeek / non-vision model users:** The first time a chart image fails to load, the agent auto-guides you through the 2-minute Vision Bridge setup. You only provide an API key.

---

## 🔄 The Workflow

```
┌──────────────────────────────────────────────────────────┐
│                   FIRST SESSION                           │
│  Onboarding → Study Plan → Ready                         │
│  (5 min: exam date, target score, background, schedule)   │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────┐
│                   EVERY SESSION                           │
│                                                          │
│  Greet + progress summary                                │
│       │                                                  │
│       ▼                                                  │
│  ┌─────────────────────────────┐                         │
│  │  TOPIC DISCOVERY (per topic) │  ← The secret sauce    │
│  │  Stage A: Priming           │                         │
│  │  Stage B: Experience Mining │                         │
│  │  Stage C: Content Confirm   │                         │
│  │  Stage D: Generate Answer   │                         │
│  └─────────────────────────────┘                         │
│       │                                                  │
│       ▼                                                  │
│  Model answer (your voice, your stories)                 │
│  + Highlighted expressions                               │
│  + Band-specific calibration                             │
│  + Anti-AI-flavor check                                  │
│       │                                                  │
│       ▼                                                  │
│  Save to ielts_answers.html                              │
│  Update progress → See you tomorrow                      │
└──────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ielts-coach/
├── .claude/skills/ielts-coach/
│   ├── SKILL.md                              # Complete agent behavior (~700 lines)
│   ├── references/
│   │   ├── question-bank.md                  # Part 1 + P2&3 New topics (38+29)
│   │   ├── question_bank_complete.json       # P2&3 Retained + Non-mainland (27+8)
│   │   ├── band-descriptors.md               # Speaking criteria by band
│   │   ├── writing-band-descriptors.md       # Official Writing descriptors (May 2023)
│   │   ├── writing-resources.md              # Task 1 chart language + Task 2 templates
│   │   └── sample-answers.md                 # Quality calibration examples
│   ├── scripts/
│   │   ├── state_manager.py                  # JSON state file management
│   │   ├── build_complete_bank.py            # Question bank builder
│   │   └── vision_mcp_server.py             # MCP vision bridge (DeepSeek → qwen-vl)
│   └── assets/
│       └── answer_template.html              # HTML template for answer rendering
├── README.md                                 # ← You are here
├── README_zh.md                              # 中文版
├── LICENSE                                   # MIT
└── .gitignore
```

> ⚡ **This is the complete repo.** Drop it into any Claude Code project. The agent reads/writes runtime state (`user_profile.json`, `study_plan.json`, `progress.json`, `ielts_answers.html`) in your project root — none of which are tracked here.

---

## 🎯 The 4D Personalization Engine

IELTS Coach personalizes on 4 dimensions simultaneously — something no static template can do:

| Dimension | Source | Example |
|---|---|---|
| **1. Personal Identity** | Onboarding | "As a software engineer in Shenzhen..." |
| **2. Topic-Specific Experience** | Topic Discovery interview | "When I was debugging that production outage at 3am..." |
| **3. Target Band Calibration** | User's target score | Band 7 vocabulary density, flexible cohesive devices |
| **4. Human Voice Preservation** | User's raw language during Discovery | Their humor, their cultural references, their sentence rhythm |

**Result:** An answer that scores well on IELTS rubrics AND the user can actually remember under exam pressure.

---

## 👁️ Vision Bridge for Non-Vision Models

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Your Chart  │────▶│  vision_bridge    │────▶│  qwen-vl-plus    │
│  (PNG/JPG)   │     │  (MCP Server)     │     │  (Free tier)     │
└──────────────┘     └──────────────────┘     └────────┬────────┘
                                                        │
                                              ┌─────────▼─────────┐
                                              │  Structured text   │
                                              │  chart description │
                                              └─────────┬─────────┘
                                                        │
┌──────────────┐     ┌──────────────────┐              │
│  Task 1      │◀────│  Your Agent      │◀─────────────┘
│  Model Answer│     │  (DeepSeek, etc.) │
└──────────────┘     └──────────────────┘
```

**One-time setup (agent does everything):** pip install → settings.json → restart. Only input needed: your Bailian API key.

Supports custom providers too — any OpenAI-compatible vision endpoint.

---

## 🤝 Contributing

This is a personal exam preparation tool, but improvements are warmly welcome:

- Report topic inaccuracies or missing questions
- Suggest HTML design improvements
- Share calibrated sample answers for the reference pool
- Report AI-flavor patterns that slipped through

Open an issue or PR.

---

## 📜 License

MIT © [Romain Chen](https://github.com/RomainCHEN) — use freely, modify freely, good luck on your exam.

---

<p align="center">
  <sub>Built for IELTS May–August 2026 season · 102 speaking topics · Speaking + Writing</sub>
  <br>
  <sub>Made with ❤️ by someone who knows how stressful IELTS prep can be</sub>
</p>
