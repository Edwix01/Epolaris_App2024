import paramiko
import conexion_ssh
from textwrap import dedent

#################### Configuracion CISCO #########################
def configurar_logs_cisco(connection, servidorIP, trap):
    """
    Configuracion de LOGS en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        servidorIP: Direccion IP del servidor syslog
        trap: Tipos de logs 
    """
    commands = [
        f'logging host {servidorIP}',
        f'loggin trap {trap}',
    ]
    
    connection.send_config_set(commands)


#################### Configuracion HP A5120 #####################
def configurar_logs_hp(connection, servidorIP):
    """
    Configuracion de LOGS en dispositivos HP usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        servidorIP: Direccion IP del servidor syslog
        trap: Tipos de logs 

    """
    commands = [
        f'infor-center loghost {servidorIP}',
    ]
    
    connection.send_config_set(commands)

################# Configuracion HP V1910 - 3COM ##################
def configurar_logs_3com(ip, username, password, servidorIP):
    """
    Función para configurar LOGS en dispositivos 3Com y HP utilizando Paramiko.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        # Obtener un canal interactivo
        channel = ssh.invoke_shell()
        # Primero, intentamos entrar en el modo de línea de comandos
        conexion_ssh.send_command(channel, "_cmdline-mode on", wait_time=2)
        # Esperamos la solicitud de confirmación y enviamos 'Y' para continuar.
        conexion_ssh.interactive_send_command(
            channel,
            "Y",  # Confirmamos la pregunta para entrar en el modo de línea de comandos.
            "Please input password:",  # La cadena que esperamos antes de enviar la contraseña.
            "512900",  # La contraseña para el modo de línea de comandos.
            wait_time=2  # Tiempo de espera ajustado correctamente.
        )
        # Después de haber entrado en el modo de línea de comandos, continúa con la configuración de STP.
        conexion_ssh.send_command(channel, "system-view", wait_time=2)
        conexion_ssh.send_command(channel, f"infor-center loghost {servidorIP}", wait_time=2)
        ssh.close()
        print("Configuracion de LOGS completada con éxito.")
    except Exception as e:
        print(f"Error al configurar LOGS en {ip}: {e}")
        ssh.close()


#################### Configuracion TPLINK #######################

def comandos_logs_tplink(servidorIP, trap):
    """
    Genera un archivo de texto con comandos para configurar LOGS en dispositivos TPLINK.

    Parámetros:
        servidorIP: Direccion IP del servidor syslog
        trap: Tipos de logs (por ejemplo, 'trap')
    """
    nombre_archivo = '/home/du/app_2024/modulo_automatizacion/comandos/comandos_logs.txt'
    # Preparar los comandos con los valores proporcionados
    comandos = dedent(f"""
        configure
        logging host index 2 {servidorIP} {trap}
        exit
    """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())

    return nombre_archivo
