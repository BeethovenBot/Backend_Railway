import json
from pathlib import Path
from utils import hamming_distance

# Ruta del archivo JSON con los vectores de 1 BB
VECTOR_PATH = Path("static/vector1BBBase.json")

# Cargar los vectores al inicio
try:
    with open(VECTOR_PATH, "r") as f:
        vectores_1BB = json.load(f)
except Exception as e:
    print(f"⚠️ Error cargando vector1BBBase.json: {e}")
    vectores_1BB = {}

def es_1BB(vector_entrada, umbral=2):
    if not vectores_1BB:
        return False

    for nombre, vector_base in vectores_1BB.items():
        distancia = hamming_distance(vector_entrada, vector_base)
        print(f"🧪 Comparando con {nombre}: distancia {distancia}")
        if distancia <= umbral:
            return True
    return False
