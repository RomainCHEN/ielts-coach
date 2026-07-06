<p align="right">
  <a href="#english">🇬🇧 English</a>&nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="#chinese">🇨🇳 简体中文</a>
</p>

---

<a id="english"></a>

<h1>🎓 IELTS Coach — Speaking & Writing AI Preparation Agent</h1>

<p>A deeply personalized <a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> skill for IELTS exam preparation. This agent generates customized model answers for IELTS Speaking (Parts 1, 2, 3) and Writing (Task 1 &amp; 2), tailored to <strong>your</strong> background, target band score, and exam timeline.</p>

<blockquote>
<strong>📅 Question Bank Season:</strong> May–August 2026 &nbsp;|&nbsp;
<strong>Topics:</strong> 102 speaking topics &nbsp;|&nbsp;
<strong>Language:</strong> Personalized in your voice
</blockquote>

<h2>✨ Features</h2>

<table>
<tr><td>📋</td><td><strong>Complete Question Bank</strong> — 102 speaking topics: Part 1 (38), Part 2&3 New (29), Part 2&3 Retained (27), Non-mainland (8)</td></tr>
<tr><td>🎯</td><td><strong>Personalized Study Plan</strong> — Onboarding collects your exam date, target scores, and availability, then builds a day-by-day schedule</td></tr>
<tr><td>🗣️</td><td><strong>Topic Discovery Conversations</strong> — Before every new topic, the agent mines your life for specific memories, opinions, and experiences — your answers sound like <em>you</em>, not a textbook</td></tr>
<tr><td>📝</td><td><strong>Band-Calibrated Answers</strong> — Vocabulary, sentence complexity, and cohesion automatically match your target band (6 / 7 / 8)</td></tr>
<tr><td>🖼️</td><td><strong>Beautiful HTML Output</strong> — All answers rendered to a responsive, printable page with highlighted expressions, structure notes, and copy buttons</td></tr>
<tr><td>🔄</td><td><strong>Self-Evolving Plan</strong> — Adapts to your progress: reschedules missed sessions, prioritizes weak areas, avoids topic repetition</td></tr>
<tr><td>✍️</td><td><strong>Writing Task 1 Charts</strong> — Drop chart images into <code>task1_charts/</code> and the agent generates model responses</td></tr>
</table>

<h2>🚀 Quick Start</h2>

<h3>Prerequisites</h3>
<ul>
  <li><a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> CLI installed</li>
  <li>Python 3.10+ (for state management scripts)</li>
</ul>

<h3>Installation</h3>

<pre><code># Clone the repository
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach

# Or copy the skill into your existing project:
cp -r .claude/skills/ielts-coach /path/to/your-project/.claude/skills/
</code></pre>

<h3>Usage</h3>

<p>The skill triggers automatically when you mention IELTS. Just say things like:</p>

<ul>
  <li>"Start my IELTS preparation"</li>
  <li>"I want to practice speaking Part 2 today"</li>
  <li>"Show me my study plan"</li>
  <li>"I have a writing task 2 question…"</li>
</ul>

<p><strong>First session:</strong> The agent runs onboarding — exam date, target scores, hobbies, background. This info personalizes <em>all</em> future answers.</p>

<p><strong>Daily sessions:</strong> Greets you with progress stats, delivers unique topics, runs a <strong>Topic Discovery conversation</strong> to mine your experiences, then generates model answers saved to <code>ielts_answers.html</code>.</p>

<h2>📁 Project Structure</h2>

<pre><code>ielts-coach/
├── .claude/skills/ielts-coach/
│   ├── SKILL.md                         # Core agent behavior instructions
│   ├── references/
│   │   ├── question-bank.md             # Part 1 + P2&3 New topics (full detail)
│   │   ├── question_bank_complete.json  # P2&3 Retained + Non-mainland topics
│   │   ├── band-descriptors.md          # IELTS band criteria reference
│   │   ├── writing-resources.md         # Task 1 chart language, Task 2 templates
│   │   └── sample-answers.md            # Calibrated example answers for quality
│   ├── scripts/
│   │   ├── state_manager.py             # JSON state file management
│   │   └── build_complete_bank.py       # Question bank builder
│   └── assets/
│       └── answer_template.html         # HTML template for answer display
├── task1_charts/                        # Drop Writing Task 1 chart images here
├── ielts_answers.html                   # Generated model answers (auto-updated)
├── CLAUDE.md                            # Project documentation for Claude
└── README.md
</code></pre>

<h2>🗂️ State Files (Auto-Generated)</h2>

<table>
<tr><th>File</th><th>Purpose</th></tr>
<tr><td><code>user_profile.json</code></td><td>Exam date, target scores, personal background</td></tr>
<tr><td><code>study_plan.json</code></td><td>Day-by-day topic schedule with completion status</td></tr>
<tr><td><code>progress.json</code></td><td>Topics completed, answers generated, daily activity log</td></tr>
</table>

<h2>📊 Topic Distribution</h2>

<table>
<tr><th>Session Type</th><th>Topics per Session</th><th>Strategy</th></tr>
<tr><td>Speaking</td><td>1–2 Part 1 + 1 Part 2&3</td><td>Essential topics → New → Retained</td></tr>
<tr><td>Writing</td><td>1–2 essays (your prompts)</td><td>Task 2 prioritized over Task 1</td></tr>
<tr><td>Mixed</td><td>1 Part 1 + 1 essay</td><td>Alternating focus</td></tr>
</table>

<h2>🧠 Design Philosophy</h2>

<table>
<tr><td><strong>Progressive Personalization</strong></td><td>General background is just the start. Every new topic triggers a mini-interview to mine <em>that specific</em> experience from your life.</td></tr>
<tr><td><strong>Polish, Don't Replace</strong></td><td>The agent elevates your raw thoughts to band-appropriate English — it doesn't ghostwrite from scratch. Your voice, your memories, your opinions.</td></tr>
<tr><td><strong>Memorization-Friendly</strong></td><td>Answers built around your own experiences are inherently easier to recall under exam pressure.</td></tr>
<tr><td><strong>Band-Appropriate</strong></td><td>A Band 6 answer that's authentically <em>you</em> beats a Band 8 answer that sounds like a dictionary.</td></tr>
<tr><td><strong>No Repetition</strong></td><td>Topics are never silently repeated. Review happens only with your consent.</td></tr>
</table>

<h2>📄 PDF Extraction</h2>

<p>The question bank was extracted from the official 50-page IELTS speaking question bank PDF using:</p>
<ol>
  <li><strong>PyMuPDF</strong> — Initial text extraction and topic identification</li>
  <li><strong><a href="https://github.com/opendatalab/MinerU">MinerU API</a></strong> — High-quality Chinese document conversion via <code>mineru-open-api flash-extract</code></li>
</ol>

<h2>🤝 Contributing</h2>

<p>Improvements welcome:</p>
<ul>
  <li>Report topic inaccuracies or missing questions</li>
  <li>Suggest HTML design improvements</li>
  <li>Add sample answers for calibration</li>
</ul>

<h2>📜 License</h2>

<p>MIT — Use freely for your IELTS preparation.</p>

<p align="right"><a href="#top">🔝 Back to top</a></p>

---

<a id="chinese"></a>

<h1>🎓 IELTS Coach — 雅思口语与写作 AI 备考助手</h1>

<p>一个深度个性化的 <a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> 技能，专为雅思备考设计。该智能助手会根据<strong>你的</strong>个人背景、目标分数和考试时间，为雅思口语（Part 1/2/3）和写作（Task 1/2）生成定制化范文答案。</p>

<blockquote>
<strong>📅 题库季节：</strong>2026年5–8月 &nbsp;|&nbsp;
<strong>话题数：</strong>102个口语话题 &nbsp;|&nbsp;
<strong>语言风格：</strong>以你的口吻个性化定制
</blockquote>

<h2>✨ 功能特性</h2>

<table>
<tr><td>📋</td><td><strong>完整题库</strong> — 102个口语话题：Part 1（38个）、Part 2&3新题（29个）、保留题（27个）、非大陆题（8个）</td></tr>
<tr><td>🎯</td><td><strong>个性化学习计划</strong> — 入门引导收集你的考试日期、目标分数和可用时间，自动生成每日学习安排</td></tr>
<tr><td>🗣️</td><td><strong>话题挖掘对话</strong> — 每接触一个新话题，助手会先引导你回忆具体经历、观点和感受——让你的答案听起来像<em>你自己</em>，而非教科书</td></tr>
<tr><td>📝</td><td><strong>分数匹配</strong> — 词汇密度、句式复杂度和衔接手段自动匹配你的目标分数（6分 / 7分 / 8分）</td></tr>
<tr><td>🖼️</td><td><strong>精美 HTML 输出</strong> — 所有答案渲染为响应式、可打印的网页，包含高亮词汇、结构笔记和一键复制</td></tr>
<tr><td>🔄</td><td><strong>计划自进化</strong> — 根据你的进度动态调整：重新安排错过的课程、优先薄弱环节、避免话题重复</td></tr>
<tr><td>✍️</td><td><strong>写作 Task 1 图表</strong> — 将图表图片放入 <code>task1_charts/</code> 文件夹，助手自动分析并生成范文</td></tr>
</table>

<h2>🚀 快速开始</h2>

<h3>前置条件</h3>
<ul>
  <li>已安装 <a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> CLI</li>
  <li>Python 3.10+（用于状态管理脚本）</li>
</ul>

<h3>安装</h3>

<pre><code># 克隆仓库
git clone https://github.com/RomainCHEN/ielts-coach.git
cd ielts-coach

# 或将技能复制到你已有的项目中：
cp -r .claude/skills/ielts-coach /path/to/your-project/.claude/skills/
</code></pre>

<h3>使用方法</h3>

<p>当你提到雅思相关内容时，技能会自动触发。例如：</p>

<ul>
  <li>"开始我的雅思备考"</li>
  <li>"我今天想练习口语 Part 2"</li>
  <li>"查看我的学习计划"</li>
  <li>"我有一个写作 Task 2 题目…"</li>
</ul>

<p><strong>首次会话：</strong>助手会进行入门引导——考试日期、目标分数、兴趣爱好、背景信息。这些信息将用于个性化<em>所有</em>后续答案。</p>

<p><strong>每日会话：</strong>问候并展示进度，推送当天独有的话题，进行<strong>话题挖掘对话</strong>了解你的相关经历，然后生成范文并保存至 <code>ielts_answers.html</code>。</p>

<h2>📁 项目结构</h2>

<pre><code>ielts-coach/
├── .claude/skills/ielts-coach/
│   ├── SKILL.md                         # 核心助手行为指令
│   ├── references/
│   │   ├── question-bank.md             # Part 1 + P2&3 新题（完整详情）
│   │   ├── question_bank_complete.json  # P2&3 保留题 + 非大陆题
│   │   ├── band-descriptors.md          # 雅思评分标准参考
│   │   ├── writing-resources.md         # Task 1 图表语言 + Task 2 模板
│   │   └── sample-answers.md            # 校准范文（质量控制）
│   ├── scripts/
│   │   ├── state_manager.py             # JSON 状态文件管理
│   │   └── build_complete_bank.py       # 题库构建工具
│   └── assets/
│       └── answer_template.html         # 答案展示 HTML 模板
├── task1_charts/                        # 将写作 Task 1 图表图片放这里
├── ielts_answers.html                   # 生成的范文（自动更新）
├── CLAUDE.md                            # Claude 项目文档
└── README.md
</code></pre>

<h2>🗂️ 状态文件（自动生成）</h2>

<table>
<tr><th>文件</th><th>用途</th></tr>
<tr><td><code>user_profile.json</code></td><td>考试日期、目标分数、个人背景</td></tr>
<tr><td><code>study_plan.json</code></td><td>每日话题安排及完成状态</td></tr>
<tr><td><code>progress.json</code></td><td>已完成话题、已生成答案、每日活动日志</td></tr>
</table>

<h2>📊 话题分配策略</h2>

<table>
<tr><th>会话类型</th><th>每次话题数</th><th>策略</th></tr>
<tr><td>口语</td><td>1–2 个 Part 1 + 1 个 Part 2&3</td><td>基础话题 → 新题 → 保留题</td></tr>
<tr><td>写作</td><td>1–2 篇作文（你提供题目）</td><td>Task 2 优先于 Task 1</td></tr>
<tr><td>混合</td><td>1 个 Part 1 + 1 篇作文</td><td>口语写作交替进行</td></tr>
</table>

<h2>🧠 设计理念</h2>

<table>
<tr><td><strong>渐进式个性化</strong></td><td>通用背景信息只是起点。每个新话题都会触发一次迷你访谈，从你的生活中挖掘<em>与这个话题相关</em>的具体经历。</td></tr>
<tr><td><strong>润色而非替代</strong></td><td>助手将你的原始想法提升到匹配目标分数的英语水平——而不是从零开始代笔。你的声音、你的回忆、你的观点。</td></tr>
<tr><td><strong>便于记忆</strong></td><td>围绕你自身经历构建的答案，在考试压力下天生更容易回忆起来。</td></tr>
<tr><td><strong>分数匹配</strong></td><td>一个真实自然的 Band 6 答案，远胜于一个听起来像词典的 Band 8 答案。</td></tr>
<tr><td><strong>永不重复</strong></td><td>话题不会在未经你同意的情况下悄悄重复。复习只在你明确要求时进行。</td></tr>
</table>

<h2>📄 PDF 提取说明</h2>

<p>题库从官方50页雅思口语题库 PDF 中提取，使用了以下工具：</p>
<ol>
  <li><strong>PyMuPDF</strong> — 初步文本提取与话题识别</li>
  <li><strong><a href="https://github.com/opendatalab/MinerU">MinerU API</a></strong> — 高质量中文文档转换，通过 <code>mineru-open-api flash-extract</code> 实现</li>
</ol>

<h2>🤝 贡献</h2>

<p>欢迎改进：</p>
<ul>
  <li>反馈话题不准确或缺失的题目</li>
  <li>建议 HTML 设计改进</li>
  <li>补充校准范文</li>
</ul>

<h2>📜 许可证</h2>

<p>MIT — 自由用于雅思备考。</p>

<p align="right"><a href="#top">🔝 回到顶部</a></p>
