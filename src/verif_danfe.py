import xml.etree.ElementTree as ET
import pdfplumber
import io
import re
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
from OCR_DACTE.src import ocr_dacte

NAMESPACE_NFE = 'http://www.portalfiscal.inf.br/nfe'
TAGS_RAIZ_VALIDAS = {'nfeProc', 'NFe'}

MARCADORES_DANFE = [
    'DANFE',
    'DOCUMENTO AUXILIAR DA NOTA FISCAL ELETRÔNICA',
    'DADOS DA NFE'
]

# Chave de acesso: 44 dígitos (pode vir com espaços a cada 4)
REGEX_CHAVE_ACESSO = re.compile(r'\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}'
                                 r'[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}[\s]?\d{4}')


def is_danfe_xml(dados: bytes) -> bool:
    try:
        root = ET.fromstring(dados)
        # Remove o namespace para pegar só o nome da tag
        tag_local = root.tag.split('}')[-1]
        ns = root.tag.split('}')[0].lstrip('{')

        return ns == NAMESPACE_NFE and tag_local in TAGS_RAIZ_VALIDAS
    except ET.ParseError:
        return False
    


def is_danfe_pdf(dados: bytes) -> bool:
    try:
        with pdfplumber.open(io.BytesIO(dados)) as pdf:
            texto = ' '.join(
                page.extract_text() or '' for page in pdf.pages
            ).upper()

        tem_marcador = any(m in texto for m in MARCADORES_DANFE)
        tem_chave = bool(REGEX_CHAVE_ACESSO.search(texto))

        return tem_marcador and tem_chave
    except Exception:
        return False
    



def is_danfe(dados: bytes, extensao: str) -> bool:
    verificadores = {
        '.xml':  is_danfe_xml,
        '.pdf':  is_danfe_pdf,
    }

    verificar = verificadores.get(extensao)
    if not verificar:
        return False

    return verificar(dados)