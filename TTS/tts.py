import threading

import requests
import pyaudio


def tts(text, character='default', output_device_index=None):
    stream_url = f"http://127.0.0.1:5000/tts?character={character}&text={text}&stream=true"

    # 初始化pyaudio
    p = pyaudio.PyAudio()

    # 获取音频设备信息
    info = p.get_host_api_info_by_index(0)
    device_count = info.get('deviceCount')

    print("输出可用设备列表：")
    for i in range(device_count):
        dev = p.get_device_info_by_host_api_device_index(0, i)
        if dev["maxOutputChannels"] > 0:
            print(f"Device {i}: {dev['name']}")
            print(f"  Max Output Channels: {dev['maxOutputChannels']}")
            print(f"  Default Sample Rate: {dev['defaultSampleRate']}")
            print("-" * 40)

    # 如果没有指定输出设备，使用默认设备
    if output_device_index is None:
        output_device_index = p.get_default_output_device_info()['index']

    # 打开音频流，指定输出设备
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=32000,
                    output=True,
                    output_device_index=output_device_index)

    # 使用requests获取音频流
    response = requests.get(stream_url, stream=True)

    # 读取数据块并播放
    for data in response.iter_content(chunk_size=1024):
        stream.write(data)

    # 停止和关闭流
    stream.stop_stream()
    stream.close()

    # 终止pyaudio
    p.terminate()

# def tts_multi_output(text, character='default', output_device_index=None):
#     stream_url = f"http://127.0.0.1:5000/tts?character={character}&text={text}&stream=true"
#
#     # 初始化pyaudio
#     p = pyaudio.PyAudio()
#
#     # 获取默认输出设备索引
#     default_index = p.get_default_output_device_info()['index']
#
#     # 如果没有指定设备，就只使用默认设备
#     if output_device_index is None or output_device_index == default_index:
#         output_device_index = None  # 避免重复打开相同设备
#
#     # 打开默认输出设备的音频流
#     default_stream = p.open(format=p.get_format_from_width(2),
#                             channels=1,
#                             rate=32000,
#                             output=True,
#                             output_device_index=default_index)
#
#     # 如果有指定另一个设备，就也打开
#     second_stream = None
#     if output_device_index is not None:
#         second_stream = p.open(format=p.get_format_from_width(2),
#                                channels=1,
#                                rate=32000,
#                                output=True,
#                                output_device_index=output_device_index)
#
#     # 请求一次音频流
#     response = requests.get(stream_url, stream=True)
#
#     # 播放到两个设备
#     for data in response.iter_content(chunk_size=1024):
#         default_stream.write(data)
#         if second_stream:
#             second_stream.write(data)
#
#     # 停止和关闭流
#     default_stream.stop_stream()
#     default_stream.close()
#
#     if second_stream:
#         second_stream.stop_stream()
#         second_stream.close()
#
#     p.terminate()


# 调用案例
if __name__ == "__main__":
    text = "这是一段测试文本，旨在通过多种语言风格和复杂性的内容来全面检验文本到语音系统的性能。"

    # 指定输出设备的索引
    output_device_index = 5  # 例如，选择索引为2的设备

    tts(text, character="胡桃",output_device_index =output_device_index )
    # tts_multi_output(text, character="胡桃", output_device_index=output_device_index)

#事实证明，对于直播来说，根本不需要虚拟声卡传递音频，直播软件会直接收取设备默认播放设备的音频
#这段代码先保留，也许以后用得到
