<p align="center">
  <img src="https://img.shields.io/github/stars/RomainCHEN/ielts-coach?style=flat-square&color=yellow" alt="Stars">
  <img src="https://img.shields.io/github/license/RomainCHEN/ielts-coach?style=flat-square&color=blue" alt="License">
  <img src="https://img.shields.io/badge/version-v2.0-1a237e?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/题库-102个话题-ffc107?style=flat-square" alt="题库">
</p>

<h1 align="center">🎓 IELTS Coach</h1>
<h3 align="center">最懂你的雅思口语与写作 AI 教练</h3>

<p align="center">
  <strong>一个 Claude Code 技能，不只生成范文——<br>它先采访你，再用<em>你的声音</em>写作，并把每句话校准到<br>雅思官方评分标准。</strong>
</p>

<p align="center">
  <a href="README.md">🇬🇧 English</a>
</p>

---

## 📑 目录

- [🧠 有什么不同](#-有什么不同)
- [✨ 核心功能](#-核心功能)
- [⚡ 快速开始](#-快速开始)
- [🔄 工作流程](#-工作流程)
- [📁 项目结构](#-项目结构)
- [🎯 四维个性化引擎](#-四维个性化引擎)
- [👁️ 非视觉模型的视觉桥接](#%EF%B8%8F-非视觉模型的视觉桥接)
- [🤝 贡献](#-贡献)
- [📜 许可证](#-许可证)

---

## 🧠 有什么不同

大多数雅思 AI 工具是这样工作的：

```
你：  "帮我写一篇关于气候变化的大作文。"
AI：  [一篇250词、充满"Firstly, Secondly, In conclusion"的通用范文]
```

**IELTS Coach 是这样工作的：**

```
助手："在你回答之前，我想了解你对此的真实看法。"
      [5分钟迷你访谈：挖掘经历、回忆、观点]
助手："让我确认一下。你提到……我围绕这个核心来写，对吗？"
你：  "对，但补充一点 Z。"
助手：[以你的口吻打磨的范文，分数匹配，零 AI 味]
```

| | 通用 AI 工具 | IELTS Coach |
|---|---|---|
| 个性化程度 | "Some people believe..." 模糊立场 | "当我在[你的公司]工作时……" 具体经历 |
| AI 检测风险 | 高（破折号、套话、机械连接） | 几乎为零（自然衔接、真人语感） |
| 可记忆性 | 很难记住，因为内容不是你自己的 | 容易——它本身就是你，只是更精致 |
| 评分对齐 | 随机 | 对照官方评分表逐 band 校准 |
| 视觉支持 | 依赖模型 | 任意模型可用（含 DeepSeek），通过 MCP 桥接 |
| 话题挖掘 | 无 | 每个话题5步结构化访谈 |

---

## ✨ 核心功能

<table>
<tr>
  <td width="48"><strong>🎯</strong></td>
  <td><strong>渐进式话题挖掘</strong><br>入门引导只是开始。每接触一个新话题——无论是"描述一部法律"还是"最喜欢的童年回忆"——助手都会先进行结构化迷你访谈，从<em>你的</em>生活中挖掘具体经历、观点和感受，然后才动笔。102个话题，102份个性化答案。</td>
</tr>
<tr>
  <td width="48"><strong>📋</strong></td>
  <td><strong>官方评分标准对齐</strong><br>写作答案依据官方 IELTS Writing Band Descriptors（2023年5月更新版）四大维度校准：任务回应、连贯与衔接、词汇丰富度、语法多样性与准确性。每个维度精确对应目标分数。</td>
</tr>
<tr>
  <td width="48"><strong>🚫</strong></td>
  <td><strong>去 AI 味强制筛查</strong><br>显式筛查并消除 AI 痕迹：不用破折号、不堆砌"not only... but also..."、不用"Firstly/Secondly/Finally"机械连接、不说"This essay will discuss..."。输出读起来像真人写作。</td>
</tr>
<tr>
  <td width="48"><strong>👁️</strong></td>
  <td><strong>非视觉模型视觉桥接</strong><br>用 DeepSeek？agent 看不到图表。内置 MCP 服务器通过阿里云百炼免费 qwen-vl 模型（或任意你选的服务商）代理图像分析。agent 自动完成全部配置——你只需提供 API key。</td>
</tr>
<tr>
  <td width="48"><strong>🖼️</strong></td>
  <td><strong>精美 HTML 输出</strong><br>响应式、可打印、可导航。高亮词汇、结构笔记、一键复制。海军蓝 + 金色雅思主题设计。</td>
</tr>
<tr>
  <td width="48"><strong>🔄</strong></td>
  <td><strong>自进化学习计划</strong><br>错过的课程自动重新安排，薄弱环节优先，跨会话追踪进度。102个话题不重复（除非你要求）。</td>
</tr>
</table>

---

## ⚡ 快速开始

```bash
# 1. 克隆
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach

# 2. 将技能复制到你的项目（或直接使用此仓库）
cp -r .claude/skills/ielts-coach /path/to/your-project/.claude/skills/

# 3. 启动 Claude Code，直接说话——技能自动触发
```

> 💡 **无需额外配置。** 说"开始我的雅思备考"，助手自动处理一切。入门引导 → 学习计划 → 每日话题挖掘 → 范文输出至 HTML 页面。

**深度求索 / 非视觉模型用户：** 第一次读取图表图片失败时，agent 自动引导你完成 2 分钟的视觉桥接配置。你只需提供一个 API key。

---

## 🔄 工作流程

```
┌──────────────────────────────────────────────────────────┐
│                   首次会话                                 │
│  入门引导 → 生成学习计划 → 准备就绪                        │
│  （5分钟：考试日期、目标分数、背景信息、时间安排）            │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────┐
│                   每次会话                                 │
│                                                          │
│  欢迎回来 + 进度概览                                       │
│       │                                                  │
│       ▼                                                  │
│  ┌─────────────────────────────────┐                     │
│  │  话题挖掘对话（每个话题都走一遍）  │  ← 核心差异          │
│  │  A: 话题引入                    │                     │
│  │  B: 经验挖掘                    │                     │
│  │  C: 内容确认                    │                     │
│  │  D: 生成范文                    │                     │
│  └─────────────────────────────────┘                     │
│       │                                                  │
│       ▼                                                  │
│  范文（你的故事、你的口吻）                                  │
│  + 高亮词汇表达                                            │
│  + 分数匹配校准                                            │
│  + 去 AI 味检查                                           │
│       │                                                  │
│       ▼                                                  │
│  保存至 ielts_answers.html                                │
│  更新进度 → 明天见！                                       │
└──────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
ielts-coach/
├── .claude/skills/ielts-coach/
│   ├── SKILL.md                              # 完整助手行为指令（约 700 行）
│   ├── references/
│   │   ├── question-bank.md                  # Part 1 + P2&3 新题（38+29）
│   │   ├── question_bank_complete.json       # P2&3 保留题 + 非大陆题（27+8）
│   │   ├── band-descriptors.md               # 口语评分标准
│   │   ├── writing-band-descriptors.md       # 官方写作评分标准（2023年5月）
│   │   ├── writing-resources.md              # Task 1 图表语言 + Task 2 模板
│   │   └── sample-answers.md                 # 质量校准范文
│   ├── scripts/
│   │   ├── state_manager.py                  # JSON 状态管理
│   │   ├── build_complete_bank.py            # 题库构建工具
│   │   └── vision_mcp_server.py             # MCP 视觉桥接（DeepSeek → qwen-vl）
│   └── assets/
│       └── answer_template.html              # 答案渲染 HTML 模板
├── README.md                                 # 英文版
├── README_zh.md                              # ← 你在这里
├── LICENSE                                   # MIT
└── .gitignore
```

> ⚡ **这就是完整仓库。** 放入任意 Claude Code 项目即可使用。运行时的状态文件（`user_profile.json`、`study_plan.json`、`progress.json`、`ielts_answers.html`）在你自己的项目根目录下——本仓库不追踪这些文件。

---

## 🎯 四维个性化引擎

IELTS Coach 同时在四个维度上个性化——这是任何静态模板做不到的：

| 维度 | 来源 | 示例 |
|---|---|---|
| **1. 个人身份** | 入门引导 | "作为一名在深圳的软件工程师……" |
| **2. 话题相关经历** | 话题挖掘访谈 | "当我凌晨三点调试那个生产环境故障时……" |
| **3. 目标分数校准** | 用户目标分数 | Band 7 词汇密度，灵活的衔接手段 |
| **4. 真人语感保留** | 谈话中捕捉的用户原始表达 | 用户的幽默感、文化背景、句式节奏 |

**效果：** 一份在雅思评分表上得分高，且考试压力下你能真正记住的答案。

---

## 👁️ 非视觉模型的视觉桥接

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  你的图表     │────▶│  vision_bridge    │────▶│  qwen-vl-plus    │
│  (PNG/JPG)   │     │  (MCP 服务器)     │     │  (免费额度)       │
└──────────────┘     └──────────────────┘     └────────┬────────┘
                                                        │
                                              ┌─────────▼─────────┐
                                              │  结构化文字描述       │
                                              │  （图表类型、数据等）  │
                                              └─────────┬─────────┘
                                                        │
┌──────────────┐     ┌──────────────────┐              │
│  Task 1      │◀────│  你的 Agent       │◀─────────────┘
│  范文         │     │  (DeepSeek等)     │
└──────────────┘     └──────────────────┘
```

**一次性配置（agent 全自动完成）：** pip install → settings.json → 重启。你只需提供：百炼 API key。

也支持自定义服务商——任意 OpenAI 兼容的视觉模型接口均可。

---

## 🤝 贡献

为个人雅思考生设计，但欢迎改进：

- 反馈话题不准确或缺失的题目
- 建议 HTML 设计改进
- 分享校准范文扩充参考库
- 报告遗漏的 AI 味儿模式

提 Issue 或 PR 即可。

---

## 📜 许可证

MIT © [Romain Chen](https://github.com/RomainCHEN) — 自由使用、自由修改，祝你考试顺利。

---

<p align="center">
  <sub>为 2026年5-8月 雅思季打造 · 102 个口语话题 · 口语 + 写作</sub>
  <br>
  <sub>由理解雅思备考压力的人用心制作 ❤️</sub>
</p>
