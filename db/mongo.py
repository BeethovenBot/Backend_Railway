from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = MongoClient(os.getenv("MONGO_URL"))
db = client["pokerbot"]
historial = db["historial"]

def guardar_en_historial(datos):
    datos["timestamp"] = datetime.utcnow().isoformat()
    historial.insert_one(datos)

def obtener_historial(limit=10):
    documentos = historial.find().sort("timestamp", -1).limit(limit)
    resultado = list(documentos)
    print("📋 Historial obtenido:", resultado)
    return resultado


