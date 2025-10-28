# src/api/model.py

import tensorflow as tf
import os


class AnomalyModel:
    def __init__(self, model_path: str):
        """
        Inicializa e carrega o modelo de detecção de anomalias.

        Args:
            model_path (str): O caminho para o arquivo do modelo (.h5).
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Arquivo do modelo não encontrado em: {model_path}")

        print(f"Carregando modelo de: {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        print("Modelo carregado com sucesso!")

    def predict(self, data):
        """
        Executa a predição (reconstrução) no modelo.
        """
        return self.model.predict(data)


# --- Carregamento Singleton do Modelo ---
# Para garantir que o modelo seja carregado apenas uma vez, criamos uma instância
# global aqui. O caminho é relativo à raiz do projeto.
MODEL_PATH = "artifacts/lstm_autoencoder_v1.keras"
model_instance = AnomalyModel(model_path=MODEL_PATH)


def get_model():
    """Função para obter a instância única do modelo."""
    return model_instance
