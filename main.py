from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#--------------------------------------------------------------

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola desde FastAPI UNICATOLICA!"}

#--------------------------------------------------------------

@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"saludo": f"Hola, {nombre}!"}

#--------------------------------------------------------------

@app.post("/enviar/{dato}")
def recibir_dato(dato: str):
    return {"respuesta": f"Me has enviado: {dato}"}

#--------------------------------------------------------------

class Persona(BaseModel):
    nombre: str
    cedula: str

@app.post("/registrar")
def registrar_persona(persona: Persona):
    return {
        "nombre_recibido": persona.nombre,
        "cedula_recibida": persona.cedula
    }