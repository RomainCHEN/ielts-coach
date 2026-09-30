# Topic Discovery (read before generating any answer)

Loaded from SKILL.md Phase 2, step 3. The learner speaks first; the agent polishes.

**Purpose:** For every new topic, mine the user's life for specific, concrete content
before generating any model answer. The user expresses first in their own words;
you then polish their raw thoughts into a band-appropriate model answer.

## Web Form Mode (Preferred for rich interaction)

Instead of asking questions one by one in the CLI, use the web form for a better
user experience. The form is served by a local Python server.

**How to use the web form:**

1. **Generate a config JSON file** with steps, questions, and question types:
   ```json
   {
     "title": "IELTS Coach - Topic Discovery",
     "description": "请回答以下问题...",
     "topic": "Topic Name",
     "steps": [
       {
         "title": "Step 1: Topic Discovery",
         "description": "先告诉我关于这个话题的信息。",
         "tip": "请尽可能详细地回答...",
         "questions": [
           {"id": "q1", "label": "What is your favourite food?", "type": "textarea"},
           {"id": "q2", "label": "Do you prefer online shopping?", "type": "radio", "options": ["Online", "In-store", "Both"]}
         ]
       },
       {
         "title": "Step 2: Upload Chart",
         "description": "请上传你的 Writing Task 1 图表图片。",
         "questions": [
           {"id": "chart", "label": "上传图表图片", "type": "paste"}
         ]
       }
     ]
   }
   ```
   Save to: `topic_form_config.json` in the project directory.

2. **Start the server directly** (NOT in background — the server will stay alive until user submits):
   ```bash
   python ielts-coach/scripts/topic_form_server.py --config topic_form_config.json --answers topic_form_answers.json --images-dir task1_charts --port 8765
   ```
   The server will automatically open the browser, stay alive waiting for user
   submission, save answers to `topic_form_answers.json`, and shut down automatically.

3. **Tell the user** to open the browser and fill in the form:
   > "浏览器应该已经自动打开了。请在表单中填写你的回答，然后点击'提交所有回答'按钮。"

4. **After user submits**, the server will automatically shut down and save the answers.

5. **Read the answers** from `topic_form_answers.json`.
   If images were uploaded, they are saved to the `--images-dir` folder.

6. **Continue with content confirmation** (Stage C) and answer generation (Stage D).

**Supported question types:**
- `textarea` — Multi-line text input
- `radio` — Single choice from options
- `image` — File upload with preview
- `paste` — Clipboard paste (Ctrl+V) or file upload

**⚠️ Important:** The server runs as a foreground process and blocks until the user submits. Do NOT run it in background — it will be killed by the CLI environment.

## Stage A: Topic Priming

1. Announce the topic and show the exact questions or cue card
2. Set expectations clearly:
   > "Before I write anything, I want to understand YOUR take on this topic. Let me
   > ask you a few questions — answer as naturally and in as much detail as you can.
   > Your raw thoughts are exactly what I need. I'll then polish them into a
   > band-[target] model answer that still sounds like YOU."

## Stage B: Experience Mining

Ask 3-5 specific, open-ended questions tailored to the topic type. Your goal is to
extract **concrete, nameable content** — specific memories, real people, genuine
opinions, actual experiences. Follow these principles:

| Principle | Good (Do This) | Bad (Avoid This) |
|-----------|----------------|-------------------|
| Go concrete | "Can you think of a specific time when...?" | "What do you think about...?" |
| Follow up | "Tell me more about that moment." | Moving on after a thin answer |
| Help recall | "Maybe a recent trip? A teacher? Something at work?" | Silence when the user is stuck |
| Capture voice | Note their humor, expressions, cultural references | Ignoring their natural language |
| Don't lead | Let them choose their own examples | "Most people talk about X — want to use that?" |

### Question Frameworks by Topic Type

**Preference & Habit Topics (Part 1 — e.g., Music, Shopping, Tidiness, Cars):**
- "What kind of [X] do you personally gravitate toward? Why?"
- "Can you think of a specific recent example of [X] in your daily life?"
- "Has your relationship with [X] changed over the years? In what way?"
- "Is there anything about your [X] habits that might surprise people?"

**Experience & Narrative Topics (Part 2 — e.g., A Person You Admire, A Difficult Decision, A Celebration):**
- "What [person / place / event] immediately comes to mind? Tell me about them/it."
- "Walk me through what happened. Set the scene — when, where, who was there?"
- "What details made this memorable? Sights, sounds, smells, feelings?"
- "Why does THIS particular [person/place/event] stand out among all the others?"
- "What did you learn, or how did you change, as a result of this experience?"

**Opinion & Analytical Topics (Part 3 — e.g., Education, Technology, Environment):**
- "What's your honest take on this? Don't worry about sounding academic yet."
- "Can you think of concrete examples from your country, your city, or your own life?"
- "In your observation, how does this differ between generations? Urban vs rural?"
- "What do people around you think about this? Do you agree with them?"
- "Why do you think this is the case? What's driving this trend?"

**Hypothetical & Abstract Topics (unfamiliar territory — e.g., A Law You'd Like, An Invention):**
- "Even if you haven't experienced this directly, what first comes to mind?"
- "Is there something related or similar that you HAVE experienced?"
- "If you had to invent a plausible example, what would feel authentic to you?"
- "What have you heard, read, or watched about this? Any impressions?"

**Writing Task 2 (argumentative essays):**
- "What's your initial position on this issue? Which side do you lean toward, and why?"
- "What concrete examples from your country, profession, or personal experience support your view?"
- "What would someone on the opposite side argue? Can you think of a fair counterpoint?"
- "If you were explaining this to a friend over coffee, how would you put it?"
- "Are there any statistics, news stories, or cultural references that relate to this topic?"

## Stage C: Content Confirmation

Before generating, summarize what you've captured and get confirmation:

> "Let me make sure I've understood. You mentioned [summarize key points in 2-3 sentences].
> I'll build your model answer around [core idea/person/experience]. Sound right?
> Anything you want to add or tweak before I write?"

This prevents wasted effort on a misaligned answer and gives the user agency.

## Stage D: Generate the Model Answer

Now generate the answer following the formats in `references/answer-formats.md`. The answer must:
- Use the user's specific examples, memories, and opinions (not generic filler)
- Preserve their authentic voice while elevating vocabulary to band-appropriate level
- Include highlighted expressions that naturally extend their existing word choices
- Feel like a **polished version of what THEY said**, not a brand-new ghostwritten answer

## Handling Difficult Discovery Situations

| Situation | How to Handle |
|-----------|---------------|
| User gives very brief, thin answers | Gently probe deeper: "That's interesting — tell me a bit more about that. What happened next?" |
| User says "I have no experience with this at all" | Pivot to related angles: "Let's find a connection. Have you ever [similar experience]? Or what do you imagine it would be like based on what you know?" |
| User's content is genuinely thin even after probing | Be honest: "This is a good start. To make this a stronger answer, let's think about adding [specific angle]. Is there anything else about...?" Then supplement judiciously. |
| User wants to skip discovery entirely | Explain the value: "I can write a generic answer, but it won't be nearly as easy to memorize because it won't sound like you. How about just 3 quick questions first?" If they still insist, generate a generic version but mark it clearly as **"[Generic — not personalized]"** and remind them they can customize it later. |
| Topic overlaps significantly with a previous one | Flag it: "This is similar to [previous topic] we covered. How was your experience or perspective different this time?" Mine for new angles. |
