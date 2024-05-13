# Listas proporcionadas
claves = ["('10.0.1.2', '10.0.1.1')", "('10.0.1.3', '10.0.1.4', '10.0.1.5')"]
valores = [[('10.0.1.2', 'G1/0', '10.0.1.1', 'G0/3')], [('10.0.1.4', 'G0/2', '10.0.1.5', 'G0/2'), ('10.0.1.3', 'G0/2', '10.0.1.4', 'G0/3')]]

# Formatear las claves
claves_formateadas = [f"{clave[0]} - {clave[1]}" for clave in claves]

# Crear el diccionario
diccionario = dict(zip(claves_formateadas, valores))

# Imprimir el diccionario resultante
print(diccionario)
