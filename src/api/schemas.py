# src/api/schemas.py

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """
    Schema para os dados de entrada da predição.
    Recebemos os dados brutos do sensor.
    """
    global_active_power: float = Field(..., example=2.514,
                                       description="Potência ativa global em kilowatts.")
    voltage: float = Field(..., example=239.1,
                           description="Tensão da rede em volts.")
    # Adicione outros campos se quiser usá-los no futuro.


class PredictionResponse(BaseModel):
    """
    Schema para a resposta da predição.
    """
    is_anomaly: bool = Field(
        ..., description="True se o dado for uma anomalia, False caso contrário.")
    reconstruction_error: float = Field(
        ..., description="O erro de reconstrução calculado pelo modelo.")
