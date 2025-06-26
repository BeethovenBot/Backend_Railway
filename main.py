from fastapi import FastAPI
from pydantic import BaseModel
import easyocr
import base64
import numpy as np
import cv2

app = FastAPI()

lector = easyocr.Reader(['en'], gpu=False)

class ImagenOCR(BaseModel):
    imagen: str  # base64 sin prefijo

@app.post("/ocr")
def ocr(imagen_ocr: ImagenOCR):
    try:
        # Decodificar base64
        img_bytes = base64.b64decode(imagen_ocr.imagen)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Procesar con EasyOCR
        resultados = lector.readtext(img, detail=0)
        texto_detectado = ' '.join(resultados)

        return {"texto": texto_detectado}
    except Exception as e:
        return {"error": str(e)}

# --------------------------------------------------------------

@app.get("/")
def read_root():
    return {"mensaje": "¡Funcionando!"}

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"saludo": f"Hola, {nombre}!"}

@app.post("/enviar/{dato}")
def recibir_dato(dato: str):
    return {"respuesta": f"Me has enviado: {dato}"}

class Persona(BaseModel):
    nombre: str
    cedula: str

@app.post("/registrar")
def registrar_persona(persona: Persona):
    return {
        "nombre_recibido": persona.nombre,
        "cedula_recibida": persona.cedula
    }
