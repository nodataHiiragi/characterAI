import os
from ollama import chat
from log import save_log, load_log
from character import select_character, load_character
from ai import chat_with_ai

# キャラクターを選択
character_name = select_character()
# キャラクターのプロンプトを読み込む
character_prompt = load_character(character_name)

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

    response = chat_with_ai(ai_model, ai_messages)

    ai_messages.append(
        {
            "role": "assistant",
            "content": response.message.content
        }
    )

    print(f"{character_name}：" + response.message.content)