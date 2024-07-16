from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import threading
import time
import psutil
import scp_client

app = FastAPI()

# 전역 변수 설정
measuring = False
temperatures = []
measure_thread = None

def measure_temperature():
    global measuring
    while measuring:
        # CPU 온도 측정
        temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        temperatures.append(temp)
        time.sleep(1)

@app.post("/start")
async def start_measurement():
    global measuring, measure_thread
    if not measuring:
        measuring = True
        measure_thread = threading.Thread(target=measure_temperature)
        measure_thread.start()
        return JSONResponse(content={"status": "Measurement started"}, status_code=200)
    else:
        return JSONResponse(content={"status": "Measurement already in progress"}, status_code=200)

@app.post("/stop/{filename}")
async def stop_measurement(filename : str):
    global measuring
    if measuring:
        measuring = False
        measure_thread.join()
        # 수집한 온도 값들을 파일로 저장
        filename = filename if filename else 'cpu_temp.txt'
        with open(filename, 'w') as f:
            for temp in temperatures:
                f.write(f"{temp}\n")
        scp_client.send_file_to_remote(matchstring=filename)
        return JSONResponse(content={"status": "Measurement stopped and data saved"}, status_code=200)
    else:
        return JSONResponse(content={"status": "No measurement in progress"}, status_code=200)

@app.get("/status")
async def status():
    return JSONResponse(content={"measuring": measuring, "data_points": len(temperatures)}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
