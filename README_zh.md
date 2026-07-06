<p align="center">
  <a href="README.md">🇬🇧 English</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="README_zh.md">🇨🇳 简体中文</a>
</p>

---

<h1 align="center">🎓 IELTS Coach</h1>
<h3 align="center">雅思口语与写作 AI 备考助手</h3>

<p align="center">
  <em>一个深度个性化的 <a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> 技能，<strong>以你的口吻</strong>生成雅思范文答案。</em>
</p>

<p align="center">
  <strong>📅 2026年5–8月</strong> &nbsp;·&nbsp;
  <strong>102个话题</strong> &nbsp;·&nbsp;
  <strong>口语 + 写作</strong> &nbsp;·&nbsp;
  <strong>HTML 输出</strong>
</p>

---

## ✨ 核心功能

| | |
|---|---|
| 🎯 **个性化学习计划** | 入门引导收集考试日期、目标分数和可用时间，自动生成每日学习安排。 |
| 🗣️ **话题挖掘对话** | 每个话题生成前，助手会引导你回忆*自己的*经历、观点和感受——答案源自*你的*内容。 |
| 📝 **分数匹配** | 词汇密度、句式结构和衔接手段自动匹配目标分数（6 / 7 / 8）。润色你的想法，而非替代。 |
| 🖼️ **HTML 输出** | 所有答案渲染为响应式、可打印的网页，包含高亮词汇和一键复制。 |
| 🔄 **计划自进化** | 动态调整：重新安排错过的课程、优先薄弱环节、未经同意绝不重复话题。 |
| ✍️ **图表分析** | 将 Task 1 图表图片放入 `task1_charts/`，助手自动分析并生成范文。 |

## 🚀 快速开始

```bash
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach
```

在 Claude Code 中提到雅思相关内容，技能会自动触发：

> "开始我的雅思备考" · "今天练习口语 Part 2" · "我有一个写作题目…"

**首次会话** → 入门引导。**每日会话** → 话题挖掘对话 + 生成范文 → 保存至 `ielts_answers.html`。

## 📁 项目结构

```
ielts-coach/
├── .claude/skills/ielts-coach/
│   ├── SKILL.md                         # 助手行为指令
│   ├── references/
│   │   ├── question-bank.md             # Part 1 + P2&3 新题
│   │   ├── question_bank_complete.json  # P2&3 保留题 + 非大陆题
│   │   ├── band-descriptors.md          # 雅思评分标准
│   │   ├── writing-resources.md         # Task 1 图表语言 + Task 2 模板
│   │   └── sample-answers.md            # 校准范文
│   ├── scripts/                         # 状态管理 + 题库构建
│   └── assets/                          # HTML 模板
├── task1_charts/                        # ← 将图表图片放这里
├── ielts_answers.html                   # 自动生成的范文
└── README_zh.md
```

## 🧠 设计理念

| 原则 | 含义 |
|---|---|
| **渐进式个性化** | 通用背景只是起点。每个新话题触发一次迷你访谈，挖掘*与这个话题相关*的经历。 |
| **润色而非替代** | 助手将*你的*原始想法提升到分数匹配的英语水平，你的声音始终保留。 |
| **便于记忆** | 围绕自身经历构建的答案，在考试压力下更容易自然回忆。 |
| **分数匹配不虚高** | 一个真实自然的 Band 6 答案，远胜于听起来像词典的 Band 8 答案。 |

## 📜 许可证

MIT — 自由用于雅思备考。

---

<p align="center">祝你考试顺利！🎯</p>
