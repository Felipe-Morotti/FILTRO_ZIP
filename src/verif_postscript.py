import io
from pypdf import PdfReader

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