# AIとの会話をログとして保存、読み込みするための関数
import os
import json
import datetime

# ログを保存する関数
def save_log(character_name, ai_messages):
    # ログディレクトリのパスを作成
    log_dir = f"logs/{character_name}"
    # 今日の日付を取得
    today = datetime.date.today()

    # ログディレクトリの作成
    os.makedirs(log_dir, exist_ok=True)
    files = os.listdir(log_dir)

    # 今日のログファイル番号を取得
    today_numbers = []
    for file in files:
        if file.startswith(str(today)) and file.endswith(".txt"):
            today_numbers.append(int(file.split("_")[1].replace(".txt", "")))

    if len(today_numbers) == 0:
        num = 1
    else:
        num = max(today_numbers) + 1

    # ログファイルに会話を保存
    base_filename = f"{log_dir}/{today}_{num:03}"
    with open(base_filename + ".txt", "w", encoding="utf-8") as f:
        for message in ai_messages:
            if message["role"] == "user":
                f.write(f"あなた: {message['content']}\n")
            elif message["role"] == "assistant":
                f.write(f"{character_name}: {message['content']}\n")

    # ログファイルに会話をJSON形式で保存
    with open(base_filename + ".json", "w", encoding="utf-8") as f:
        json.dump(ai_messages, f, ensure_ascii=False, indent=4)

# ログを読み込む関数
def load_log(character_name, character_prompt):
    log_dir = f"logs/{character_name}"

    # ログディレクトリが存在しない場合は作成
    os.makedirs(log_dir, exist_ok=True)

    # ログディレクトリ内のJSONファイルを取得
    json_files = []
    for file in os.listdir(log_dir):
        if file.endswith(".json"):
            json_files.append(file)

    # ログの存在判定
    if len(json_files) == 0:
        ai_messages = [
            {
                "role": "system",
                "content": character_prompt
            }
        ]
    else:
        latest = max(json_files)

        with open(os.path.join(log_dir, latest), "r", encoding="utf-8") as f:
            ai_messages = json.load(f)

    print(f"読み込んだメッセージ数: {len(ai_messages)}")
    return ai_messages