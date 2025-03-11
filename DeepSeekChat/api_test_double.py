# from openai import OpenAI
# client = OpenAI(api_key="sk-67fa3741d7ae4e55b0446826c06ccc71", base_url="https://api.deepseek.com")
#
# # Round 1
# messages = [{"role": "user", "content": "千早爱音和若叶睦谁的吉他水平更强？"}]
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=messages
# )
#
# messages.append(response.choices[0].message)
# print(f"Messages Round 1: {messages}")
#
# # Round 2
# messages.append({"role": "user", "content": "千早爱音跟墨提斯比呢?"})
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=messages
# )
#
# messages.append(response.choices[0].message)
# print(f"Messages Round 2: {messages}")


#