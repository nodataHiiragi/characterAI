from ollama import chat

ai_model = "qwen3:14b"
ai_messages = [
    {
        "role": "system",
        "content": "あなたは関西弁を話す猫です。"
    }
]

while True:
    user_input = input("あなた: ")

    if user_input.lower() in ["exit", "quit"]:
        print("終了します。")
        break

    print (ai_messages)
    
    ai_messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    
    response = chat(
        model=ai_model,
        messages=ai_messages
    )

    ai_messages.append(
        {
            "role": "assistant",
            "content": response.message.content
        }
    )

    print("猫：" + response.message.content)