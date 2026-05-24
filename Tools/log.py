import logging
from pathlib import Path
import time
from contextlib import contextmanager

def set_logger(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("classificacao")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # salva em arquivo
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # também mostra no terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


@contextmanager
def log_timer(logger: logging.Logger, tarefa: str):
    inicio = time.perf_counter()
    logger.info(f"Iniciando: {tarefa} ⏳")
    try:
        yield  # Aqui é onde o código dentro do 'with' será executado
    finally:
        fim = time.perf_counter()
        duracao = fim - inicio
        logger.info(f"Finalizado: {tarefa} | Tempo: {duracao:.2f}s ✅")