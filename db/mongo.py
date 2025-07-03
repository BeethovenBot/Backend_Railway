from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["pokerbot"]
historial = db["historial"]

def guardar_en_historial(data: dict):
    historial.insert_one(data)

def obtener_historial(limit=10):
    documentos = historial.find().sort("createdAt", -1).limit(limit)
    return list(documentos)
