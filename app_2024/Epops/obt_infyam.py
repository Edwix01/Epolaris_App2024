import yaml

def infyam(nombre):
# Cargar el archivo YAML
    """
    Funcion para leer los datos de un archivo yaml
    Parameters:
    nombre(str):      Ruta del archivo yaml

    Return:       
    credenciales_switches(dict):    Diccionario con información de los switches
    """
    with open(nombre, "r") as archivo:
           datos = yaml.safe_load(archivo)
    # Inicializar un diccionario para almacenar las credenciales SSH y la comunidad SNMP
    # Inicializar un diccionario para almacenar las credenciales SSH y la comunidad SNMP
    credenciales_switches = {}

    # Obtener las credenciales SSH y la comunidad SNMP de todos los switches
    for categoria, configuracion in datos.items():
        if categoria.startswith('switches_'):
            marca = categoria.replace('switches_', '')  # Obtener la marca del switch
            for switch, detalles in configuracion['hosts'].items():
                if 'epops_host' in detalles:
                    ip = detalles['epops_host']
                    usuario = configuracion['vars'].get('epops_user')
                    contraseña = configuracion['vars'].get('epops_ssh_pass')
                    snmp = configuracion['vars'].get('epops_snmp')
                    credenciales_switches[ip] = {'marca': marca, 'usuario': usuario, 'contraseña': contraseña, 'snmp': snmp}

# Imprimir el diccionario de credenciales SSH y SNMP para todos los switches
    return credenciales_switches
