import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def recomendar_jugada(data):
    jugador = data.jugador
    mesa = data.mesa
    rivales = data.rivales

    prompt = f"""
Estás jugando póker y se te presenta la siguiente situación:

Cartas del jugador: {jugador['cartas'][0]['numero']} de {jugador['cartas'][0]['palo']} y {jugador['cartas'][1]['numero']} de {jugador['cartas'][1]['palo']}
Stack: {jugador['stack']} | Apuesta actual: {jugador['apuesta']}
Asiento: {jugador['asiento']} | Botón: {jugador['boton']}

Cartas en mesa:
Flop: {', '.join([f"{c['numero']} de {c['palo']}" for c in mesa['flop']])}
Turn: {mesa['turn']['numero']} de {mesa['turn']['palo']}
River: {mesa['river']['numero']} de {mesa['river']['palo']}

Pote actual: {mesa['pote']}

Rivales:
"""

    for r in rivales:
        prompt += f"- Asiento {r['asiento']}: Stack {r['stack']}, Apuesta {r['apuesta']}\n"

    prompt += "\nCon base en esta información, ¿cuál sería la mejor decisión del jugador? Justifica la respuesta."

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
