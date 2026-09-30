# Image Recognition Fallback (non-vision models)

Loaded when a chart image cannot be read. The agent does all configuration; the learner only supplies an API key and restarts the agent.

This section covers what to do when the user's agent model cannot process images
(e.g., DeepSeek, some open-source models, or API-only text models).

## When to Trigger

Trigger this flow when EITHER:
- The model fails to read a chart image while checking Task 1 charts (SKILL.md Phase 2)
- The model fails to read a PDF scan or screenshot the user uploads
- The user explicitly mentions their model "can't see images"
- Any Read tool call on an image file returns an error or blank content

## Detection

If a Read call on an image (PNG/JPG/PDF) returns an error or the model says it cannot
describe the image, immediately recognize this as a vision support gap. Do NOT retry
the same approach — pivot to the fallback flow below.

## Step-by-Step Fallback Flow

**Core principle: YOU (the agent) do all the configuration work.** The user only provides
credentials. Never ask the user to manually edit JSON files, restart servers, or run
commands — you handle all of that. The only thing the user must do is restart their agent
at the end (because you cannot control their process).

### Step 1: Acknowledge and Explain

> "It looks like your current model doesn't support image recognition (common with
> DeepSeek and others). No worries — I'll set up a local MCP vision bridge for you.
> This takes about 2 minutes and only needs to be done once."

### Step 2: Ask About Provider Preference

> "Pick a vision provider:
> 1. **Alibaba Cloud Bailian (百炼, recommended)** — Free tier. Uses DashScope
>    API (`dashscope.aliyuncs.com/compatible-mode/v1`) with qwen3.7-plus,
>    which natively supports image recognition. I just need your API key.
> 2. **Your own provider** — If you already use OpenAI, Claude API, or any
>    OpenAI-compatible vision service, I'll configure that instead."

Ask: "Which option? Or would you rather skip this chart for now?"

### Step 3A: Set Up Bailian (Option 1 — Agent Does Everything)

If the user chooses Bailian:

1. **Ask for the API key only:**
   > "Go to [bailian.console.aliyun.com](https://bailian.console.aliyun.com/) →
   >   API Key management → create or copy your key. Paste it here."

2. **Wait for the user to paste the key.** Validate it's non-empty.

3. **Install dependencies** (run this yourself — do NOT ask the user):
   ```bash
   pip install mcp httpx
   ```

4. **Verify the script exists:** Check that `scripts/vision_mcp_server.py` is present in
   the skill directory. If not, create it from the template.

5. **Configure the MCP server** — edit the project settings file yourself:
   - First, check if `./.claude/settings.json` exists. If not, create it.
   - The MCP server config goes under `mcpServers` key.
   - If the file already has content, merge; otherwise create the full structure.
   - Use these values:
     - `command`: `"python"`
     - `args`: `["ielts-coach/scripts/vision_mcp_server.py"]`
     - `env.VISION_API_KEY`: the key the user provided
     - `env.VISION_BASE_URL`: `"https://dashscope.aliyuncs.com/compatible-mode/v1"`
     - `env.VISION_MODEL`: `"qwen3.7-plus"`

   Target structure for `.claude/settings.json`:
   ```json
   {
     "mcpServers": {
       "vision-bridge": {
         "command": "python",
         "args": ["ielts-coach/scripts/vision_mcp_server.py"],
         "env": {
           "VISION_API_KEY": "<user-provided-key>",
           "VISION_BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
           "VISION_MODEL": "qwen3.7-plus"
         }
       }
     }
   }
   ```

6. **If `.claude/settings.json` already has content** (e.g., existing `mcpServers` or
   other keys), carefully merge the `vision-bridge` entry into the existing `mcpServers`
   object without overwriting other servers or top-level settings.

7. **Confirm completion:**
   > "Done! I've installed the dependencies and configured the vision bridge. All you
   > need to do now is restart your agent. When you're back, I'll analyze the chart
   > for you. Ready to restart?"

### Step 3B: Set Up Custom Provider (Option 2 — Agent Does Everything)

If the user prefers their own provider:

1. **Collect credentials:**
   > "Please provide:
   > - **Base URL** — your OpenAI-compatible chat completions endpoint
   >   (e.g., `https://api.openai.com/v1`)
   > - **API Key** — your key
   > - **Model Name** — the vision-capable model ID (e.g., `gpt-4o`)"

2. **Wait for the user to provide all three.** Validate each is non-empty.
   If the base URL doesn't end with `/v1`, note it's fine — the server handles this.

3. **Install dependencies** (run this yourself):
   ```bash
   pip install mcp httpx
   ```

4. **Configure the MCP server** — same process as Step 3A, but with the user's custom values:
   - `env.VISION_BASE_URL`: user's provided base URL
   - `env.VISION_MODEL`: user's provided model name
   - `env.VISION_API_KEY`: user's provided key

5. **Confirm completion** — same as Step 3A.

### Step 4: Post-Restart Verification

After the user restarts their agent and returns:

1. **Option A** — The MCP tool may already be available. If so, the deferred tool
   `mcp__vision-bridge__analyze_image` should appear in the system reminder.
   Load its schema via ToolSearch and proceed to analyze.

2. **Option B** — If the tool doesn't appear (new session, different context), ask
   the user to confirm they restarted, then try reading a chart image — the fallback
   should succeed now.

3. **If the tool call fails** after setup:
   - Check the error message. Common issues: wrong API key (401), network issue (timeout),
     model doesn't support vision (400).
   - For Bailian: remind the user the key must be from the Bailian console, not Alibaba Cloud's
     general API key. It needs access to the model service.
   - Offer to update the API key or switch providers.

4. **Once working**, proceed with generating the Task 1 model answer as normal.

## MCP Server Details

The vision bridge MCP server (`scripts/vision_mcp_server.py`) provides:

| Tool | Purpose |
|------|---------|
| `analyze_image` | Takes an image file path, returns a detailed text description suitable for IELTS Task 1 analysis |
| `get_model_info` | Returns the configured model name and provider for verification |

**How it works:**
1. Reads the image file, encodes it as base64
2. Sends it to the configured vision model endpoint (OpenAI-compatible chat completions API)
3. The prompt asks the model to describe the image in IELTS Task 1 terms: chart type, axes, trends, key data points, units
4. Returns the text description to the agent

**Configuration location:** `./.claude/settings.json` in the project directory.
This keeps the MCP server scoped to the IELTS Coach project —
other projects won't be affected.

## What NOT to Do

- Do NOT repeatedly retry Read on the same image — if it fails once on a non-vision model, it will fail every time
- Do NOT pretend to describe the chart from the filename or guess its content
- Do NOT ask the user to manually edit configuration files — you do ALL the editing
- Do NOT ask the user to run `pip install` — you run it yourself
- Do NOT pressure the user to switch models — the MCP bridge solves the problem without changing their setup
- Do NOT leave the user with no path forward — if they decline the MCP bridge, offer to work with a text description they can provide themselves
- The ONLY thing the user needs to do is: (a) provide their API key, (b) restart their agent

## Vision Bridge Troubleshooting

When debugging a vision bridge setup or failure, check these in order:

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| API returns 404 | Wrong protocol (Anthropic `/v1/messages` when endpoint expects `/chat/completions`) | Use `dashscope.aliyuncs.com/compatible-mode/v1` — this is OpenAI-compatible. The older `llm-9hbxloqkuc0kihh2.cn-beijing.maas.aliyuncs.com/apps/anthropic` may not work or may use a different protocol. |
| Request times out (>60s) | Image + long prompt takes time to process | Set timeout to at least 120 seconds (`httpx.Timeout(120.0, connect=30.0)`) |
| Model returns but doesn't describe image | Model may be text-only (e.g., `qwen-plus`, `qwen-turbo`) | Only `qwen3.7-plus`, `qwen-vl-plus`, `qwen-vl-max` support vision. Verify the model name. |
| MCP tool not appearing in session | SDK version mismatch — `@server.tool()` decorator not available in all MCP SDK versions | `vision_mcp_server.py` uses `@server.list_tools()` + `@server.call_tool()` for broad SDK compatibility |
| Bailian key rejected (401) | Key type mismatch | Keys from `bailian.console.aliyun.com` work with DashScope. Verify the key has model service access enabled. |
| OpenSSL/bad handshake on Windows | Python SSL configuration | No fix needed — the standard `dashscope.aliyuncs.com` endpoint works without special SSL config |
