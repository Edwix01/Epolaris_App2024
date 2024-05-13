import yaml

def cargar_configuracion_yaml(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        return yaml.safe_load(archivo)