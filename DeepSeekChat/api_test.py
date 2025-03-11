# # Please install OpenAI SDK first: `pip3 install openai`
#
# from openai import OpenAI
#
# client = OpenAI(api_key="sk-67fa3741d7ae4e55b0446826c06ccc71", base_url="https://api.deepseek.com")
#
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "千早爱音和墨提斯比呢？"},
#     ],
#     stream=False
# )
#
# print(response.choices[0].message.content)
#