import openai
import os
from models.request_models import EstadoJuego
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def recomendar_jugada(data: EstadoJuego):
    cartas_jugador = data.cartas_jugador or []
    cartas_mesa = data.cartas_mesa or []
    boton = data.boton_posicion
    asiento_jugador = data.asiento_jugador
    pot = data.pot or "Desconocido"
    apuestas = data.apuestas or []
    stacks = data.stacks or []

    # Construcción de texto
    cartas_jugador_str = ", ".join(cartas_jugador) if cartas_jugador else "No detectadas"
    cartas_mesa_str = ", ".join(cartas_mesa) if cartas_mesa else "No hay cartas en mesa"

    stack_jugador = stacks[asiento_jugador - 1] if asiento_jugador and asiento_jugador <= len(stacks) else "Desconocido"
    apuesta_jugador = apuestas[asiento_jugador - 1] if asiento_jugador and asiento_jugador <= len(apuestas) else "Desconocida"

    rivales_str = ""
    for i in range(6):
        if asiento_jugador and (i + 1) == asiento_jugador:
            continue
        stack = stacks[i] if i < len(stacks) else "?"
        apuesta = apuestas[i] if i < len(apuestas) else "?"
        rivales_str += f"- Rival {i+1}: Stack {stack}, Apuesta {apuesta}\n"

    prompt = f"""
Estás jugando póker y se te presenta la siguiente situación:

Cartas del jugador: {cartas_jugador_str}
Stack: {stack_jugador} | Apuesta actual: {apuesta_jugador}
Asiento del jugador: {asiento_jugador} | Posición del botón: {boton}
Pote actual: {pot}

Cartas en mesa: {cartas_mesa_str}

Rivales:
{rivales_str}
Con base en esta información, ¿cuál sería la mejor decisión del jugador? Justifica la respuesta.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres Phil Hellmuth, jugador profesional de póker. Responde como un experto. Comienza tu respuesta con una palabra (Fold, Call o Raise), luego explica brevemente por qué. Usa un tono profesional, claro y conciso."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        texto = response.choices[0].message.content
        return {"resultado": texto}
    except Exception as e:
        return {"error": str(e)}
