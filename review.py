import os
import sys
from ollama import chat

if len(sys.argv) < 2:
    print("使い方: python review.py <レビュー対象ファイル>")
    exit()

os.makedirs("reviews", exist_ok=True)

for filename in sys.argv[1:]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"ファイル {filename} が見つかりません。")
        continue


    prompt = f"""
    次のPythonコードをレビューしてください。

    観点：
    - 可読性
    - バグの可能性
    - パフォーマンス
    - 改善案

    コード:

    {code}
    """

    response = chat(
        model="qwen3:14b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    outputbase = os.path.splitext(os.path.basename(filename))[0]
    outputfile = os.path.join("reviews", outputbase + "_review.md")

    with open(outputfile, "w", encoding="utf-8") as f:
        f.write(response.message.content)

    print(f"レビューを{outputfile}に保存しました。")