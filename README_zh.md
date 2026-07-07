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
| 🗣️ **渐进式话题挖掘** | 通用背景只是开始。每接触一个新话题——无论是"描述一部法律"还是"一段童年回忆"——助手都会先进行结构化迷你访谈，从*你的*生活中挖掘具体经历、观点和感受，然后才动笔生成。答案源自*你的*真实内容，而非模板。 |
| 📝 **分数匹配答案** | 词汇密度、句式结构和衔接手段自动校准至目标分数（6 / 7 / 8），润色的是你的想法，不是替代你说话。 |
| 📋 **官方评分标准对齐** | 写作答案依据官方 IELTS Writing Band Descriptors（2023年5月更新版）四大维度校准：任务回应、连贯与衔接、词汇丰富度、语法多样性与准确性。 |
| 🚫 **去 AI 味** | 写作范文经过显式筛查，杜绝 AI 痕迹——不用破折号、不堆砌"not only... but also..."、不用机械的"Firstly/Secondly/Finally"、不说"This essay will discuss..."。输出读起来像真人写作，不像机器生成。 |
| 🖼️ **HTML 输出** | 所有答案渲染为响应式、可打印的网页，包含高亮词汇、结构笔记和一键复制。 |
| 🔄 **计划自进化** | 动态调整：重新安排错过的课程、优先薄弱环节、未经同意绝不重复话题。 |
| ✍️ **图表分析** | 将 Task 1 图表图片放入 `task1_charts/`，助手自动分析并生成范文。 |
| 👁️ **视觉桥接** | 使用 DeepSeek 等不支持图像识别的模型？技能内置 MCP 服务器，可通过阿里云百炼免费 qwen-vl 模型（或你自己的服务商）代理图像分析。图表读取失败时，助手会引导你完成一次性配置，不让你卡住。 |

## 🚀 快速开始

```bash
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach
```

在 Claude Code 中提到雅思相关内容，技能会自动触发：

> "开始我的雅思备考" · "今天练习口语 Part 2" · "我有一个写作题目…"

**首次会话** → 入门引导（考试日期、目标分数、个人背景）。**之后的每次会话** → 每个新话题先进行话题挖掘对话 → 生成个性化范文 → 渲染至 `ielts_answers.html`。

## 📁 项目结构

```
.claude/skills/ielts-coach/
├── SKILL.md                              # 助手行为指令 + 完整工作流
├── references/
│   ├── question-bank.md                  # Part 1 + P2&3 新题
│   ├── question_bank_complete.json       # P2&3 保留题 + 非大陆题
│   ├── band-descriptors.md               # 口语评分标准
│   ├── writing-band-descriptors.md       # 官方写作评分标准（Task 1 & 2, Bands 5-9）
│   ├── writing-resources.md              # Task 1 图表语言 + Task 2 模板
│   └── sample-answers.md                 # 校准范文
├── scripts/
│   ├── state_manager.py                  # JSON 状态文件管理
│   ├── build_complete_bank.py            # 题库构建工具
│   └── vision_mcp_server.py             # MCP 视觉桥接（非视觉模型使用）
└── assets/
    └── answer_template.html              # 答案展示 HTML 模板
```

> **💡 将 `.claude/skills/ielts-coach/` 复制到你自己的项目中即可使用。** 技能会在你的项目根目录下自动创建状态文件（`user_profile.json`、`study_plan.json`、`progress.json`、`ielts_answers.html`）——这些文件不会被本仓库追踪。

## 🧠 设计理念

| 原则 | 含义 |
|---|---|
| **渐进式个性化** | 通用背景只是起点。每个新话题触发一次迷你访谈，挖掘*与这个话题相关*的具体经历。 |
| **润色而非替代** | 助手将*你的*原始想法提升到分数匹配的英语水平，你的声音、你的回忆、你的观点始终保留。 |
| **便于记忆** | 围绕自身经历构建的答案，在考试压力下更容易自然回忆。 |
| **官方标准写作** | 所有写作输出依据公开的 IELTS Writing Band Descriptors 校准。四个评分维度各 Band 6→7→8 的进阶路径在范文中有明确体现。 |
| **真人写作，非机器生成** | 范文显式去 AI 化：自然衔接替代机械连接词、直接立场替代模棱两可、你已有的词汇被提升而非被生词表轰炸。 |

## 📜 许可证

MIT — 自由用于雅思备考。

---

<p align="center">祝你考试顺利！🎯</p>
