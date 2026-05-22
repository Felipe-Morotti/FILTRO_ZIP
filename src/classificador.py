from pathlib import Path
from zipfile import ZipFile
import logging
import filetype
from ver_postscript import tem_postscript

BASE_DIR = Path(__file__).parents[1]
FILTERED_DATA_DIR = BASE_DIR / 'filtered_data'

DICIONARIO_PASTAS: dict[str, Path] = {
    'XML':       FILTERED_DATA_DIR / 'xml',
    'JPEG':      FILTERED_DATA_DIR / 'jpg',
    'PDF_NO_PS': FILTERED_DATA_DIR / 'pdf_no_ps',
    'PDF':       FILTERED_DATA_DIR / 'pdf',
    'QUARENTENA': FILTERED_DATA_DIR / 'quarentena'
}

EXTENSOES_JPEG = {'.jpg', '.jpeg'} 


def salvar_arquivo(logger: logging.Logger, destino: Path, dados: bytes) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(dados)
    logger.info(f"Arquivo salvo em: {destino}")


def quarentenar(logger: logging.Logger, nome: str, extensao: str, dados: bytes) -> None:
    destino = DICIONARIO_PASTAS['QUARENTENA'] / f"{nome}.quarantine"
    salvar_arquivo(logger, destino, dados)
    logger.warning(
        f"Quarentena | '{nome}' rejeitado: "
        f"extensão '{extensao}' não corresponde ao conteúdo real do arquivo."
    )


def validar_formato(dados: bytes, extensao: str) -> bool:
    tipo = filetype.guess(dados)
    if tipo is None:
        return extensao in ('.xml',) and dados.startswith(b'<?xml')

    mapa = {
        '.pdf':  'application/pdf',
        '.jpg':  'image/jpeg',
        '.jpeg': 'image/jpeg',
    }
    return mapa.get(extensao) == tipo.mime


def classificador(logger: logging.Logger, zip_path: Path) -> None:
    with ZipFile(zip_path, 'r') as zipped:
        arquivos = zipped.namelist()
        logger.info(f"ZIP lido. {len(arquivos)} arquivo(s) encontrado(s). \u2705")

        for arquivo in arquivos:
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

            salvar_arquivo(logger, destino, dados)