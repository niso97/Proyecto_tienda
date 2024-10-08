import json
import os

COUNTERS_FILE = 'counters.json'

def load_counters():
    if os.path.exists(COUNTERS_FILE):
        with open(COUNTERS_FILE, 'r') as file:
            return json.load(file)
    return {
        "producto": 0,
        "proveedor": 0,
        "marca": 0,
        "categoria": 0
    }

def save_counters(counters):
    with open(COUNTERS_FILE, 'w') as file:
        json.dump(counters, file)

def generar_codigo_producto():
    counters = load_counters()
    counters["producto"] += 1
    save_counters(counters)
    return f"{counters['producto']:05d}"

def generar_codigo_proveedor():
    counters = load_counters()
    counters["proveedor"] += 1
    save_counters(counters)
    return f"P{counters['proveedor']:04d}"

def generar_codigo_marca():
    counters = load_counters()
    counters["marca"] += 1
    save_counters(counters)
    return f"M{counters['marca']:04d}"

def generar_codigo_categoria():
    counters = load_counters()
    counters["categoria"] += 1
    save_counters(counters)
    return f"C{counters['categoria']:04d}"

# Ejemplos de uso

# print(generar_codigo_producto())   # Ejemplo: 00001
# print(generar_codigo_proveedor())  # Ejemplo: P0001
# print(generar_codigo_marca())      # Ejemplo: M0001
# print(generar_codigo_categoria())  # Ejemplo: C0001
