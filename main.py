from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.ocr_processor import procesar_ocr
from controllers.gpt_handler import recomendar_jugada
from models.request_models import ImagenOCR, EstadoJuego

app = FastAPI()

# Permitir acceso desde cualquier origen (útil para Vercel Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensaje": "✅ Backend de PokerBot funcionando correctamente"}

@app.get("/status")
def status():
    return {
        "estado": "activo",
        "mensaje": "🎯 El backend de Railway está corriendo sin errores.",
    }


#@app.post("/ocr")
#def ocr_batch(imagenes: ImagenOCR):
 #   return procesar_ocr(imagenes.imagenes)

@app.post("/recomendar")
def recomendar(data: EstadoJuego):
    return recomendar_jugada(data)
