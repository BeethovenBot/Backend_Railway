from db.mongo import guardar_en_historial
from gpt_handler import recomendar_jugada
from models.request_models import Carta, EstadoJuego, Rival
from datetime import datetime

async def procesar_info_plana(payload: dict):
    # Extraer directamente los campos
    cartas_jugador = payload.get("cartas_jugador", [])
    cartas_mesa = payload.get("cartas_mesa", [])
    boton_posicion = payload.get("boton_posicion", 0)
    asiento_jugador = payload.get("asiento_jugador", 5)
    apuestas = payload.get("apuestas", [])
    pot = payload.get("pot", "")
    stacks = payload.get("stacks", [])

    # Construir cartas
    jugador_cartas = []
    for c in cartas_jugador:
        if " " in c:
            numero, palo = c.split(" ", 1)
            jugador_cartas.append(Carta(numero=numero, palo=palo))

    mesa_cartas = [Carta(numero=c.split(" ", 1)[0], palo=c.split(" ", 1)[1])
                   for c in cartas_mesa if " " in c]

    flop = mesa_cartas[:3]
    turn = mesa_cartas[3] if len(mesa_cartas) > 3 else None
    river = mesa_cartas[4] if len(mesa_cartas) > 4 else None

    jugador = {
        "cartas": jugador_cartas,
        "stack": stacks[asiento_jugador - 1] if len(stacks) >= asiento_jugador else "",
        "apuesta": apuestas[asiento_jugador - 1] if len(apuestas) >= asiento_jugador else "",
        "asiento": asiento_jugador,
        "boton": (boton_posicion == asiento_jugador)
    }

    mesa = {
        "flop": flop,
        "turn": turn,
        "river": river,
        "pote": pot
    }

    rivales = []
    for i in range(6):
        if i + 1 == asiento_jugador:
            continue
        rivales.append(Rival(
            asiento=i + 1,
            stack=stacks[i] if i < len(stacks) else "",
            apuesta=apuestas[i] if i < len(apuestas) else ""
        ))

    estado = EstadoJuego(
        timestamp=datetime.utcnow().isoformat(),
        jugador=jugador,
        mesa=mesa,
        rivales=rivales
    )

    recomendacion = recomendar_jugada(estado)

    await guardar_en_historial(
        id_mano=estado.timestamp,
        origen="plano",
        respuesta_gpt=recomendacion,
        cartas_jugador=[f"{c.numero} {c.palo}" for c in jugador_cartas],
        cartas_mesa=[f"{c.numero} {c.palo}" for c in mesa_cartas],
        posicion=boton_posicion
    )

    return {"resultado": recomendacion}