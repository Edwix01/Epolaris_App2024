import paramiko
import conexion_ssh
from textwrap import dedent

#################### Configuracion CISCO #########################

def configurar_vlan_cisco(connection, vlan_id, vlan_name):
    """
    Creacion de VLAN en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        vlan_id: Numero de VLAN.
        vlan_name: Nombre de la VLAN.
    """
    commands = [
        f'vlan {vlan_id}',
        f'name {vlan_name}',
    ]
    
    connection.send_config_set(commands)

#################### Configuracion HP A5120 #####################

def configurar_vlan_hp(connection, vlan_id, vlan_name):
    """
    Creacion de una VLAN en dispositivos HP usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        vlan_id: Numero de VLAN.
        vlan_name: Nombre de la VLAN.

    """
    commands = [
        f'vlan {vlan_id}',
        f'name {vlan_name}',
    ]
    
    connection.send_config_set(commands)

################# Configuracion HP V1910 - 3COM ##################
def configurar_vlan_3com(ip, username, password, vlan_id, vlan_name):
    """
    Función para crear VLANs en dispositivos 3Com y HP utilizando Paramiko.
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
        conexion_ssh.send_command(channel, f"vlan {vlan_id}", wait_time=2)
        conexion_ssh.send_command(channel, f"name {vlan_name}", wait_time=2)
        ssh.close()
        print("Creacion de VLAN completada con éxito.")
    except Exception as e:
        print(f"Error al crear VLAN en {ip}: {e}")
        ssh.close()


#################### Configuracion TPLINK #######################

def comandos_vlan_tplink(vlan_id, vlan_name):
    """
    Genera un archivo de texto con comandos para crear VLANs en dispositivos TP-Link.

    Parámetros:
        vlan_id: Número de VLAN.
        vlan_name: Nombre de la VLAN.
    """
    nombre_archivo = '/home/du/app_2024/modulo_automatizacion/comandos/comandos_vlan.txt'
    # Preparar los comandos con los valores proporcionados
    comandos = dedent(f"""
        configure
        vlan {vlan_id}
        name {vlan_name}
        exit
    """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())

    return nombre_archivo
