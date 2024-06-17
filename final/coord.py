import math
import random
import requests

# Define las funciones de distancia y evaluación de ruta
def distancia(coord1, coord2):
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(0, len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    # Cierra el ciclo
    ciudad1 = ruta[-1]
    ciudad2 = ruta[0]
    total += distancia(coord[ciudad1], coord[ciudad2])
    return total

# Algoritmo de Simulated Annealing
def simulated_annealing(ruta, coord):
    T = 20
    T_MIN = 0
    V_enfriamiento = 100

    while T > T_MIN:
        dist_actual = evalua_ruta(ruta, coord)
        for _ in range(1, V_enfriamiento):
            # Intercambio aleatorio de dos ciudades
            i = random.randint(0, len(ruta) - 1)
            j = random.randint(0, len(ruta) - 1)
            nueva_ruta = ruta[:]
            nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
            dist_nueva = evalua_ruta(nueva_ruta, coord)
            ap = aceptar_prob(dist_actual, dist_nueva, T)
            if ap > random.random():
                ruta = nueva_ruta
                dist_actual = dist_nueva
        T -= 1
    return ruta

# Función de probabilidad de aceptación
def aceptar_prob(dist_actual, dist_nueva, T):
    return math.exp((dist_actual - dist_nueva) / T)

# Lee las coordenadas desde un archivo
def leer_coordenadas_archivo(nombre_archivo):
    coord = {}
    with open(nombre_archivo) as f:
        for linea in f:
            ciudad, lat, lon = linea.strip().split(",")
            coord[ciudad] = (float(lat), float(lon))
    return coord

def obtener_ruta_ciudades(ciudades):
    coord = {
        'Aguascalientes': [21.87641043660486, -102.26438663286967],
        'BajaCalifornia': [32.5027, -117.00371],
        'BajaCaliforniaSur': [24.14437, -110.3005],
        'Campeche': [19.8301, -90.53491],
        'Chiapas': [16.75, -93.1167],
        'Chihuahua': [28.6353, -106.0889],
        'CDMX': [19.432713075976878, -99.13318344772986],
        'Coahuila': [25.4260, -101.0053],
        'Colima': [19.2452, -103.725],
        'Durango': [24.0277, -104.6532],
        'Guanajuato': [21.0190, -101.2574],
        'Guerrero': [17.5506, -99.5024],
        'Hidalgo': [20.1011, -98.7624],
        'Jalisco': [20.6767, -103.3475],
        'Mexico': [19.285, -99.5496],
        'Michoacan': [19.701400113725654, -101.20829680213464],
        'Morelos': [18.6813, -99.1013],
        'Nayarit': [21.5085, -104.895],
        'NuevoLeon': [25.6714, -100.309],
        'Oaxaca': [17.0732, -96.7266],
        'Puebla': [19.0414, -98.2063],
        'Queretaro': [20.5972, -100.387],
        'QuintanaRoo': [21.1631, -86.8023],
        'SanLuisPotosi': [22.1565, -100.9855],
        'Sinaloa': [24.8091, -107.394],
        'Sonora': [29.0729, -110.9559],
        'Tabasco': [17.9892, -92.9475],
        'Tamaulipas': [25.4348, -99.134],
        'Tlaxcala': [19.3181, -98.2375],
        'Veracruz': [19.1738, -96.1342],
        'Yucatan': [20.967, -89.6237],
        'Zacatecas': [22.7709, -102.5833]
    }
    ruta = list(coord.keys())
    ruta_optima = simulated_annealing(ruta, coord)
    return coord, ruta_optima

if __name__ == "__main__":
    coord, ruta_optima = obtener_ruta_ciudades([])
    for ciudad in ruta_optima:
        print(ciudad, coord[ciudad])
