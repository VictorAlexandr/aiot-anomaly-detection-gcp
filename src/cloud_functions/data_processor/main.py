# src/cloud_functions/data_processor/main.py

import base64
import json


def process_sensor_data(event, context):
    """
    Função acionada por uma mensagem no Pub/Sub.
    Apenas decodifica e imprime a mensagem recebida.
    """
    print(f"ID do Evento: {context.event_id}")
    print(f"Tipo do Evento: {context.event_type}")

    # A mensagem do Pub/Sub vem codificada em Base64 no campo 'data'
    if 'data' in event:
        pubsub_message_data = base64.b64decode(event['data']).decode('utf-8')
        print(f"Dados Recebidos: {pubsub_message_data}")

        # Convertendo a string JSON de volta para um dicionário Python
        message_dict = json.loads(pubsub_message_data)

        # Aqui é onde, no futuro, faremos o pré-processamento e a chamada para a API de inferência.
        # Por enquanto, apenas confirmamos o recebimento.
        print(
            f"Processando dados para o sensor: {message_dict.get('sensor_id')}")

    else:
        print("Nenhum dado recebido no evento.")

    return 'Success!'
