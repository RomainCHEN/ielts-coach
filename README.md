<h1 align="center">🎓 IELTS Coach</h1>
<h3 align="center">The Most Personalized IELTS Speaking & Writing AI Coach</h3>

<p align="center">
  <img src="https://img.shields.io/github/stars/RomainCHEN/ielts-coach?style=flat-square&color=yellow" alt="Stars">
  <img src="https://img.shields.io/github/license/RomainCHEN/ielts-coach?style=flat-square&color=blue" alt="License">
  <img src="https://img.shields.io/badge/version-v2.0-1a237e?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/topics-102-ffc107?style=flat-square" alt="Topics">
</p>

<p align="center">
  <strong>An AI agent skill that interviews you first, writes in <em>your</em> voice,<br>and calibrates every sentence to official IELTS band descriptors.</strong>
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
User: Write me an essay about climate change.
AI:   [Generates a 250-word essay full of Firstly, Secondly, In conclusion]
```

**IELTS Coach works like this:**

```
Coach: Before I write anything, what is YOUR take on this topic?
       [5-minute mini-interview: mines memories, opinions, personal examples]
Coach: Let me make sure I have this right. You believe X because of
       your experience with Y. I will build your answer around that.
User:  Yes, and also mention Z.
Coach: [Polished essay IN THE USER'S VOICE, band-calibrated, zero AI flavor]
```

| | Generic AI | IELTS Coach |
|---|---|---|
| Personalization | Vague references to some people or society | Specific: When I was working at [your company]... |
| AI detection risk | High (dashes, clichés, mechanical linkers) | Near-zero (natural cohesion, human voice) |
| Memorability | Hard to remember because it is not yours | Easy: it literally IS you, just polished |
| Scoring alignment | Random | Calibrated to official IELTS descriptors per band |
| Vision support | Depends on model | Works on any model (DeepSeek included) via MCP bridge |
| Topic discovery | None | Structured interview per topic, covering all 102 |

---

## ✨ Features

<table>
<tr>
  <td width="48"><strong>🎯</strong></td>
  <td><strong>Progressive Topic Discovery</strong><br>Not just onboarding. Every new topic triggers a structured mini-interview. The agent mines <em>your</em> specific memories, opinions, and experiences before writing a single word. 102 topics, 102 personalized answers.</td>
</tr>
<tr>
  <td width="48"><strong>📋</strong></td>
  <td><strong>Official Band Descriptor Alignment</strong><br>Writing answers calibrated against the public IELTS Writing Band Descriptors (updated May 2023). Task Response, Coherence and Cohesion, Lexical Resource, and Grammatical Range and Accuracy. All four criteria tuned to your target band.</td>
</tr>
<tr>
  <td width="48"><strong>🚫</strong></td>
  <td><strong>Anti-AI-Flavor Enforcement</strong><br>Explicitly screens for and eliminates AI patterns: no em dashes, no scare quotes, no mechanical linkers like Firstly/Secondly/Finally, no This essay will discuss clichés. Reads like polished human writing.</td>
</tr>
<tr>
  <td width="48"><strong>👁️</strong></td>
  <td><strong>Vision Bridge for Non-Vision Models</strong><br>Running on DeepSeek? Your agent cannot see charts. The included MCP server proxies images through Alibaba Cloud Bailian's free qwen-vl model, or any provider you choose. Agent auto-configures everything. You just provide the API key.</td>
</tr>
<tr>
  <td width="48"><strong>🖼️</strong></td>
  <td><strong>Beautiful HTML Output</strong><br>Responsive, printable, navigable. Highlighted vocabulary, structure notes, copy buttons. Navy and gold IELTS-themed design.</td>
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

# 2. Copy the skill into your agent's skill directory:
#    Claude Code:     cp -r ielts-coach /your-project/.claude/skills/
#    Other agents:    copy ielts-coach/ into whatever directory your agent uses for skills

# 3. Start your agent and just talk. The skill triggers automatically.
```

> 💡 **No configuration needed.** Say Start my IELTS preparation and the agent handles everything. Onboarding → Study Plan → Daily sessions with Topic Discovery → Model answers in HTML.

**For DeepSeek and non-vision model users:** The first time a chart image fails to load, the agent auto-guides you through the 2-minute Vision Bridge setup. You only provide an API key.

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
├── SKILL.md                              # Complete agent behavior (~700 lines)
├── references/
│   ├── question-bank.md                  # Part 1 + P2&3 New topics (38+29)
│   ├── question_bank_complete.json       # P2&3 Retained + Non-mainland (27+8)
│   ├── band-descriptors.md               # Speaking criteria by band
│   ├── writing-band-descriptors.md       # Official Writing descriptors (May 2023)
│   ├── writing-resources.md              # Task 1 chart language + Task 2 templates
│   └── sample-answers.md                 # Quality calibration examples
├── scripts/
│   ├── state_manager.py                  # JSON state file management
│   ├── build_complete_bank.py            # Question bank builder
│   └── vision_mcp_server.py             # MCP vision bridge (DeepSeek → qwen-vl)
└── assets/
    └── answer_template.html              # HTML template for answer rendering
```

> ⚡ **Copy the `ielts-coach/` folder into your agent's skill directory. That is it.** Runtime state files (`user_profile.json`, `study_plan.json`, `progress.json`, `ielts_answers.html`) are auto-generated in your project root and never tracked here.

---

## 🎯 The 4D Personalization Engine

IELTS Coach personalizes on 4 dimensions simultaneously. No static template can do this.

| Dimension | Source | Example |
|---|---|---|
| **1. Personal Identity** | Onboarding | As a software engineer in Shenzhen... |
| **2. Topic-Specific Experience** | Topic Discovery interview | When I was debugging that production outage at 3am... |
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

Supports custom providers too. Any OpenAI-compatible vision endpoint works.

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

MIT © [Romain Chen](https://github.com/RomainCHEN). Use freely, modify freely. Good luck on your exam.

---

<p align="center">
  <sub>Built for IELTS May–August 2026 season · 102 speaking topics · Speaking + Writing</sub>
  <br>
  <sub>Made with ❤️ by someone who knows how stressful IELTS prep can be</sub>
</p>
