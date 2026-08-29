import os
import json
from ollama import chat
from log import save_log, load_log
from character import select_character, load_character
from ai import chat_with_ai
from memory import save_memory, load_memory, update_memory, extract_memory

ai_model = "qwen3:14b"
# キャラクターを選択
character_name = select_character()
# キャラクターのプロンプトを読み込む
character_prompt = load_character(character_name)

# 記憶を読み込む
ai_memory = load_memory(character_name)

character_prompt += (
    "\n\n## ユーザーについて覚えている情報\n"
    "この情報を会話に自然に活用してください。\n\n"
    + json.dumps(ai_memory, ensure_ascii=False, indent=4))

ai_messages = [
    {
        "role": "system",
        "content": character_prompt
    }
]

# 会話ログを読み込む
ai_messages.extend(load_log(character_name))


while True:
    user_input = input("あなた: ")

    # 終了コマンドの判定
    if user_input.lower() in ["exit", "quit"]:
        print("終了します。")
        # 会話ログを保存
        save_log(character_name, ai_messages)
        # 記憶を更新
        #ai_memory = update_memory(ai_memory, extract_memory(ai_model, ai_messages))
        #save_memory(character_name, ai_memory)
        ai_memory = extract_memory(ai_model, ai_messages)

        print("記憶候補:")
        print(json.dumps(ai_memory, ensure_ascii=False, indent=4))
        break

    # ユーザーの入力を会話ログに追加
    ai_messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # AIに会話を送って応答を受け取る
    response = chat_with_ai(ai_model, ai_messages)

    # AIの応答を会話ログに追加
    ai_messages.append(
        {
            "role": "assistant",
            "content": response.message.content
        }
    )

    # AIの応答を表示
    print(f"{character_name}：" + response.message.content)