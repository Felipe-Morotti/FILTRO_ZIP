import filetype

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