from coord import obtener_coordenadas
import folium
import networkx as nx
import os

def crear_mapa(ruta, coordenadas_ciudades, nombre_archivo="mapa.html"):
    # Crear un objeto de mapa centrado en las coordenadas medias
    centro_mapa = [21.87641043660486, -102.26438663286967]
    mapa = folium.Map(location=centro_mapa, zoom_start=5)

    # Añadir marcadores para cada ciudad
    for ciudad, coords in coordenadas_ciudades.items():
        folium.Marker(location=coords, popup=ciudad).add_to(mapa)

    # Dibujar la ruta en el mapa si existe
    if ruta:
        coordenadas_ruta = [coordenadas_ciudades[ciudad] for ciudad in ruta]
        folium.PolyLine(locations=coordenadas_ruta, color="blue").add_to(mapa)

    # Guardar el mapa en un archivo HTML
    mapa.save(nombre_archivo)
    return nombre_archivo

def generar_camino_mas_corto(ciudades, coordenadas_ciudades, ciudad_inicio, ciudad_destino):
    # Crear un grafo
    G = nx.Graph()

    # Añadir nodos al grafo
    for ciudad in ciudades:
        G.add_node(ciudad, pos=coordenadas_ciudades[ciudad])

    # Añadir aristas con distancias geográficas entre todas las ciudades
    for i, ciudad1 in enumerate(ciudades):
        for ciudad2 in ciudades[i+1:]:
            coord1 = coordenadas_ciudades[ciudad1]
            coord2 = coordenadas_ciudades[ciudad2]
            distancia = nx.linalg.norm([coord1[0] - coord2[0], coord1[1] - coord2[1]])
            G.add_edge(ciudad1, ciudad2, weight=distancia)

    # Calcular el camino más corto
    camino_mas_corto = nx.shortest_path(G, source=ciudad_inicio, target=ciudad_destino, weight='weight')
    return camino_mas_corto

def generar_mapa_html(ciudad_inicio, ciudad_destino, nombre_archivo="mapa.html"):
    ciudades = ["Aguascalientes", "Zacatecas", "Guadalajara", "Monterrey"]
    coordenadas_ciudades = {
        "Aguascalientes": [21.87641043660486, -102.26438663286967],
        "Zacatecas": [22.77085517480739, -102.58317855537285],
        "Guadalajara": [20.6743626, -103.3870785],
        "Monterrey": [25.6866142, -100.3161126]
    }

    # Obtener el camino más corto
    camino_mas_corto = generar_camino_mas_corto(ciudades, coordenadas_ciudades, ciudad_inicio, ciudad_destino)

    # Crear el mapa y guardarlo en un archivo HTML
    archivo_mapa = crear_mapa(camino_mas_corto, coordenadas_ciudades, nombre_archivo)
    return archivo_mapa

if __name__ == "__main__":
    ciudad_inicio = "Aguascalientes"
    ciudad_destino = "Monterrey"
    archivo_mapa = generar_mapa_html(ciudad_inicio, ciudad_destino)
    print(f"Mapa generado: {archivo_mapa}")

