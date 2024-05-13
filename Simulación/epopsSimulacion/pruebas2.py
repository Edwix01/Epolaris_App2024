# Lista de listas de ejemplo
lista_de_listas = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd'], [5, 'e']]

# Utilizar map() y una función lambda para filtrar los segundos valores que cumplen cierta condición
segundos_valores = list(map(lambda x: x[1], filter(lambda x: x[0] > 3, lista_de_listas)))

# Imprimir los segundos valores que cumplen la condición
print(segundos_valores)
