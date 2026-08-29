import subprocess
from ollama import chat

result = subprocess.run(
    ["git", "diff", "--cached"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

diff = result.stdout
if not diff:
    print("ステージ済みの変更がありません。git addを実行してください。")
    exit()

prompt = f"""
Git差分から、
適切なGitのコミットメッセージのみを生成してください。

ルール:
- コミットメッセージを日本語で生成
- コミットメッセージは50文字以内で要約
- コミットメッセージのみを出力
- 説明文は不要

Git差分:
{diff}
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

commit_message = response.message.content.strip()
print(f"生成されたコミットメッセージ: {commit_message}")

answer = input("このコミットメッセージでコミットしますか？（y/n）:")
if answer.lower() != "y":
    print("コミットをキャンセルしました。")
    exit()

commit_result = subprocess.run(
    ["git", "commit", "-m", commit_message],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

if commit_result.returncode == 0:
    print(f"{commit_message}をコミットしました。")
else:
    print("コミットに失敗しました。")
    exit()

push_result = subprocess.run(
    ["git", "push"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(push_result.stdout)
print(push_result.stderr)

if push_result.returncode == 0:
    print("プッシュ成功しました。")
else:
    print("プッシュに失敗しました。")