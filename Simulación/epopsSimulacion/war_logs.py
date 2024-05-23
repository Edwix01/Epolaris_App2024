import conexion_ssh
import config_logs
import os
import read_yaml
import obt_infyam
import time 
import teleg
import war_disp

def procesar_dispositivos_logs(datos_yaml,di_ip):

    """
    Procesa una lista de dispositivos para activar un servidor de LOGS según la información proporcionada en un archivo YAML.

    La función itera sobre cada grupo de dispositivos definido en el archivo YAML, extrae las configuraciones necesarias,
    y aplica las configuraciones de LOGS correspondientes utilizando diferentes bibliotecas y métodos según la marca y 
    características del dispositivo.

    Parámetros:
    datos_yaml (dict): Diccionario cargado desde un archivo YAML que contiene la información de configuración
                           para cada grupo de dispositivos.

    di_ip(str):   Direccion IP que requieren configuración de logs.

    """

    if not datos_yaml:
        print("No se proporcionaron datos válidos.")
        return

    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        device_type = datos_yaml[grupo]['vars']['device_type']
        servidordelogs = "10.0.1.10"
        trap = "7"

        ip = di_ip
        try:
            if marca in ['3COM', 'HPV1910']:
                # Usar Paramiko para dispositivos 3Com - HPV1910
                config_logs.configurar_logs_3com(ip, user, password, servidordelogs, save_config=True)

            elif marca == 'TPLINK':
                archivo = config_logs.comandos_logs_tplink(servidordelogs, trap)
                conexion_ssh.epmiko(user, password, ip, archivo)
                print(f"Configuración de logs completada exitosamente para el servidor {servidordelogs}.")

            else:
                # Para Cisco y HPv1910, se utiliza Netmiko
                dispositivo = {
                    'device_type': device_type,
                    'host': ip,
                    'username': user,
                    'password': password,
                }
                
                connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)

                if connection:
                    if marca == 'CISCO':
                        config_logs.configurar_logs_cisco(connection, servidordelogs, trap, save_config=False)

                    elif marca == 'HPA5120':
                        config_logs.configurar_logs_hp(connection, servidordelogs, save_config=False)
                    connection.disconnect()
        except Exception as e:
            print(f"Error al configurar el dispositivo {ip}: {e}")


def prevención_corte_logs(direc):
    """
    Funcion para emitir advertencia preventiva en caso de que un switch falle

    Parameters:
    conexiones(list):       Lista con tuplas que especifican las conexiones entre dispositivos
    root(str):              Dirección IP de la raíz del árbol STP 


    Returns:
    Advertencia - Mensaje enviado por telegram
    """
    base_path = "/home/edwin/Documents/Prototipo_App2024/Simulación/epopsSimulacion/inventarios"
    archivo = os.path.join(base_path, "dispositivos.yaml")
    datos_yaml = read_yaml.cargar_datos_snmp(archivo)
    interrupciones = war_disp.leer_incidencias(direc)
    #Generar Advertencia
    cabecera = "-----------------------Notificación---------------------------"
    tail = "-"*len(cabecera)
    mesf = ""
    for disp in direc:
        if  interrupciones[disp] >= 2:
            mesf = (cabecera+"\nEl dispositivo: "+disp+" ha tenido varias fallas"+"\nSe ha levantado los logs\n"+tail)
            procesar_dispositivos_logs(datos_yaml,disp)
            print(mesf)

current_dir = os.path.dirname(__file__)
nombreyaml = os.path.join(current_dir, 'inventarios', 'dispositivos.yaml')
datos = obt_infyam.infyam(nombreyaml)
direc = datos.keys()

while True:
    prevención_corte_logs(direc)
    time.sleep(60*5)
