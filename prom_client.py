from config import YOLO_INPUT_PATH, YOLO_OUTPUT_PATH, IP, Port

from yolo_image_predict import YOLOJob
from check_result import file_count

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse

from prometheus_client import make_asgi_app
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client.registry import Collector


yolo = YOLOJob()
yolo.set_input_path(YOLO_INPUT_PATH)
yolo.set_output_path(YOLO_OUTPUT_PATH)



# Custom Metric Collector
class CustomCollector(Collector):
    def collect(self):
        yield GaugeMetricFamily('number_of_completed_tasks', 'number_of_completed_tasks', value=file_count(YOLO_OUTPUT_PATH))
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


# POST - Task requests
@app.post("/image_predict/{idxrange}")
async def send_notification(idxrange: str, background_tasks: BackgroundTasks):
    ##################################
    #   idxrange example
    #
    #   1)"0-10" -> iamge[0:10]
    #   2)"100-999" -> iamge[100:999]
    #
    ##################################

    start_idx, end_idx = [int(idx) for idx in idxrange.split("-")]
    yolo.set_start_idx(start_idx)
    yolo.set_end_idx(end_idx)

    background_tasks.add_task(yolo.execute_yolo_predict)
    return {"message": "YOLO image predict execute in the background"}

# @app.post("/request")
# async def request_job(item: Item):
#     return JSONResponse(content={"message": "Image processing started"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host=IP, port=Port)