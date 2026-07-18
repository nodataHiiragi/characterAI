import os
from ollama import chat
from log import save_log, load_log

character_list = os.listdir("characters")

print("利用可能なキャラクター:")
for i, character in enumerate(character_list):
    print(str(i + 1) + ". " + character.replace(".txt", ""))

character_number = input("キャラクター選択:")

try:
    character_index = int(character_number) - 1
except ValueError:
    print("キャラクター番号を入力してください")
    exit()

character_name = character_list[character_index].replace(".txt", "")

filename = os.path.join("characters", character_list[character_index])

with open(filename, "r", encoding="utf-8") as f:
    character_prompt = f.read()

ai_model = "qwen3:14b"
# 会話ログを読み込む
ai_messages = load_log(character_name, character_prompt)


while True:
    user_input = input("あなた: ")

    if user_input.lower() in ["exit", "quit"]:
        print("終了します。")
        # 会話ログを保存
        save_log(character_name, ai_messages)
        break
    
    ai_messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    print("AI応答待ち...")
    response = chat(
        model=ai_model,
        messages=ai_messages
    )
    print("AI応答受信")

    ai_messages.append(
        {
            "role": "assistant",
            "content": response.message.content
        }
    )

    print(f"{character_name}：" + response.message.content)