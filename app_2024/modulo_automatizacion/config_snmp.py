import paramiko
import conexion_ssh
from textwrap import dedent

#################### Configuracion CISCO #########################
def configurar_snmp_cisco(connection, community_name):
    commands = [
        f"snmp-server community {community_name} RO",
    ]
    connection.send_config_set(commands)

#################################################################
################### Configuracion HPA5120 #######################
def configurar_snmp_hp(connection, community_name):
    commands = [
        f"snmp-agent community read {community_name}",
    ]
    connection.send_config_set(commands)

################################################################
############### Configuracion 3COM-HP1910 #########################
def configurar_snmp_3com(ip, username, password, community_name):
    """
    Función para configurar SNMP en un dispositivo 3Com y HP1910 
    utilizando Paramiko.
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
        # Después de haber entrado en el modo de línea de comandos, continúa con la configuración de SNMP.
        conexion_ssh.send_command(channel, "system-view", wait_time=2)
        conexion_ssh.send_command(channel, f"snmp-agent community read {community_name}", wait_time=2)
        ssh.close()
        print("Configuración de SNMP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar SNMP en {ip}: {e}")
        ssh.close()

#################################################################
#################### Configuracion TPLINK #######################
def comandos_snmp_tplink(comunidad):
    """
    Genera un archivo de texto con comandos de configuración para SNMP.

    Parámetros:
        comunidad (str): El nombre de la comunidad SNMP.
    """
    # Preparar los comandos con los valores proporcionados
    nombre_archivo = '/home/du/app_2024/modulo_automatizacion/comandos/comandos_snmp.txt'
    comandos = dedent(f"""
    configure
    snmp-server community {comunidad} read-only
    """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())

    return nombre_archivo
