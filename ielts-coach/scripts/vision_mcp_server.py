#!/usr/bin/env python3
"""
IELTS Coach - Vision MCP Bridge Server

A lightweight MCP (Model Context Protocol) server that provides image analysis
capabilities to AI coding agents running on models without native vision support
(e.g., DeepSeek).

Provides:
- analyze_image: Reads an image file and returns a text description optimized for
  IELTS Task 1 chart analysis
- get_model_info: Returns the currently configured vision model and provider

============================================================
SUPPORTED PROVIDERS
============================================================

1. OpenAI-compatible (DashScope, OpenAI, etc.):
   VISION_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
   VISION_MODEL="qwen3.7-plus"

2. Google Gemini (native API):
   VISION_BASE_URL="https://generativelanguage.googleapis.com/v1beta"
   VISION_MODEL="gemini-2.5-flash"
   (API key in VISION_API_KEY, passed as ?key= query param)

3. Google Gemini (OpenAI-compatible):
   VISION_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai"
   VISION_MODEL="gemini-2.5-flash"

============================================================
SETUP (for users)
============================================================

1. Install dependencies:
   pip install mcp httpx

2. Add the MCP server to your agent's config:

   {
     "mcpServers": {
       "vision-bridge": {
         "command": "python",
         "args": ["ielts-coach/scripts/vision_mcp_server.py"],
         "env": {
           "VISION_API_KEY": "your-api-key-here",
           "VISION_BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
           "VISION_MODEL": "qwen3.7-plus"
         }
       }
     }
   }

3. Restart your agent.
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

DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL = "qwen3.7-plus"

VISION_API_KEY = os.getenv("VISION_API_KEY", "")
VISION_BASE_URL = os.getenv("VISION_BASE_URL", DEFAULT_BASE_URL)
VISION_MODEL = os.getenv("VISION_MODEL", DEFAULT_MODEL)

# ---------------------------------------------------------------------------
# Startup logging (diagnostic)
# ---------------------------------------------------------------------------

_STARTUP_LOG = Path(__file__).with_name("vision_mcp_startup.log")
try:
    _STARTUP_LOG.write_text(
        f"vision_mcp_server.py started at {__import__('datetime').datetime.now().isoformat()}\n"
        f"python: {__import__('sys').executable}\n"
        f"cwd: {Path.cwd()}\n"
        f"VISION_API_KEY set: {bool(VISION_API_KEY)}\n"
        f"VISION_BASE_URL: {VISION_BASE_URL}\n"
        f"VISION_MODEL: {VISION_MODEL}\n"
    )
except Exception:
    pass  # Don't crash if we can't write a log

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

server = Server("vision-bridge")


def _is_gemini():
    return "generativelanguage.googleapis.com" in VISION_BASE_URL


def _encode_image(image_path: str) -> tuple[str, str, str]:
    """Read an image file and return (base64_data, mime_type, data_uri)."""
    path = Path(image_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    mime_type, _ = mimetypes.guess_type(str(path))
    if mime_type is None:
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
    return encoded, mime_type, data_uri


def _call_gemini_api(image_path: str) -> str:
    """Send an image to Gemini via native API."""
    encoded, mime_type, _ = _encode_image(image_path)

    system_prompt = (
        "You are an IELTS Task 1 chart analyst. Describe the image in precise, "
        "structured detail so that an AI agent (without vision) can generate a "
        "high-quality Task 1 model answer.\n\n"
        "Include: chart type, title, axes labels with units, legend entries, "
        "key data points, trends, comparisons, peaks, lows, time periods, "
        "and a 2-3 point overview summary.\n\n"
        "Be thorough and precise with numbers. Do NOT interpret or give IELTS advice "
        "- just describe what you see in data-rich detail."
    )

    base = VISION_BASE_URL.rstrip("/")
    if not base.endswith("/models"):
        base = f"{base}/models"
    url = f"{base}/{VISION_MODEL}:generateContent?key={VISION_API_KEY}"

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}],
        },
        "contents": [{
            "parts": [
                {"inlineData": {"mimeType": mime_type, "data": encoded}},
                {"text": "Describe this chart/image in full detail for IELTS Task 1 analysis."},
            ],
        }],
        "generationConfig": {"maxOutputTokens": 2000, "temperature": 0.0},
    }

    response = httpx.post(url, json=payload, timeout=httpx.Timeout(180.0, connect=30.0))
    response.raise_for_status()
    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Gemini response: {json.dumps(data, indent=2)[:500]}") from e


def _call_openai_api(image_path: str) -> str:
    """Send an image via OpenAI-compatible chat completions API."""
    _, _, data_uri = _encode_image(image_path)

    system_prompt = (
        "You are an IELTS Task 1 chart analyst. Describe the image in precise, "
        "structured detail so that an AI agent (without vision) can generate a "
        "high-quality Task 1 model answer.\n\n"
        "Include: chart type, title, axes labels with units, legend entries, "
        "key data points, trends, comparisons, peaks, lows, time periods, "
        "and a 2-3 point overview summary.\n\n"
        "Be thorough and precise with numbers. Do NOT interpret or give IELTS advice "
        "- just describe what you see in data-rich detail."
    )

    payload = {
        "model": VISION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": data_uri, "detail": "high"}},
                {"type": "text", "text": "Describe this chart/image in full detail for IELTS Task 1 analysis."},
            ]},
        ],
        "max_tokens": 2000,
        "temperature": 0.0,
    }

    headers = {
        "Authorization": f"Bearer {VISION_API_KEY}",
        "Content-Type": "application/json",
    }

    base = VISION_BASE_URL.rstrip("/")
    if base.endswith("/chat/completions"):
        url = base
    else:
        url = f"{base}/chat/completions"

    response = httpx.post(url, json=payload, headers=headers,
                          timeout=httpx.Timeout(120.0, connect=30.0))
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response: {json.dumps(data, indent=2)[:500]}") from e


def _call_vision_api(image_path: str) -> str:
    """Route to the correct API implementation based on configuration."""
    if _is_gemini():
        return _call_gemini_api(image_path)
    return _call_openai_api(image_path)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@server.list_tools()
async def handle_list_tools():
    return [
        Tool(
            name="analyze_image",
            description="Analyze an image file using a vision-capable LLM and return a detailed text description optimized for IELTS Task 1 chart analysis. Use this when the agent cannot directly process images.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Absolute or relative path to the image file (PNG, JPG, GIF, WEBP).",
                    }
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="get_model_info",
            description="Return the currently configured vision model and provider information.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "analyze_image":
        image_path = arguments.get("image_path", "")
        if not VISION_API_KEY:
            return [TextContent(type="text", text=(
                "ERROR: VISION_API_KEY not set. Configure it in the MCP server env section."
            ))]
        try:
            description = _call_vision_api(image_path)
            return [TextContent(type="text", text=description)]
        except FileNotFoundError as e:
            return [TextContent(type="text", text=f"ERROR: {e}")]
        except httpx.HTTPStatusError as e:
            return [TextContent(type="text", text=(
                f"ERROR: API returned {e.response.status_code}.\n{e.response.text[:500]}\n\n"
                "Check VISION_API_KEY, VISION_BASE_URL, and VISION_MODEL."
            ))]
        except Exception as e:
            return [TextContent(type="text", text=f"ERROR: {type(e).__name__}: {e}")]

    elif name == "get_model_info":
        info = json.dumps({
            "model": VISION_MODEL,
            "base_url": VISION_BASE_URL,
            "protocol": "gemini-native" if _is_gemini() else "openai-compatible",
            "api_key_configured": bool(VISION_API_KEY),
            "api_key_prefix": f"{VISION_API_KEY[:8]}..." if VISION_API_KEY else "(not set)",
            "status": "ready" if VISION_API_KEY else "missing API key",
        }, indent=2)
        return [TextContent(type="text", text=info)]

    else:
        return [TextContent(type="text", text=f"ERROR: Unknown tool: {name}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
