import os
import json
import datetime
from ollama import chat
from log import save_log

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

d = datetime.date.today()
log_dir = f"logs/{character_name}"

filename = os.path.join("characters", character_list[character_index])
json_files = []

os.makedirs(log_dir, exist_ok=True)

for file in os.listdir(log_dir):
    if file.endswith(".json"):
        json_files.append(file)

with open(filename, "r", encoding="utf-8") as f:
    character_prompt = f.read()

ai_model = "qwen3:14b"

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


while True:
    user_input = input("あなた: ")

    if user_input.lower() in ["exit", "quit"]:
        print("終了します。")
        save_log(character_name, ai_messages)
        #os.makedirs(log_dir, exist_ok=True)
        #files = os.listdir(log_dir)

        #today_numbers =[]

        #for file in files:
        #    if file.startswith(str(d)) and file.endswith(".txt"):
        #        today_numbers.append(int(file.split("_")[1].replace(".txt", "")))


        #if len(today_numbers) == 0:
        #    num = 1
        #else:
        #    num = max(today_numbers) + 1

        #with open(f"{log_dir}/{d}_{num:03}.txt", "w", encoding="utf-8") as f:
        #    for message in ai_messages:
        #        if message["role"] == "user":
        #            f.write(f"あなた: {message['content']}\n")
        #        elif message["role"] == "assistant":
        #            f.write(f"{character_name}: {message['content']}\n")
        #with open(f"{log_dir}/{d}_{num:03}.json", "w", encoding="utf-8") as f:
        #    json.dump(ai_messages, f, ensure_ascii=False, indent=4)
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