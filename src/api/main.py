# src/api/main.py

from fastapi import FastAPI
import numpy as np
from .schemas import PredictionRequest, PredictionResponse
from .model import get_model
# Importe as configurações
from .config import ANOMALY_THRESHOLD, MIN_POWER, MAX_POWER, TIME_STEPS

app = FastAPI(
    title="AIoT Anomaly Detection API",
    description="API para detectar anomalias em dados de sensores de energia.",
    version="1.0.0"
)

model = get_model()


def scale_value(value, min_val, max_val):
    """Normaliza um valor para a escala [0, 1]."""
    return (value - min_val) / (max_val - min_val)


@app.get("/")
def read_root():
    return {"Status": "API is running!"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_anomaly(request: PredictionRequest):
    """
    Recebe dados de um sensor, pré-processa, executa a inferência
    e retorna se o dado constitui uma anomalia.
    """
    print(f"Dados recebidos para predição: {request.dict()}")

    # 1. Pré-processar o dado recebido
    power_value = request.global_active_power
    scaled_power = scale_value(power_value, MIN_POWER, MAX_POWER)
    print(
        f"Valor Original: {power_value}, Valor Normalizado: {scaled_power:.4f}")

    # 2. Preparar a sequência para o modelo
    # O modelo espera uma sequência de 'TIME_STEPS' (ex: 24). Como a API recebe
    # um ponto de dado por vez, vamos SIMULAR uma sequência onde todos os
    # valores anteriores são iguais ao valor atual.
    # Em um sistema de produção real, teríamos um buffer ou banco de dados
    # para obter os valores reais anteriores.
    sequence = np.full((1, TIME_STEPS, 1), scaled_power)

    # 3. Realizar a inferência (reconstrução)
    reconstructed_sequence = model.predict(sequence)

    # 4. Calcular o erro de reconstrução
    # Calculamos o MAE entre a sequência de entrada e a reconstruída.
    reconstruction_error = np.mean(np.abs(sequence - reconstructed_sequence))
    print(f"Erro de Reconstrução: {reconstruction_error:.4f}")

    # 5. Comparar com o limiar
    is_anomaly = reconstruction_error > ANOMALY_THRESHOLD
    print(f"É anomalia? {is_anomaly}")

    # 6. Retornar a resposta
    response = PredictionResponse(
        is_anomaly=bool(is_anomaly),  # Garante que o tipo é bool nativo
        reconstruction_error=float(reconstruction_error)
    )

    return response
