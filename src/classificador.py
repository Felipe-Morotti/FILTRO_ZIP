from pathlib import Path
from zipfile import ZipFile
import logging
import sys

BASE_DIR = Path(__file__).parents[1]
sys.path.append(str(BASE_DIR))

from Tools.utils import salvar_arquivo, quarentenar, validar_formato, tem_postscript
FILTERED_DATA_DIR = BASE_DIR / 'filtered_data'

DICIONARIO_PASTAS: dict[str, Path] = {
    'XML':       FILTERED_DATA_DIR / 'xml',
    'JPEG':      FILTERED_DATA_DIR / 'jpg',
    'PDF_NO_PS': FILTERED_DATA_DIR / 'pdf_no_ps',
    'PDF':       FILTERED_DATA_DIR / 'pdf',
    'QUARENTENA': FILTERED_DATA_DIR / 'quarentena'
}

EXTENSOES_JPEG = {'.jpg', '.jpeg'} 



def classificador(logger: logging.Logger, zip_path: Path) -> None:
    with ZipFile(zip_path, 'r') as zipped:
        arquivos = zipped.namelist()
        logger.info(f"ZIP lido. {len(arquivos)} arquivo(s) encontrado(s). \u2705")

        for i, arquivo in enumerate(arquivos, 1):
            path_arquivo = Path(arquivo)
            nome = path_arquivo.name
            ext = path_arquivo.suffix.lower()

            if not nome:
                continue

            dados = zipped.read(arquivo)

            if not validar_formato(dados, ext):
                quarentenar(logger, nome, ext, dados)
                continue

            if ext == '.xml':
                destino = DICIONARIO_PASTAS['XML'] / nome
            
            elif ext in EXTENSOES_JPEG:
                destino = DICIONARIO_PASTAS['JPEG'] / nome

            elif ext == '.pdf':
                if tem_postscript(dados):
                    destino = DICIONARIO_PASTAS['PDF'] / nome
                else:
                    destino = DICIONARIO_PASTAS['PDF_NO_PS'] / nome

            else:
                logger.warning(f"Extensão não reconhecida, ignorando: {nome}")
                continue

            logger.info(f"Arquivo {i} classificado com sucesso. \u2705")

            salvar_arquivo(logger, destino, dados)