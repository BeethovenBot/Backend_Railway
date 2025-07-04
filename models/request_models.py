from pydantic import BaseModel
from typing import List

class EstadoBasico(BaseModel):
    cartas_jugador: List[str]
    cartas_mesa: List[str]
    boton_posicion: int
    asiento_jugador: int
    imagenes: List[str]  # 6 apuestas + 1 pote + 6 stacks