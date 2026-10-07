import sys
import io
import os

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")

import asyncio
import json
from contextlib import AsyncExitStack
from collections.abc import Callable
from pathlib import Path
from typing import cast

from mcp import ClientSession, StdioServerParameters
from mcp.types import TextContent
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

load_dotenv(Path(__file__).resolve().parent / ".env")

client = AsyncOpenAI(base_url="http://127.0.0.1:8000/v1", api_key=os.environ["LOCAL_API_KEY"])
MODEL = "Qwen3.5-4B-4bit"

WORKSPACE = Path(__file__).parent / "workspace"

# Each server is just a command to launch. Same format Claude Code uses.
MCP_SERVERS = {
    "time": StdioServerParameters(command="uvx", args=["mcp-server-time"]),
    "fetch": StdioServerParameters(command="uvx", args=["mcp-server-fetch"]),
}


# --- our own local tools, unchanged from v2 ---------------------------------

def list_files() -> str:
    return "\n".join(p.name for p in WORKSPACE.iterdir()) or "(empty)"


def read_file(filename: str) -> str:
    path = WORKSPACE / filename
    return path.read_text(encoding="utf-8") if path.is_file() else f"error: no {filename}"


def write_file(filename: str, content: str) -> str:
    """Write (or overwrite) a file in the workspace folder."""
    (WORKSPACE / filename).write_text(content, encoding="utf-8")
    return f"wrote {filename}"


LOCAL_TOOLS: dict[str, Callable[..., str]] = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
}

TOOL_SCHEMAS: list[ChatCompletionToolUnionParam] = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in the user's workspace folder.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read one file from the user's workspace folder.",
            "parameters": {
                "type": "object",
                "properties": {"filename": {"type": "string"}},
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write a file in the user's workspace folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filename", "content"],
            },
        },
    },
]


# --- NEW: the MCP component -------------------------------------------------

# which MCP server owns each remote tool (tool name -> live session)
mcp_sessions: dict[str, ClientSession] = {}


async def connect_mcp(stack: AsyncExitStack):
    """Launch each MCP server and merge its tools into TOOL_SCHEMAS."""
    for name, params in MCP_SERVERS.items():
        read, write = await stack.enter_async_context(stdio_client(params))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()

        tools = (await session.list_tools()).tools
        for tool in tools:
            mcp_sessions[tool.name] = session
            TOOL_SCHEMAS.append(
                cast(ChatCompletionToolUnionParam,
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    },
                }
                )
            )
        print(f"  [mcp] connected '{name}': {[t.name for t in tools]}")


async def call_tool(name: str, args: dict) -> str:
    """Run a tool - ours directly, or an MCP server's over the protocol."""
    if name in LOCAL_TOOLS:
        return LOCAL_TOOLS[name](**args)
    result = await mcp_sessions[name].call_tool(name, args)
    return "\n".join(c.text for c in result.content if isinstance(c, TextContent))


# --- the agent loop, unchanged from v2 (just async now) ---------------------

async def run_agent(user_message: str) -> str:
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a helpful personal assistant."},
        {"role": "user", "content": user_message},
    ]
    while True:
        response = await client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOL_SCHEMAS
        )
        message = response.choices[0].message
        if not message.tool_calls:
            return message.content or ""

        messages.append(cast(ChatCompletionAssistantMessageParam, message.to_dict()))
        for call in message.tool_calls:
            if call.type != "function":
                continue
            args = json.loads(call.function.arguments or "{}")
            print(f"  [tool] {call.function.name}({args})")
            result = await call_tool(call.function.name, args)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )


async def main():
    async with AsyncExitStack() as stack:
        await connect_mcp(stack)
        print(f"\nv3 assistant ({MODEL}) with {len(TOOL_SCHEMAS)} tools - ctrl+c to quit")
        try:
            while True:
                question = await asyncio.to_thread(input, "\nyou: ")
                print("\nassistant:", await run_agent(question))
        except (EOFError, KeyboardInterrupt):
            print("\nbye!")


if __name__ == "__main__":
    asyncio.run(main())
