from ultralytics import YOLO
import os
from utils import count_files_in_directory
import time 

class YOLOJob:
    def __init__(self):
        self.latency = 0
        self.operation_status = False
        self.input_path = None
        self.output_path = None
        self.start_idx = None
        self.end_idx = None
        self.current_dir = None

    def set_input_path(self,input_path):
        self.input_path = input_path 
        self.dir_list = int(count_files_in_directory(input_path))
    def set_output_path(self,output_path):
        self.output_path = output_path    
        self.current_dir = "predict"
    def set_start_idx(self,start_idx):
        self.start_idx = start_idx
    def set_end_idx(self,end_idx):
        self.end_idx = end_idx
    
    def switch_operation_status(self):
        self.operation_status += 1
    def get_image_list(self, startidx, endidx):
        return [ f"{self.input_path}/{i}" for i in os.listdir(self.input_path)[startidx:endidx]]
    
    def execute_yolo_predict(self) :
        try:
            start = time.time()
            dircheck = self.current_dir.split("t")
            if dircheck[1] == '' :
                self.current_dir = "predict2"
            else:
                self.current_dir = f"predict{int(dircheck[1])+1}"
            model = YOLO("yolov8n.pt") 
            model.predict(source=self.get_image_list(self.start_idx, self.end_idx),project=self.output_path, save=True)
            self.switch_operation_status()
            return None, time.time() - start
        except Exception as e:
            return e, time.time() - start
