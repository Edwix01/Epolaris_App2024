import yaml
# Función para leer el archivo YAML
def leer_yaml(ruta):
    """
    Esta función devuelve los datos del archivo yaml en formato de diccionario.

    Parámetros:
    ruta (str): Ruta del archivo .yaml

    Retorna:
    datos: Datos en formato diccionario.
    """
    with open(ruta, 'r') as archivo:
        datos = yaml.safe_load(archivo)
    return datos
