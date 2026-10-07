import sys
import io

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")

import json
from collections.abc import Callable
from pathlib import Path
from typing import cast

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="0ldManforgot")
MODEL = "Qwen3.5-4B-4bit"

WORKSPACE = Path(__file__).parent / "workspace"
MEMORY_FILE = Path(__file__).parent / "memory.md"


# --- memory: a markdown file, that's it -------------------------------------

def load_memory() -> str:
    if MEMORY_FILE.is_file():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return "(nothing saved yet)"


def save_memory(fact: str) -> str:
    """Append one fact about the user to long-term memory."""
    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- {fact}\n")
    return f"saved: {fact}"


# --- tools ------------------------------------------------------------------

def list_files() -> str:
    return "\n".join(p.name for p in WORKSPACE.iterdir()) or "(empty)"


def read_file(filename: str) -> str:
    path = WORKSPACE / filename
    return path.read_text(encoding="utf-8") if path.is_file() else f"error: no {filename}"


def write_file(filename: str, content: str) -> str:
    """Write (or overwrite) a file in the workspace folder."""
    (WORKSPACE / filename).write_text(content, encoding="utf-8")
    return f"wrote {filename}"


TOOLS: dict[str, Callable[..., str]] = {
    "list_files": list_files,
    "read_file": read_file,
    "save_memory": save_memory,
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
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": (
                "Save one short fact about the user to long-term memory. "
                "Use whenever you learn something worth remembering: their "
                "name, preferences, projects, recurring tasks."
            ),
            "parameters": {
                "type": "object",
                "properties": {"fact": {"type": "string"}},
                "required": ["fact"],
            },
        },
    },
]


SYSTEM_PROMPT = """You are a helpful personal assistant.

Here is what you remember about the user from previous sessions:
{memory}

When you learn a new lasting fact about the user, save it with save_memory."""


def run_agent(messages: list[ChatCompletionMessageParam]) -> str:
    while True:
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOL_SCHEMAS
        )
        message = response.choices[0].message
        if not message.tool_calls:
            messages.append({"role": "assistant", "content": message.content})
            return message.content or ""

        messages.append(cast(ChatCompletionAssistantMessageParam, message.to_dict()))
        for call in message.tool_calls:
            if call.type != "function":
                continue
            args = json.loads(call.function.arguments or "{}")
            print(f"  [tool] {call.function.name}({args})")
            result = TOOLS[call.function.name](**args)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )


if __name__ == "__main__":
    # Conversation history persists across turns now, too.
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT.format(memory=load_memory())}
    ]
    print(f"v4 assistant ({MODEL}) - memory loaded - ctrl+c to quit")
    try:
        while True:
            messages.append({"role": "user", "content": input("\nyou: ")})
            print("\nassistant:", run_agent(messages))
    except (EOFError, KeyboardInterrupt):
        print("\nbye!")
