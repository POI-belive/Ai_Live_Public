from openai import OpenAI

# api_key配置初始化
client = OpenAI(api_key="sk-67fa3741d7ae4e55b0446826c06ccc71", base_url="https://api.deepseek.com")

# deepseek调用（支持流式对话）
def deepseek_chat_stream(message, model="deepseek-chat", messages=None):
    # 判断初始化对话
    if messages is None:
        messages = []

    # 添加用户对话内容
    messages.append({"role": "user", "content": message})

    # 调用api，启用流式响应
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True  # 启用流式响应
    )

    # 处理流式响应
    assistant_message_content = ""
    print("Assistant: ", end="", flush=True)  # 实时输出
    for chunk in response:
        if chunk.choices[0].delta.content:  # 检查是否有内容
            content = chunk.choices[0].delta.content
            assistant_message_content += content
            print(content, end="", flush=True)  # 实时输出

    # 将完整的回复添加到 messages 中
    messages.append({"role": "assistant", "content": assistant_message_content})

    # 返回完整的回复和更新后的 messages
    return assistant_message_content, messages


# 调用案例
if __name__ == "__main__":
    # 第一轮对话
    string_talk1 = "介绍一下小米su7"
    response1, messages = deepseek_chat_stream(string_talk1)

    # 第二轮对话
    string_talk2 = "小米su7和比亚迪的电车相比有什么优点"
    response2, messages = deepseek_chat_stream(string_talk2, messages=messages)

    # 第三轮对话
    string_talk3 = "小米su7跟特斯拉电车比起来谁更好"
    response3, messages = deepseek_chat_stream(string_talk3, messages=messages)
