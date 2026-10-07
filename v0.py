import io
import sys


if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")

from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="0ldManforgot")
MODEL = "Qwen3.5-4B-4bit"

def chat(user_message: str) -> str:
    response = client.chat.completions.create(
        model = MODEL,
        messages = [
            {"role": "system", "content": "You are a helpful personal assistant."},
            {"role": "user", "content": user_message}
        ],
    )
    return response.choices[0].message.content or ""

if __name__ == "__main__":
    print(f"v0 assistant( {MODEL}) - ctrl+c to quit")
    try:
        while True:
            question = input("\nyou: ")
            print("\nassistant:", chat(question))
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
