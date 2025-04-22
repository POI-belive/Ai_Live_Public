import subprocess
import os
import time

def start_tts_api():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(base_dir, "GPT-SoVITS-Inference")
    python_exe = os.path.join(project_dir, "runtime", "python.exe")
    api_script = os.path.join(project_dir, "pure_api.py")

    env = os.environ.copy()
    env["PYTHONPATH"] = project_dir

    print(f"正在使用解释器：{python_exe}")
    print(f"启动 TTS API 脚本：{api_script}")

    process = subprocess.Popen([python_exe, api_script], cwd=project_dir, env=env)
    return process

if __name__ == "__main__":
    print("启动 TTS HTTP 服务...")
    process = start_tts_api()

    print("服务已启动，主程序将保持运行。")

    try:
        while True:
            time.sleep(60)  # 每分钟睡眠一次
    except KeyboardInterrupt:
        print("\n收到退出指令，关闭服务中...")
        process.terminate()
        process.wait()
        print("服务已退出。")
