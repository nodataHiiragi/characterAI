import os
from ollama import chat

character_list = os.listdir("characters")

print("利用可能なキャラクター:")
for i, character in enumerate(character_list):
    print(str(i + 1) + ". " + character.replace(".txt", ""))

character_number = input("キャラクター選択:")
character_name = character_list[int(character_number) - 1].replace(".txt", "")

try:
    character_index = int(character_number) - 1
except ValueError:
    print("キャラクター番号を入力してください")
    exit()

filename = os.path.join("characters", character_list[character_index])

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

    print(f"{character_name}：" + response.message.content)