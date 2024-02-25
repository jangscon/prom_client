from config import YOLO_INPUT_PATH, YOLO_OUTPUT_PATH, FFMPEG_INPUT_PATH, FFMPEG_OUTPUT_PATH, IP, Port, IPERF3_IP, IPERF3_Port, BANDWIDTH, MEM, CPU
from yolo_image_predict import YOLOJob
from ffmpeg_video_size_reduction import FFMpegJob

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse

from prometheus_client import make_asgi_app
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client.registry import Collector

from computing_measure import get_network_bandwidth, get_cpu_utility, get_available_ram

yolo = YOLOJob()
yolo.set_input_path(YOLO_INPUT_PATH)
yolo.set_output_path(YOLO_OUTPUT_PATH)

total_output_image = 0

mpeg = FFMpegJob()
mpeg.set_input_path(FFMPEG_INPUT_PATH)
mpeg.set_output_path(FFMPEG_OUTPUT_PATH)


# def set_total_output_image():
#     global total_output_image
#     total_output_image += file_count(f"{YOLO_OUTPUT_PATH}/{yolo.current_dir}")
#     return total_output_image

# Custom Metric Collector
class CustomCollector(Collector):
    def collect(self):
        # yield GaugeMetricFamily('number_of_completed_tasks', 'number_of_completed_tasks', value=set_total_output_image())
        yield GaugeMetricFamily('yolo_predict_task_status', 'True == Done, False == Not yet', value=yolo.operation_status)
        # c = CounterMetricFamily('my_counter_total', 'Help text', labels=['foo'])
        # c.add_metric(['bar'], 1.7)
        # c.add_metric(['baz'], 3.8)
        # yield c
REGISTRY.register(CustomCollector())


# GET - metric exporter
# Create app
app = FastAPI(debug=False)
# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app(REGISTRY)
app.mount("/metrics", metrics_app)

@app.get("/update_computing_measure")
async def send_notification():
    bandwidth = get_network_bandwidth(IPERF3_IP, IPERF3_Port)
    RAM = get_available_ram()
    cpu = get_cpu_utility()
    return {"network_latency": bandwidth, "cpu" : cpu, "memory" : RAM}

@app.get("/computing_measure")
async def send_notification():
    return {"network_latency": BANDWIDTH, "cpu" : CPU, "memory" : MEM}

@app.get("/video_resize/{idxrange}")
async def send_notification(idxrange: str):
    start_idx, end_idx = [int(idx) for idx in idxrange.split("-")]
    mpeg.set_start_idx(start_idx)
    mpeg.set_end_idx(end_idx)

    result = mpeg.vid_resize()
    return {
        "result" : result
    }



@app.get("/image_predict/{idxrange}")
async def send_notification(idxrange: str):
    start_idx, end_idx = [int(idx) for idx in idxrange.split("-")]
    yolo.set_start_idx(start_idx)
    yolo.set_end_idx(end_idx)

    result = yolo.execute_yolo_predict()
    return {
        "result" : result
    }




if __name__ == "__main__":
    uvicorn.run(app, host=IP, port=Port)