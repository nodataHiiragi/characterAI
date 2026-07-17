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