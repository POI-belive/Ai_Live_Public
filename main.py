from DeepSeekChat.deepseek_api import deepseek_chat
from DeepSeekChat.deepseek_api_stream import deepseek_chat_stream
from TTS.play_tts import tts

if __name__ == "__main__":
    string_talk1 = "介绍一下小米手机"
    text = deepseek_chat(string_talk1)
    print(text)

    tts(text, character="胡桃")

    string_talk2="和苹果手机比谁更强?"
    text = deepseek_chat(string_talk2)
    print(text)
    tts(text, character="胡桃")
#