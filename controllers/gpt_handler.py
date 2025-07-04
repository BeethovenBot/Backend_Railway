import openai
import os
from models.request_models import EstadoJuego
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def recomendar_jugada(data: EstadoJuego):
    cartas_jugador = data.cartas_jugador
    cartas_mesa = data.cartas_mesa
    boton = data.boton_posicion
    pot = data.pot
    apuestas = data.apuestas
    stacks = data.stacks

    # Construir descripción de cartas del jugador
    cartas_jugador_str = f"{cartas_jugador[0]['numero']} de {cartas_jugador[0]['palo']} y {cartas_jugador[1]['numero']} de {cartas_jugador[1]['palo']}"

    # Construir descripción de cartas en mesa
    flop = cartas_mesa.get('flop', [])
    flop_str = ', '.join([f"{c['numero']} de {c['palo']}" for c in flop]) if flop else "No hay flop"
    turn = cartas_mesa.get('turn')
    turn_str = f"{turn['numero']} de {turn['palo']}" if turn else "No hay turn"
    river = cartas_mesa.get('river')
    river_str = f"{river['numero']} de {river['palo']}" if river else "No hay river"

    # Construir descripción de rivales
    rivales_str = ""
    for i, (stack, apuesta) in enumerate(zip(stacks, apuestas)):
        rivales_str += f"- Rival {i+1}: Stack {stack}, Apuesta {apuesta}\n"

    prompt = f"""
Estás jugando póker y se te presenta la siguiente situación:

Cartas del jugador: {cartas_jugador_str}
Stack: {stacks[0]} | Apuesta actual: {apuestas[0]}
Posición del botón: {boton}

Cartas en mesa:
Flop: {flop_str}
Turn: {turn_str}
River: {river_str}

Pote actual: {pot}

Rivales:
{rivales_str}
Con base en esta información, ¿cuál sería la mejor decisión del jugador? Justifica la respuesta.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres Phil Hellmuth, jugador profesional de póker. Responde como un experto. Comienza tu respuesta con una palabra (Fold, Call o Raise), luego explica brevemente por qué. Mantén un tono profesional y claro."},
                {"role": "user", "content": prompt}
            ]
        )
        texto = response.choices[0].message.content
        return {"recomendacion": texto}
    except Exception as e:
        return {"error": str(e)}
