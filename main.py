from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from controllers.ocr_processor import procesar_ocr
from controllers.gpt_handler import recomendar_jugada
from models.request_models import ImagenOCR, EstadoJuego
from models.request_models import HistorialEntrada
from db.mongo import guardar_en_historial
from db.mongo import obtener_historial

from bson import json_util

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ocr")
def ocr_batch(imagenes: ImagenOCR):
    return procesar_ocr(imagenes.imagenes)

@app.get("/historial")
def get_historial():
    documentos = obtener_historial()
    return JSONResponse(content=json_util.dumps(documentos), media_type="application/json")


@app.post("/guardar_historial")
def guardar(data: HistorialEntrada):
    guardar_en_historial(data.dict())
    return {"mensaje": "✅ Historial guardado"}

@app.get("/")
def root():
    return {"mensaje": "✅ Backend de PokerBot funcionando correctamente"}

@app.post("/recomendar")
def recomendar(data: EstadoJuego):
    return recomendar_jugada(data)
