import socket
import argparse
import pip
import os
import subprocess


def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def create_directory(directory_path):
    # 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"디렉토리 생성: {directory_path}")
    else:
        print(f"디렉토리 이미 존재: {directory_path}")

install("prometheus-client")
install("uvicorn")
install("fastapi")
install("ultralytics")
install("ffmpeg-python")
install("iperf3")
install("paramiko")
install("scp")

subprocess.Popen(['sudo', 'apt-get', 'install', "iperf3"])


parser = argparse.ArgumentParser()
parser.add_argument("--yolo_input_path", type=str, default="/yolo_input")
parser.add_argument("--yolo_output_path", type=str, default="/yolo_output")
parser.add_argument("--ffmpeg_input_path", type=str, default="/ffmpeg_input")
parser.add_argument("--ffmpeg_output_path", type=str, default="/ffmpeg_output")
parser.add_argument("--port",type=int, default=8000)
parser.add_argument("--process_img",type=int, default=200)

args = parser.parse_args()

# IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()

YOLO_INPUT_PATH = args.yolo_input_path
YOLO_OUTPUT_PATH = args.yolo_output_path
FFMPEG_INPUT_PATH = args.ffmpeg_input_path
FFMPEG_OUTPUT_PATH = args.ffmpeg_output_path
Port = args.port
PROCESS_IMAGE = args.process_img

create_directory(YOLO_OUTPUT_PATH)
create_directory(f"{YOLO_OUTPUT_PATH}/predict")
create_directory(FFMPEG_OUTPUT_PATH)

from computing_measure import get_available_ram, get_network_bandwidth


bandwidth = get_network_bandwidth("155.230.36.27", 5202)
mem = get_available_ram()



with open("config.py","w") as f:
    f.write(f'YOLO_INPUT_PATH = "{YOLO_INPUT_PATH}"\n')
    f.write(f'YOLO_OUTPUT_PATH = "{YOLO_OUTPUT_PATH}"\n')
    f.write(f'FFMPEG_INPUT_PATH = "{FFMPEG_INPUT_PATH}"\n')
    f.write(f'FFMPEG_OUTPUT_PATH = "{FFMPEG_OUTPUT_PATH}"\n')
    f.write(f'BANDWIDTH = {bandwidth}\n')
    f.write(f'MEM = {mem}\n')
    f.write(f'IP = "{IP}"\n')
    f.write(f'Port = {Port}\n')
    f.write(f'IPERF3_IP = "155.230.36.27"\n')
    f.write(f'IPERF3_Port = 5201\n')
    f.write(f'PROCESS_IMAGE = {PROCESS_IMAGE}\n')
