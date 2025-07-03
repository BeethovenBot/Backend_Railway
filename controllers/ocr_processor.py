import easyocr
import base64
import io
from PIL import Image
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def procesar_ocr(lista_base64):
    resultados = []

    for img_b64 in lista_base64:
        try:
            imagen_bytes = base64.b64decode(img_b64)
            imagen = Image.open(io.BytesIO(imagen_bytes)).convert('RGB')

            resultado = reader.readtext(np.array(imagen), detail=0, paragraph=False)
            texto = resultado[0] if resultado else ""
            resultados.append(texto.strip())

        except Exception as e:
            print(f"Error procesando imagen: {e}")
            resultados.append("")

    return {"textos": resultados}
