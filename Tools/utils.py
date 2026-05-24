from pathlib import Path
import logging
import filetype
import io
from pypdf import PdfReader

BASE_DIR = Path(__file__).parents[1]
FILTERED_DATA_DIR = BASE_DIR / 'filtered_data'
DICIONARIO_PASTAS: dict[str, Path] = {
    'XML':       FILTERED_DATA_DIR / 'xml',
    'JPEG':      FILTERED_DATA_DIR / 'jpg',
    'PDF_NO_PS': FILTERED_DATA_DIR / 'pdf_no_ps',
    'PDF':       FILTERED_DATA_DIR / 'pdf',
    'QUARENTENA': FILTERED_DATA_DIR / 'quarentena'
}


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



def tem_postscript(dados: bytes) -> bool:
    try:
        leitor = PdfReader(io.BytesIO(dados))

        for page in leitor.pages:
            resources = page.get("/Resources")
            if not resources:
                continue

            # Verifica XObjects do subtipo PostScript
            xobjects = resources.get("/XObject", {})
            for obj_ref in xobjects.values():
                obj = obj_ref.get_object()
                if obj.get("/Subtype") == "/PS":
                    return True

            # Verifica fontes Type 1 (PostScript-based)
            fonts = resources.get("/Font", {})
            for font_ref in fonts.values():
                font = font_ref.get_object()
                if font.get("/Subtype") == "/Type1":
                    return True

        return False

    except Exception:
        return False  # PDF corrompido ou ilegível