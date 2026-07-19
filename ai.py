from ollama import chat

# AIモデルに会話を送って応答を受け取る
def chat_with_ai(ai_model, ai_messages):
    print("AI応答待ち…")
    # AIに会話を送って応答を受け取る
    response = chat(
        model=ai_model,
        messages=ai_messages
    )
    print("AI応答受信")

    return response