# src/api/logger_config.py

import logging
from pythonjsonlogger import jsonlogger

def setup_logger():
    """Configura o logger para emitir logs em formato JSON."""
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.INFO)
    
    # Evita adicionar múltiplos handlers se a função for chamada mais de uma vez
    if not logger.handlers:
        logHandler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
    
    return logger

# Cria uma instância única do logger para ser importada por outros módulos
log = setup_logger()