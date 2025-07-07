from fastapi import APIRouter
from db.mongo import obtener_historial
from fastapi.responses import JSONResponse
from bson import json_util

router = APIRouter()

@router.get("/api/historial")
def get_historial():
    historial_data = obtener_historial()
    # Usar json_util para convertir ObjectId y datetime
    return JSONResponse(content=json_util.loads(json_util.dumps(historial_data)))
