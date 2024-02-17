# README.md

## Environment Setup

### 1. Clone the repository:
```
git clone https://github.com/jangscon/prom_client.git
```

### 2. Run setup.py:
- The script takes two parameters: the path to the image for prediction and the path to save the prediction results.
- Execute setup.sh with parameters as shown in the example below:
  ```bash
  python3 setup.py "/INPUT_PATH" "/OUTPUT_PATH" PortNumber 
  ```
- After this command, Running prom_client.py will start the FastAPI application.
  ```bash
  python3 prom_client.py 
  ```
  
## Testing
### get metrics
- Communication is possible on port 8000. To retrieve metrics, execute the following command using curl on the client:
```bash
curl -o test.txt "http://[ServerIP]:8000/metrics/"
```
- Check test.txt to verify if metrics have been retrieved correctly.

### task requests
- To send a request to the server, execute the following command:
-   This command instructs the server to perform prediction tasks for images numbered 0 to 29.
 ```bash
curl -X POST "http://[ServerIP]:8000/image_predict/0-30"
```