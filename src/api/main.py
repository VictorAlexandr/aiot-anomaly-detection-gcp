# src/api/main.py

from fastapi import FastAPI, status, Request
import numpy as np
import time

# Importe o nosso logger configurado
from .logger_config import log

from .schemas import PredictionRequest, PredictionResponse
from .model import get_model
from .config import ANOMALY_THRESHOLD, MIN_POWER, MAX_POWER, TIME_STEPS

app = FastAPI(
    title="AIoT Anomaly Detection API",
    description="API para detectar anomalias em dados de sensores de energia.",
    version="1.0.0"
)

model = get_model()

# (função scale_value permanece a mesma)
def scale_value(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

# Adicionando um middleware para logar todas as requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    log.info(
        "request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time_ms": f"{process_time:.2f}"
        }
    )
    return response

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health_check():
    log.info("Health check endpoint was called.")
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"Status": "API is running!"}

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_anomaly(request: PredictionRequest):
    # Substituindo print() por log.info() com informações estruturadas
    log.info("prediction request received", extra={"request_data": request.dict()})

    power_value = request.global_active_power
    scaled_power = scale_value(power_value, MIN_POWER, MAX_POWER)
    
    sequence = np.full((1, TIME_STEPS, 1), scaled_power)
    reconstructed_sequence = model.predict(sequence)
    
    reconstruction_error = np.mean(np.abs(sequence - reconstructed_sequence))
    is_anomaly = reconstruction_error > ANOMALY_THRESHOLD

    response_data = {
        "is_anomaly": bool(is_anomaly),
        "reconstruction_error": float(reconstruction_error)
    }
    log.info("prediction result", extra=response_data)
    
    return PredictionResponse(**response_data)