# scripts/publisher.py

import time
import json
import random
from google.cloud import pubsub_v1
import pandas as pd

# --- Configurações ---
# Substitua pelo ID do seu projeto GCP
PROJECT_ID = "129263070097"  
# O nome do tópico que criamos com o Terraform
TOPIC_ID = "aiot-sensor-data" 
# Caminho para o nosso dataset
DATASET_PATH = "data/household_power_consumption.txt"

# --- Inicialização do Cliente Publisher ---
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_message(data):
    """Publica uma única mensagem no tópico Pub/Sub."""
    try:
        # Os dados precisam ser enviados como bytes, então codificamos a string JSON
        future = publisher.publish(topic_path, data=json.dumps(data).encode("utf-8"))
        # O .result() bloqueia até que a mensagem seja publicada com sucesso
        print(f"Publicada mensagem ID: {future.result()}")
    except Exception as e:
        print(f"Ocorreu um erro ao publicar a mensagem: {e}")

def simulate_sensor_data():
    """Lê o dataset e simula o envio de dados de sensores."""
    # Carregando uma pequena amostra do dataset para simulação
    try:
        df = pd.read_csv(
            DATASET_PATH, 
            sep=';', 
            low_memory=False, 
            na_values=['?'],
            nrows=1000  # Pegamos apenas 1000 linhas para a simulação
        )
        df.columns = [
            'Date', 'Time', 'Global_active_power', 'Global_reactive_power', 
            'Voltage', 'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 
            'Sub_metering_3'
        ]
        print("Dataset de simulação carregado.")
    except FileNotFoundError:
        print(f"Erro: Dataset não encontrado em '{DATASET_PATH}'. Verifique o caminho.")
        return

    print("Iniciando simulação de publicação de dados...")
    while True:
        try:
            # Pega uma linha aleatória do nosso dataframe de amostra
            random_row = df.sample(n=1).iloc[0].to_dict()
            
            # Formata a mensagem como um dicionário (JSON)
            message_data = {
                "timestamp": f"{random_row['Date']} {random_row['Time']}",
                "global_active_power": random_row['Global_active_power'],
                "voltage": random_row['Voltage'],
                "sensor_id": f"sensor_{random.randint(1, 10)}" # Adiciona um ID de sensor aleatório
            }
            
            # Publica a mensagem
            publish_message(message_data)
            
            # Espera um pouco para simular o intervalo entre as leituras
            time.sleep(5) 
        except KeyboardInterrupt:
            print("\nSimulação interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"Ocorreu um erro no loop de simulação: {e}")
            time.sleep(5)

if __name__ == "__main__":
    simulate_sensor_data()