# src/cloud_functions/data_processor/main.py

import base64
import json
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# --- Constantes de Pré-processamento ---
# Estes valores foram obtidos durante a análise no Card 2.
# Em um sistema de produção, eles viriam de um "model registry" ou de um arquivo de configuração.
# Para nosso projeto, defini-los como constantes aqui é suficiente.
# NOTA: Estes são os valores min/max para a coluna 'Global_active_power' APÓS a reamostragem horária.
# Vamos usar valores aproximados baseados na análise geral.
# Idealmente, salvaríamos o scaler treinado, mas para esta fase, isso é mais simples.
MIN_POWER = 0.076
MAX_POWER = 8.42

# Criamos uma instância do scaler que PODE ser ajustada com esses valores.
# No entanto, uma forma mais simples é fazer a matemática diretamente.


def scale_value(value, min_val, max_val):
    """Normaliza um valor para a escala [0, 1] usando os valores min/max conhecidos."""
    return (value - min_val) / (max_val - min_val)


def process_sensor_data(event, context):
    """
    Função acionada por uma mensagem no Pub/Sub.
    Decodifica, pré-processa (normaliza) e imprime a mensagem.
    """
    print(f"ID do Evento: {context.event_id}")

    if 'data' in event:
        # 1. Decodificar a mensagem
        pubsub_message_data = base64.b64decode(event['data']).decode('utf-8')
        message_dict = json.loads(pubsub_message_data)
        print(f"Dados Recebidos: {message_dict}")

        # 2. Extrair o valor relevante
        active_power = message_dict.get('global_active_power')

        if active_power is not None:
            # 3. Pré-processamento: Normalizar o dado
            # Convertendo para float e depois para um array NumPy para o scaler
            try:
                power_value = float(active_power)

                # Usando nossa função de normalização manual
                scaled_power = scale_value(power_value, MIN_POWER, MAX_POWER)

                print(
                    f"Valor Original: {power_value}, Valor Normalizado: {scaled_power:.4f}")

                # Futuramente, este valor normalizado será enviado para a API de inferência.

            except (ValueError, TypeError) as e:
                print(
                    f"Não foi possível processar o valor '{active_power}': {e}")
        else:
            print("Campo 'global_active_power' não encontrado na mensagem.")

    else:
        print("Nenhum dado recebido no evento.")

    return 'Success!'
