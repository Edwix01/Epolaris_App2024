import networkx as nx

def encontrar_caminos_posibles(grafo_matriz, nodo_inicial, nodo_final):
    # Convertir la matriz de adyacencia en un grafo dirigido
    G = nx.DiGraph()
    for i in range(len(grafo_matriz)):
        for j in range(len(grafo_matriz[i])):
            if grafo_matriz[i][j] == 1:
                G.add_edge(i, j)

    # Encontrar todos los caminos posibles entre nodo_inicial y nodo_final
    caminos_posibles = list(nx.all_simple_paths(G, source=nodo_inicial, target=nodo_final))

    return caminos_posibles

# Ejemplo de uso
grafo_matriz = [[0, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 0, 0, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]]
nodo_inicial = 3
nodo_final = 3

caminos = encontrar_caminos_posibles(grafo_matriz, nodo_inicial, nodo_final)
print("Caminos posibles de", nodo_inicial, "a", nodo_final, ":", caminos)

