from paddleocr import PaddleOCR
import base64
import io
from PIL import Image
import numpy as np

ocr = PaddleOCR(use_angle_cls=False, lang='en')

def procesar_ocr(lista_base64):
    resultados = []

    for idx, img_b64 in enumerate(lista_base64):
        try:
            imagen_bytes = base64.b64decode(img_b64)
            imagen = Image.open(io.BytesIO(imagen_bytes)).convert('RGB')
            img_array = np.array(imagen)

            ocr_result = ocr.ocr(img_array, cls=False)
            if ocr_result and ocr_result[0]:
                texto = ocr_result[0][0][1][0]  # primer bloque detectado
            else:
                texto = ""

            resultados.append(texto.strip())
        except Exception as e:
            print(f"Error OCR img {idx}: {e}")
            resultados.append("")

    return {"textos": resultados}
