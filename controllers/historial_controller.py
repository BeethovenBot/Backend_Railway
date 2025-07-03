from fastapi import APIRouter
from db.mongo import obtener_historial

router = APIRouter()

@router.get("/historial")
def obtener_ultimos_juegos(limit: int = 10):
    data = obtener_historial(limit)
    for doc in data:
        doc["_id"] = str(doc["_id"])  # serializable
    return {"historial": data}
