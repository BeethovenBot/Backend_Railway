from typing import List, Optional
from pydantic import BaseModel

class Rival(BaseModel):
    asiento: int
    apuesta: str
    stack: str

class HistorialJugada(BaseModel):
    id_mano: str
    respuesta_gpt: str
    origen: str
    cartas_jugador: List[str]
    cartas_mesa: List[str]
    posicion: str
    stack_jugador: str
    apuesta_jugador: str
    pote: str
    rivales: List[Rival]
