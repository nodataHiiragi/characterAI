# AIの記憶を管理するための関数
import os
import json
from ollama import chat

# 記憶を保存する関数
def save_memory(character_name, memory):
    # 記憶ディレクトリのパスを作成
    memory_dir = "memories"

    # 記憶ディレクトリの作成
    os.makedirs(memory_dir, exist_ok=True)

    # 記憶をJSON形式で保存
    filename = f"{memory_dir}/{character_name}_memory.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)

# 記憶を読み込む関数
def load_memory(character_name):
    memory_dir = "memories"

    # 記憶ディレクトリの作成
    os.makedirs(memory_dir, exist_ok=True)

    filename = f"{memory_dir}/{character_name}_memory.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            memory = json.load(f)
    else:
        memory = {}

    return memory

# 記憶を更新する関数
def update_memory(memory, new_memory):
    memory.update(new_memory)
    return memory

# 記憶を抽出する関数
def extract_memory(ai_model, ai_messages):
    memory_messages = [
        {
            "role": "system",
            "content": "あなたは長期記憶を整理する役割を持っています。ユーザーについて長期的に記憶しておく価値がある情報だけを抽出してください。"
        },
        {
            "role": "user",
            "content": 
            "以下の会話から「ユーザーについて長期的に覚えておく価値がある情報」だけを抽出してください。\n"
            "出力はJSONオブジェクトのみで返してください。\n"
            "保存してよい情報例\n\n"
            "・好き嫌い\n"
            "・趣味\n"
            "・仕事\n"
            "・居住地域\n"
            "・家族構成\n"
            "・価値観\n"
            "・継続中のプロジェクト\n"  
            "・将来の目標\n\n"
            "保存してはいけない情報例\n\n"
            "・AI自身の状態\n"
            "・AIが覚えているという事実\n"
            "・今回だけの会話内容\n"
            "・一時的な話題\n"
            "・その場の質問\n"
            "・推測\n"
            "説明は禁止。\n"
            "Markdownは禁止。\n"
            "情報がない場合は{}だけ返してください\n\n"
            + json.dumps(ai_messages, ensure_ascii=False, indent=4)
        }
    ]

    response = chat(
        model = ai_model,
        messages = memory_messages
    )

    try:
        memory = json.loads(response.message.content)
    except json.JSONDecodeError:
        print("記憶の抽出に失敗しました。空の記憶を返します。")
        memory = {}

    return memory
