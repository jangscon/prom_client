import socket
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--image_path", type=str, action="store")          
parser.add_argument("--output_path", type=str, action="store_true")           
parser.add_argument("--port",type=int, default=8000)
args = parser.parse_args()



# IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()

YOLO_INPUT_PATH = args.image_path
YOLO_OUTPUT_PATH = args.output_path
Port = args.Port

with open("config.py","w") as f:
    f.write(f'YOLO_INPUT_PATH = "{YOLO_INPUT_PATH}"')
    f.write(f'YOLO_OUTPUT_PATH = "{YOLO_OUTPUT_PATH}"')
    f.write(f'IP = "{IP}"')
    f.write(f'Port = {Port}')
