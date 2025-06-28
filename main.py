from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import base64
import numpy as np
import cv2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lector = easyocr.Reader(['en'], gpu=False)

class ImagenOCR(BaseModel):
    imagenes: list[str]  # Lista de imágenes en base64 sin prefijo

@app.post("/ocr")
def ocr_batch(imagen_ocr: ImagenOCR):
    try:
        def procesar_imagen(base64_img):
            try:
                img_bytes = base64.b64decode(base64_img)
                nparr = np.frombuffer(img_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                resultados = lector.readtext(img, detail=0)
                return ' '.join(resultados)
            except Exception as e:
                return f"ERROR: {str(e)}"

        resultados = [procesar_imagen(img) for img in imagen_ocr.imagenes]
        return {"textos": resultados}
    except Exception as e:
        return {"error": str(e)}

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
