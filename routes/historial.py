from fastapi import APIRouter
from db.mongo import obtener_historial
from fastapi.responses import JSONResponse
from bson import json_util

router = APIRouter()

@router.get("/historial")
def get_historial():
    historial_data = obtener_historial()
    return JSONResponse(content=json_util.loads(json_util.dumps(historial_data)))
