from gpt_handler import recomendar_jugada
from models.historial import guardar_en_historial
from models.request_models import EstadoBasico
from ocr_processor import procesar_ocr

from fastapi import HTTPException
from datetime import datetime

async def procesar_info_plana(payload: EstadoBasico):
    try:
        imagenes = payload.imagenes

        if len(imagenes) != 13:
            raise HTTPException(status_code=400, detail="Se esperaban 13 imágenes: 6 apuestas, 1 pote, 6 stacks")


        # Procesar OCR
        apuestas = [procesar_ocr(img) for img in imagenes[:6]]
        pote = procesar_ocr(imagenes[6])
        stacks = [procesar_ocr(img) for img in imagenes[7:]]

        # Armar estructura
        jugador = {
            "cartas": [],
            "stack": stacks[payload.asiento_jugador - 1] if len(stacks) >= payload.asiento_jugador else "",
            "apuesta": apuestas[payload.asiento_jugador - 1] if len(apuestas) >= payload.asiento_jugador else "",
            "asiento": payload.asiento_jugador,
            "boton": (payload.boton_posicion == payload.asiento_jugador)
        }

        for carta_str in payload.cartas_jugador:
            if " " in carta_str:
                numero, palo = carta_str.split(" ", 1)
                jugador["cartas"].append({"numero": numero, "palo": palo})

        mesa = {"flop": [], "turn": None, "river": None, "pote": pote}
        mesa_cartas = [c for c in payload.cartas_mesa if " " in c]
        mesa_cartas = [{"numero": c.split(" ", 1)[0], "palo": c.split(" ", 1)[1]} for c in mesa_cartas]

        if len(mesa_cartas) >= 3:
            mesa["flop"] = mesa_cartas[:3]
        if len(mesa_cartas) >= 4:
            mesa["turn"] = mesa_cartas[3]
        if len(mesa_cartas) == 5:
            mesa["river"] = mesa_cartas[4]

        rivales = []
        for i in range(6):
            if (i + 1) == payload.asiento_jugador:
                continue
            rivales.append({
                "asiento": i + 1,
                "stack": stacks[i] if i < len(stacks) else "",
                "apuesta": apuestas[i] if i < len(apuestas) else ""
            })

        estado = {
            "timestamp": datetime.utcnow().isoformat(),
            "jugador": jugador,
            "mesa": mesa,
            "rivales": rivales
        }

        respuesta = recomendar_jugada(estado)

        await guardar_en_historial(
            id_mano=estado["timestamp"],
            origen="plano",
            respuesta_gpt=respuesta,
            cartas_jugador=payload.cartas_jugador,
            cartas_mesa=payload.cartas_mesa,
            posicion=payload.boton_posicion
        )

        return {"respuesta": respuesta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")