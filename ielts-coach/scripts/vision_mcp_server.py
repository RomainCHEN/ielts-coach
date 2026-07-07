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

3. Restart your agent. It will use `analyze_image` when it encounters charts.

Environment Variables:
   VISION_API_KEY  (required) - API key for the vision model provider
   VISION_BASE_URL (optional) - OpenAI-compatible chat completions URL
                   Default: Alibaba Cloud Bailian DashScope
   VISION_MODEL    (optional) - Model ID. Default: "qwen3.7-plus"
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


def _build_url():
    base = VISION_BASE_URL.rstrip("/")
    if base.endswith("/chat/completions"):
        return base
    return f"{base}/chat/completions"


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

    response = httpx.post(
        _build_url(), json=payload, headers=headers,
        timeout=httpx.Timeout(120.0, connect=30.0),
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected API response structure: {json.dumps(data, indent=2)[:500]}") from e


# ---------------------------------------------------------------------------
# Tools (using list_tools/call_tool for MCP SDK 1.x compatibility)
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
