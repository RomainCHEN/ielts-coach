#!/usr/bin/env python3
"""
IELTS Coach — Vision MCP Bridge Server

A lightweight MCP (Model Context Protocol) server that provides image analysis
capabilities to Claude Code agents running on models without native vision support
(e.g., DeepSeek).

Provides:
- analyze_image: Reads an image file and returns a text description optimized for
  IELTS Task 1 chart analysis
- get_model_info: Returns the currently configured vision model and provider

============================================================
SETUP (for users)
============================================================

1. Install dependencies:
   pip install mcp httpx

2. Configure Claude Code — add to ~/.claude/claude.json (or project settings.json):

   {
     "mcpServers": {
       "vision-bridge": {
         "command": "python",
         "args": [".claude/skills/ielts-coach/scripts/vision_mcp_server.py"],
         "env": {
           "VISION_API_KEY": "your-api-key-here",
           "VISION_BASE_URL": "https://llm-9hbxloqkuc0kihh2.cn-beijing.maas.aliyuncs.com/apps/anthropic",
           "VISION_MODEL": "qwen-vl-plus"
         }
       }
     }
   }

   # For a custom provider, change VISION_BASE_URL and VISION_MODEL accordingly:
   # OpenAI: VISION_BASE_URL="https://api.openai.com/v1"  VISION_MODEL="gpt-4o"
   # Any OpenAI-compatible endpoint works.

3. Restart Claude Code. The agent will use analyze_image when it encounters charts.

Environment Variables:
   VISION_API_KEY  (required) — API key for the vision model provider
   VISION_BASE_URL (optional) — OpenAI-compatible chat completions URL
                   Default: Alibaba Cloud Bailian (qwen-vl)
   VISION_MODEL    (optional) — Model ID. Default: "qwen-vl-plus"
============================================================
"""

import os
import json
import base64
import mimetypes
from pathlib import Path

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ---------------------------------------------------------------------------
# Configuration (from environment variables)
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "https://llm-9hbxloqkuc0kihh2.cn-beijing.maas.aliyuncs.com/apps/anthropic"
DEFAULT_MODEL = "qwen-vl-plus"

VISION_API_KEY = os.getenv("VISION_API_KEY", "")
VISION_BASE_URL = os.getenv("VISION_BASE_URL", DEFAULT_BASE_URL)
VISION_MODEL = os.getenv("VISION_MODEL", DEFAULT_MODEL)

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

server = Server("vision-bridge")


def _encode_image(image_path: str) -> tuple[str, str]:
    """Read an image file and return (base64_data_uri, mime_type)."""
    path = Path(image_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    mime_type, _ = mimetypes.guess_type(str(path))
    if mime_type is None:
        # Fallback: detect from extension
        ext = path.suffix.lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        mime_type = mime_map.get(ext, "image/png")

    data = path.read_bytes()
    encoded = base64.b64encode(data).decode("utf-8")
    data_uri = f"data:{mime_type};base64,{encoded}"
    return data_uri, mime_type


def _call_vision_api(image_path: str) -> str:
    """Send an image to the vision model and return its description."""
    data_uri, mime_type = _encode_image(image_path)

    # Build the prompt for IELTS Task 1 chart analysis
    system_prompt = (
        "You are an IELTS Task 1 chart analyst. Describe the image in precise, "
        "structured detail so that an AI agent (without vision) can generate a "
        "high-quality Task 1 model answer.\n\n"
        "Include in your description:\n"
        "- Chart type (line, bar, pie, table, map, process diagram, mixed)\n"
        "- Title and subtitle if visible\n"
        "- X-axis and Y-axis labels with units\n"
        "- Legend entries (categories, series names)\n"
        "- Key data points, trends, comparisons, peaks, lows, and anomalies\n"
        "- Time periods shown\n"
        "- Any numerical values that are clearly readable\n"
        "- Overview-level summary: the 2-3 most important things the chart shows\n\n"
        "Be thorough and precise with numbers. Do NOT interpret or give IELTS advice "
        "— just describe what you see in data-rich detail."
    )

    user_content = [
        {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}},
        {"type": "text", "text": "Please describe this chart/image in full detail for IELTS Task 1 analysis."},
    ]

    # Cut /v1/chat/completions suffix if already present to avoid double-appending
    base = VISION_BASE_URL.rstrip("/")
    if base.endswith("/v1"):
        url = f"{base}/chat/completions"
    elif "/chat/completions" in base:
        url = base
    else:
        url = f"{base}/chat/completions"

    payload = {
        "model": VISION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "max_tokens": 2000,
        "temperature": 0.0,
    }

    headers = {
        "Authorization": f"Bearer {VISION_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    with httpx.Client(timeout=httpx.Timeout(60.0)) as client:
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    # Extract the assistant's message from the OpenAI-compatible response
    try:
        content = data["choices"][0]["message"]["content"]
        return content.strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response structure: {json.dumps(data, indent=2)[:500]}") from e


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@server.tool()
async def analyze_image(image_path: str) -> str:
    """Analyze an image file using a vision-capable LLM and return a detailed
    text description optimized for IELTS Task 1 chart analysis.

    Use this when the agent cannot directly process images (e.g., running on
    DeepSeek or another non-vision model).

    Args:
        image_path: Absolute or relative path to the image file (PNG, JPG, GIF, WEBP).

    Returns:
        A structured text description covering chart type, axes, data points,
        trends, and key features.
    """
    if not VISION_API_KEY:
        return (
            "ERROR: VISION_API_KEY environment variable is not set. "
            "Please configure the MCP server with your API key. "
            "For Bailian (百炼): get your key from https://bailian.console.aliyun.com/ "
            "and add it to the 'env' section of the vision-bridge MCP server config."
        )

    try:
        description = _call_vision_api(image_path)
        return description
    except FileNotFoundError as e:
        return f"ERROR: {e}"
    except httpx.HTTPStatusError as e:
        return (
            f"ERROR: API request failed with status {e.response.status_code}.\n"
            f"Response: {e.response.text[:500]}\n\n"
            "Troubleshooting:\n"
            "- Verify your VISION_API_KEY is correct and not expired\n"
            "- Verify VISION_BASE_URL is correct for your provider\n"
            "- Verify VISION_MODEL is a valid model ID for your provider\n"
            "- Check that your provider supports vision/image inputs"
        )
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"


@server.tool()
async def get_model_info() -> str:
    """Return the currently configured vision model and provider information.

    Useful for verifying the MCP server is configured correctly before
    attempting image analysis.
    """
    return json.dumps({
        "model": VISION_MODEL,
        "base_url": VISION_BASE_URL,
        "api_key_configured": bool(VISION_API_KEY),
        "api_key_prefix": f"{VISION_API_KEY[:8]}..." if VISION_API_KEY else "(not set)",
        "status": "ready" if VISION_API_KEY else "missing API key",
    }, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
