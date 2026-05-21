from pathlib import Path
import logging
import sys
from classificador import classificador

BASE_DIR = Path(__file__).parents[1]
sys.path.append(str(BASE_DIR))

from Tools.utils import set_logger
from Tools.utils import log_timer

RAW_DATA_DIR = BASE_DIR / 'raw_data'      
RAW_DATA_PATH = RAW_DATA_DIR / 'hospede_do_zip' / 'arquivos_genericos.zip'

FILTERED_DATA_DIR = BASE_DIR / 'filtered_data'

LOG_PATH = BASE_DIR / 'log_register' / 'classificacao.log'

logger_pronto = set_logger(LOG_PATH)

def main(logger: logging.Logger) -> None:
    classificador(logger_pronto, RAW_DATA_PATH)


if __name__ == "__main__":
    main(logger_pronto)