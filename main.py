from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.ocr_processor import procesar_ocr
from controllers.gpt_handler import recomendar_jugada
from models.request_models import ImagenOCR, EstadoJuego
from models.request_models import HistorialEntrada
from db.mongo import guardar_en_historial, obtener_historial

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/guardar_historial")
def guardar(data: HistorialEntrada):
    guardar_en_historial(data.dict())
    return {"mensaje": "✅ Historial guardado"}

@app.get("/historial")
def historial():
    return obtener_historial()

@app.get("/")
def root():
    return {"mensaje": "✅ Backend de PokerBot funcionando correctamente"}

@app.get("/status")
def status():
    return {
        "estado": "activo",
        "mensaje": "🎯 El backend de Railway está corriendo sin errores.",
    }

# ✅ OCR endpoint
@app.post("/ocr")
def ocr_batch(imagenes: ImagenOCR):
    return procesar_ocr(imagenes.imagenes)

# ✅ Recomendación
@app.post("/recomendar")
def recomendar(data: EstadoJuego):
    return recomendar_jugada(data)
