import requests
import pyaudio


def tts(text, character='default', output_device_index=None):
    stream_url = f"http://127.0.0.1:5000/tts?character={character}&text={text}&stream=true"

    # 初始化pyaudio
    p = pyaudio.PyAudio()

    # 获取音频设备信息
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
        print(f"  Max Input Channels: {device_info['maxInputChannels']}")
        print(f"  Max Output Channels: {device_info['maxOutputChannels']}")
        print(f"  Default Sample Rate: {device_info['defaultSampleRate']}")
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


# 调用案例
if __name__ == "__main__":
    text = "这是一段测试文本，旨在通过多种语言风格和复杂性的内容来全面检验文本到语音系统的性能。"

    # 指定输出设备的索引（根据打印的设备信息选择）
    output_device_index = 5  # 例如，选择索引为2的设备

    tts(text, character="胡桃",output_device_index =output_device_index )

