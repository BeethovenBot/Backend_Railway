from pydantic import BaseModel
from typing import List, Optional

class ImagenOCR(BaseModel):
    imagenes: List[str]

class EstadoJuego(BaseModel):
    cartas_jugador: List[str]
    cartas_mesa: List[str]
    boton_posicion: Optional[int]
    asiento_jugador: Optional[int]
    apuestas: Optional[List[str]]
    pot: Optional[str]
    stacks: Optional[List[str]]
