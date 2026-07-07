<h1 align="center">🎓 IELTS Coach</h1>
<h3 align="center">最懂你的雅思口语与写作 AI 教练</h3>

<p align="center">
  <img src="https://img.shields.io/github/stars/RomainCHEN/ielts-coach?style=flat-square&color=yellow" alt="Stars">
  <img src="https://img.shields.io/github/license/RomainCHEN/ielts-coach?style=flat-square&color=blue" alt="License">
  <img src="https://img.shields.io/badge/version-v2.0-1a237e?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/题库-102个话题-ffc107?style=flat-square" alt="题库">
</p>

<p align="center">
  <strong>一个 AI agent 技能。先跟你聊几分钟，了解你怎么想、你有什么经历，<br>然后用你说话的方式帮你写出来。每句话都能在雅思评分表上找到对应。</strong>
</p>

<p align="center">
  <a href="README.md">🇬🇧 English</a>
</p>

---

## 📑 目录

- [🧠 跟别的工具有什么不一样](#-跟别的工具有什么不一样)
- [✨ 能干什么](#-能干什么)
- [⚡ 快速上手](#-快速上手)
- [🔄 是怎么工作的](#-是怎么工作的)
- [📁 文件结构](#-文件结构)
- [🎯 四个维度的个性化](#-四个维度的个性化)
- [👁️ DeepSeek 也能看图](#%EF%B8%8F-deepseek-也能看图)
- [🤝 一起完善](#-一起完善)
- [📜 许可](#-许可)

---

## 🧠 跟别的工具有什么不一样

大部分雅思 AI 工具是这样的：

```
你：  帮我写一篇关于气候变化的大作文。
AI：  [扔给你一篇套话连篇的250词范文，通篇 Firstly... Secondly... In conclusion]
```

**这个 Coach 是这样干的：**

```
教练：先不急着写，聊聊你怎么看这个话题？
      [聊个五分钟：挖你的真实经历、想法、身边的故事]
教练：好，我理一下。你其实想说的是……对吧？那我围绕这个来写。
你：  对，再加一句……
教练：[一篇你自己看着都觉得这说的就是我的范文，分数匹配，没有 AI 味儿]
```

| | 一般 AI 工具 | IELTS Coach |
|---|---|---|
| 有没有你自己的想法 | Some people believe... 不知道谁 believe | 我去年在XX公司上班的时候…… 就是你的故事 |
| 会不会被看出来是 AI 写的 | 大概率会（破折号、套话、机械过渡） | 基本不会（自然流畅，像真人写的） |
| 好不好背 | 难背，内容跟你没关系 | 好背：本来就是你说的话，只是帮你润色了一下 |
| 能不能对上评分标准 | 随缘 | 对着官方评分表一条一条校准 |
| 能不能看图 | 看你用的模型支持不支持 | 啥模型都能，包括 DeepSeek，靠 MCP 桥接 |
| 会不会先跟你聊 | 上来就写 | 每个话题先聊再写，102个话题不重样 |

---

## ✨ 能干什么

<table>
<tr>
  <td width="48"><strong>🎯</strong></td>
  <td><strong>别上来就写，先聊聊</strong><br>入门引导收集的那些背景只是基础。每碰到一个新话题，管它是描述一部法律还是你最难忘的一次旅行，教练都会先跟你聊几分钟，挖你的具体经历、真实想法、身边的故事。你的生活就是最好的素材。</td>
</tr>
<tr>
  <td width="48"><strong>📋</strong></td>
  <td><strong>对着官方评分标准写</strong><br>写作范文不是瞎写的。任务回应、连贯与衔接、词汇丰富度、语法多样性与准确性，这四个评分维度，每个都对着官方 Band Descriptors（2023年5月版）校准到你的目标分数。</td>
</tr>
<tr>
  <td width="48"><strong>🚫</strong></td>
  <td><strong>把 AI 味儿去掉</strong><br>专门检查并干掉那些一看就是 AI 写的痕迹：不用破折号，不用 not only... but also... 的堆砌，不用 Firstly... Secondly... Finally... 那种念稿子一样的过渡，不说 This essay will discuss... 之类的套话。读起来像正常人写的。</td>
</tr>
<tr>
  <td width="48"><strong>👁️</strong></td>
  <td><strong>DeepSeek 也能看图</strong><br>用 DeepSeek 的话 agent 读不了图表图片。没关系，内置了一个 MCP 服务器，把图片甩给阿里云百炼免费的 qwen-vl 模型去看，看完告诉你图上有什么。全程 agent 自己配好，你只需要给一个 API key。</td>
</tr>
<tr>
  <td width="48"><strong>🖼️</strong></td>
  <td><strong>排版好看的 HTML</strong><br>所有范文输出到一个网页，手机上也能看，打印出来也行。高亮词汇、结构分析、一键复制。配色是雅思经典的海军蓝加金色。</td>
</tr>
<tr>
  <td width="48"><strong>🔄</strong></td>
  <td><strong>学习计划会自己调整</strong><br>今天没空练就自动往后排。某个话题写得不顺就优先再练一次。102 个话题不会偷偷重复安排，除非你自己说再来一题。进度全记在本地 JSON 文件里，跨会话不丢失。</td>
</tr>
</table>

---

## ⚡ 快速上手

```bash
# 1. 下载
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach

# 2. 把 ielts-coach 文件夹复制到你的 agent 的 skills 目录：
#    Claude Code:     cp -r ielts-coach /你的项目/.claude/skills/
#    其他 agent:      把 ielts-coach/ 复制到对应 agent 的 skills 目录即可

# 3. 启动 agent，直接说人话就行，技能会自动触发
```

> 💡 **不用额外配置。** 说一句开始我的雅思备考，剩下的教练帮你搞定。入门引导 → 学习计划 → 每天聊话题 → 范文自动保存到网页。

**用 DeepSeek 或者其他非视觉模型的同学：** 第一次碰到图表读不出来的时候，教练会自动引导你花两分钟搭好视觉桥接。你全程只需要提供一个 API key。

---

## 🔄 是怎么工作的

```
┌──────────────────────────────────────────────────────────┐
│                   第一次用                                  │
│  填信息 → 自动生成学习计划 → 搞定                           │
│  （5分钟：考试日期、目标分、你是干啥的、啥时候有空）          │
└─────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────┐
│                   每次打开                                  │
│                                                          │
│  打个招呼 + 告诉你上次练到哪了                               │
│       │                                                  │
│       ▼                                                  │
│  ┌─────────────────────────────────┐                     │
│  │  话题挖掘对话（每个话题走一遍）     │  ← 核心差异          │
│  │  A: 告诉你今天聊什么             │                     │
│  │  B: 引导你回忆相关经历           │                     │
│  │  C: 跟你确认：我理解对了吗？       │                     │
│  │  D: 把你的话润色成范文           │                     │
│  └─────────────────────────────────┘                     │
│       │                                                  │
│       ▼                                                  │
│  一篇范文（你的故事、你说话的感觉）                           │
│  + 高亮好词好句                                             │
│  + 冲着你的目标分数校准                                       │
│  + 检查有没有 AI 味儿                                        │
│       │                                                  │
│       ▼                                                  │
│  保存到 ielts_answers.html                                 │
│  更新进度 → 明天见 👋                                        │
└──────────────────────────────────────────────────────────┘
```

---

## 📁 文件结构

```
ielts-coach/
├── SKILL.md                              # 教练的大脑（约 700 行指令）
├── references/
│   ├── question-bank.md                  # Part 1 + P2&3 新题（38+29）
│   ├── question_bank_complete.json       # P2&3 保留题 + 非大陆题（27+8）
│   ├── band-descriptors.md               # 口语评分标准
│   ├── writing-band-descriptors.md       # 官方写作评分标准（2023年5月版）
│   ├── writing-resources.md              # Task 1 图表写法 + Task 2 模板
│   └── sample-answers.md                 # 范文参考（用于校准质量）
├── scripts/
│   ├── state_manager.py                  # JSON 状态文件读写
│   ├── build_complete_bank.py            # 题库构建
│   └── vision_mcp_server.py             # MCP 视觉桥接（DeepSeek → qwen-vl）
└── assets/
    └── answer_template.html              # 范文网页模板
```

> ⚡ **把 `ielts-coach/` 整个文件夹丢进你 agent 的 skills 目录就好。** 运行时的个人文件（`user_profile.json`、`study_plan.json`、`progress.json`、`ielts_answers.html`）在你的项目根目录下自动生成，这个仓库里不存你的隐私。

---

## 🎯 四个维度的个性化

任何静态模板都做不到的事情。这个教练同时在四个维度上做个性化：

| 维度 | 来源 | 举个例子 |
|---|---|---|
| **1. 你是谁** | 入门引导 | 我在深圳当程序员…… |
| **2. 你经历过什么** | 话题挖掘聊天 | 那次凌晨三点抢修线上故障的时候…… |
| **3. 你要考几分** | 你的目标分数 | Band 7 的词汇密度，不用硬塞生僻词 |
| **4. 你是什么口吻** | 聊天里捕捉到的语言习惯 | 你说话的那种幽默感、你的文化背景、你的句式节奏 |

**最后出来的效果：** 一篇在雅思评分表上拿得到目标分，而且你考试那天真的能想起来怎么说的范文。

---

## 👁️ DeepSeek 也能看图

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  你的图表     │────▶│  vision_bridge    │────▶│  qwen-vl-plus    │
│  (PNG/JPG)   │     │  (MCP 服务器)     │     │  (百炼免费额度)   │
└──────────────┘     └──────────────────┘     └────────┬────────┘
                                                        │
                                              ┌─────────▼─────────┐
                                              │  把图里的内容用     │
                                              │  文字描述出来        │
                                              └─────────┬─────────┘
                                                        │
┌──────────────┐     ┌──────────────────┐              │
│  Task 1      │◀────│  你的 Agent       │◀─────────────┘
│  范文         │     │  (DeepSeek等)     │
└──────────────┘     └──────────────────┘
```

**一次配好，后面不用管（全程 agent 自己动）：** pip install → 写 settings.json → 重启。你只做一件事：给 API key。

想用自己的模型也行，任何兼容 OpenAI 接口格式的视觉模型都能接。

---

## 🤝 一起完善

这个工具原本是我自己备考用的，觉得好用就开源了。非常欢迎一起改进：

- 发现题库有错漏？提个 Issue
- HTML 页面有什么好的设计想法？说来听听
- 你也写了范文愿意分享？丢进参考库
- 发现范文里还有 AI 味儿没去掉？告诉我

直接提 Issue 或者 PR 都行。

---

## 📜 许可

MIT © [Romain Chen](https://github.com/RomainCHEN)。随便用、随便改。祝你上岸。

---

<p align="center">
  <sub>覆盖 2026年5-8月 雅思口语季 · 102个话题 · 口语 + 写作</sub>
  <br>
  <sub>一个被雅思折磨过的人用心写的工具 ❤️</sub>
</p>
