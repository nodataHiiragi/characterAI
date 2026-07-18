# キャラクター制御のためのモジュール
import os

# キャラクターを選択する関数
def select_character():
    character_list = os.listdir("characters")

    # キャラクターリストを表示
    print("利用可能なキャラクター:")
    for i, character in enumerate(character_list):
        print(str(i + 1) + ". " + character.replace(".txt", ""))

    character_number = input("キャラクター選択: ")

    # キャラクター番号の入力待機
    try:
        character_index = int(character_number) - 1
    except ValueError:
        print("キャラクター番号を入力してください")
        exit()

    # キャラクター名を取得
    character_name = character_list[character_index].replace(".txt", "")

    return character_name

# キャラクターのプロンプトを読み込む関数
def load_character(character_name):
    # キャラクターのプロンプトファイルを読み込む
    filename = os.path.join("characters", character_name + ".txt")

    # キャラクターのプロンプトを読み込む
    with open(filename, "r", encoding="utf-8") as f:
        character_prompt = f.read()

    return character_prompt
