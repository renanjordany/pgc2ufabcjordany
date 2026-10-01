import math
import random

def calcular_limiar(m: int, epsilon: float, delta: float) -> int:
    if m <= 0 or epsilon <= 0 or delta <= 0:
        return 1
    val = (12.0 / (epsilon ** 2)) * math.log2((8.0 * m) / delta)
    return math.ceil(val)

def algoritmo_1_estimador_f0(fluxo: list, epsilon: float, delta: float):
    m = len(fluxo)
    if m == 0:
        return 0.0

    limite = calcular_limiar(m, epsilon, delta)
    p = 1.0
    conjunto_x = set()

    for item in fluxo:
        conjunto_x.discard(item)
        if random.random() < p:
            conjunto_x.add(item)

        if len(conjunto_x) == limite:
            conjunto_x = {elem for elem in conjunto_x if random.random() >= 0.5}
            p = p / 2.0
            if len(conjunto_x) == limite:
                return None

    return len(conjunto_x) / p

def algoritmo_2_relaxado(fluxo: list, epsilon: float, delta: float):
    m = len(fluxo)
    if m == 0:
        return 0.0

    limite = calcular_limiar(m, epsilon, delta)
    p = 1.0
    conjunto_x = set()

    for item in fluxo:
        conjunto_x.discard(item)
        if random.random() < p:
            conjunto_x.add(item)

        if len(conjunto_x) == limite:
            conjunto_x = {elem for elem in conjunto_x if random.random() >= 0.5}
            p = p / 2.0

    return len(conjunto_x) / p

def contar_distintos_exato(fluxo: list) -> int:
    return len(set(fluxo))