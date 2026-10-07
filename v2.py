import sys
import io
import os

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")


import json
from collections.abc import Callable
from pathlib import Path
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

load_dotenv(Path(__file__).resolve().parent / ".env")

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key=os.environ["LOCAL_API_KEY"])
MODEL = "Qwen3.5-4B-4bit"

WORKSPACE = Path(__file__).parent / "workspace"



def list_files() -> str:
    """List the files in the assistant's workspace folder."""
    return "\n".join(p.name for p in WORKSPACE.iterdir()) or "(empty)"


def read_file(filename: str) -> str:
    """Read a file from the workspace folder."""
    path = WORKSPACE / filename
    if not path.is_file():
        return f"error: no file named {filename}"
    return path.read_text(encoding="utf-8")


def write_file(filename: str, content: str) -> str:
    """Write (or overwrite) a file in the workspace folder."""
    (WORKSPACE / filename).write_text(content, encoding="utf-8")
    return f"wrote {filename}"


TOOLS: dict[str, Callable[..., str]] = {
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


def run_agent(user_message: str) -> str:
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": "You are a helpful personal assistant."},
        {"role": "user", "content": user_message},
    ]

    # THE agent loop. This is the whole trick.
    while True:
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOL_SCHEMAS
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or ""  # done - it answered

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
    print(f"v2 agent ({MODEL}) - ctrl+c to quit")
    try:
        while True:
            question = input("\nyou: ")
            print("\nassistant:", run_agent(question))
    except (EOFError, KeyboardInterrupt):
        print("\nbye!")
