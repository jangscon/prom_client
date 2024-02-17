import subprocess
import time
from config1 import execution_command


def measure_execution_time(command):
    # Record the start time
    start_time = time.time()
    # Run the command
    process = subprocess.run(command)
    # Ensure the command was executed successfully
    if process.returncode != 0:
        print("Error executing command")
        return None
    # Record the end time
    end_time = time.time()
    # Calculate the execution time
    execution_time = end_time - start_time
    return execution_time


execution_time = measure_execution_time(execution_command)
if execution_time is not None:
    print(f"Execution time: {execution_time} seconds")







