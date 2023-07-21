import numpy as np
import torch
from torchvision.models import inception_v3, Inception_V3_Weights
import time
import psutil
import mlflow

# Load the Inception model
model = inception_v3(weights=Inception_V3_Weights.DEFAULT)
model.eval()

# Define a function to measure latency
def measure_latency(model):
    input_data = torch.randn(1, 3, 229, 229) # Example input data
    start_time = time.time()
    _ = model(input_data)
    latency = time.time() - start_time
    return latency

# Define a function to monitor hardware usage
def monitor_hardware ():
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    return cpu_percent , memory_percent

# Start an MLflow run
with mlflow.start_run():

    # Log the model parameters to MLflow
    model_params = {
        name: value for name, value in vars(model).items() if np.isscalar(value)
    }
    mlflow.log_params(model_params)

    # Monitor hardware usage and log metrics to MLflow
    while True:
        cpu_percent, memory_percent = monitor_hardware()

        latency = measure_latency(model)

        # Log metrics to MLflow
        mlflow.log_metric("CPU Usage", cpu_percent)
        mlflow.log_metric("Memory Usage", memory_percent)
        mlflow.log_metric("Latency", latency)

        # Sleep for some time before the next monitoring iteration
        time.sleep(10)
