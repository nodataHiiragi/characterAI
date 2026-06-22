import os
import sys
from ollama import chat

filename = os.path.join("characters", sys.argv[1] + ".txt")

if len(sys.argv) < 2:
    print("使い方: python characterAI.py <character>")
    exit()

with open(filename, "r", encoding="utf-8") as f:
    character_prompt = f.read()

ai_model = "qwen3:14b"
ai_messages = [
    {
        "role": "system",
        "content": character_prompt
    }
]

while True:
    user_input = input("あなた: ")

    if user_input.lower() in ["exit", "quit"]:
        print("終了します。")
        break
    
    ai_messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    
    response = chat(
        model=ai_model,
        messages=ai_messages
    )

    ai_messages.append(
        {
            "role": "assistant",
            "content": response.message.content
        }
    )

    print("assistant：" + response.message.content)