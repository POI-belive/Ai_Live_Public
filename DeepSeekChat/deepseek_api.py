from openai import OpenAI

#api_key配置初始化
client =OpenAI(api_key="sk-67fa3741d7ae4e55b0446826c06ccc71",base_url="https://api.deepseek.com")

#全局变量，保存上一轮回复
history_messages=""

#deepseek调用
def deepseek_chat(message, model="deepseek-chat", messages=None):
    global history_messages
    #判断初始化对话
    if messages is None:
        messages=[]


    #添加用户对话内容
    messages.append({"role": "user", "content": "你是一个介绍员，请以通俗易懂的语言介绍以下我提出的问题，并尽量将回答控制在100字以内"+ message})

    #添加上一轮回复
    if history_messages:
        messages.append({"role": "user", "content": history_messages})

    #调用api
    response=client.chat.completions.create(
        model=model,
        messages=messages,
        stream = False
    )

    # 获取模型的回复内容
    assistant_message =response.choices[0].message.content

    # 更新全局变量，保存本次的回复内容
    history_messages = assistant_message

    # 打印对话内容
    print(f"User: {message}")
    print(f"Assistant: {assistant_message}")

    return assistant_message

#清除聊天记录
def clear_chat():
    global history_messages
    history_messages=""

#调用案例
if __name__ == "__main__":
    string_talk1 = "介绍一下小米su7"
    deepseek_chat(string_talk1)

    string_talk2="和比亚迪的电车相比有什么优点"
    deepseek_chat(string_talk2)

    clear_chat()

    string_talk3 = "跟特斯拉电车比起来谁更好"
    deepseek_chat(string_talk3)

