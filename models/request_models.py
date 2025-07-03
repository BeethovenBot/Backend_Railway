from pydantic import BaseModel
from typing import List, Optional

class ImagenOCR(BaseModel):
    imagenes: List[str]  # Lista de imágenes en base64

class Carta(BaseModel):
    numero: str
    palo: str

class Rival(BaseModel):
    asiento: int
    stack: str
    apuesta: str

class EstadoJuego(BaseModel):
    timestamp: Optional[str]
    jugador: dict  # incluye cartas, stack, apuesta, asiento, boton
    mesa: dict     # incluye flop, turn, river, pote
    rivales: List[Rival]
