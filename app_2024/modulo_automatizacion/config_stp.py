import paramiko
import conexion_ssh
from textwrap import dedent

#################### Configuracion CISCO #########################
#-----------------------------------------------------------------#
def configurar_stpMode_cisco(connection, region_name, modo):
    """
    Configura el modo STP en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        modo: El modo de STP deseado (pvst, rapid-pvst o mst).
    """
    commands = [
        f'spanning-tree mode {modo}',
    ]
    
    if modo == 'mst':
        commands.extend([
            'spanning-tree mst configuration',
            f'name {region_name}',
            'exit',
        ])
        
    commands.append('end')
    
    connection.send_config_set(commands)

#------------------------------------------------------------------#
def configurar_stpPrioridad_cisco(connection, prioridad, vlaniD):
    """
    Configura el modo STP en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        prioridad: Numero de prioridad (Rango de 0 - 61440).
    """
    commands = [
        f'spanning-tree vlan {vlaniD} priority {prioridad}',
        f'end',
    ]
    
    connection.send_config_set(commands)

#################################################################
#################### Configuracion HP A5120 #####################

def configurar_stpMode_hp(connection, region_name, modo):
    """
    Configura el modo STP en dispositivos HP usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        region_name: El nombre de la región MST.
        modo: El modo de STP deseado (STP, RSTP o MSTP).
    """
    commands = [
        f'stp mode {modo}'
    ]
    
    if modo == 'mst':
        commands.extend([
            'stp region-configuration',
            f'region-name {region_name}',
            'active region-configuration',
        ])
        
    commands.extend([
        'stp enable',
        'exit',
    ])
    
    connection.send_config_set(commands)

#------------------------------------------------------------------------------#
def configurar_stpPrioridad_hp(connection, instance, modo, prioridad, vlan):
    """
    Configura el modo STP en dispositivos HP usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        prioridad: Numero de prioridad (Rango de 0 - 61440).
        instancia: Numero de instancia (0 por defecto y agrupa todas las VLANS que no han sido asignadas a otras vlans)
        vlan: Rango de Vlans
    """

    commands = [
    ]
    
    if modo == 'stp' or modo == 'rstp':
        commands.extend([
            f'stp priority {prioridad}',
        ])
    elif modo == 'pvst':
        commands.extend([
            f'stp vlan {vlan} priority {prioridad}',
        ])
    elif modo == 'mstp':
        commands.extend([
            f'stp instance {instance} priority {prioridad}',
        ])

    commands.extend([
        'exit',
    ])

    
    connection.send_config_set(commands)

#################################################################
################# Configuracion HP V1910 - 3COM ##################
def configurar_STP_3com(ip, username, password, region_name, modo):
    """
    Función para configurar STP en un dispositivo 3Com utilizando Paramiko.
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
        conexion_ssh.send_command(channel, f"stp mode {modo}", wait_time=2)
        if modo == 'mstp':
            conexion_ssh.send_command(channel, "stp region-configuration", wait_time=2)
            conexion_ssh.send_command(channel, f"region-name {region_name}", wait_time=2)
            conexion_ssh.send_command(channel, "active region-configuration", wait_time=2)
        conexion_ssh.send_command(channel, "exit", wait_time=2)
        ssh.close()
        print("Configuración de STP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar STP en {ip}: {e}")
        ssh.close()

#------------------------------------------------------------------------------------------#
def configurar_stpPriority_3com(ip, username, password, modo, prioridad, vlan, instance):
    """
    Función para configurar STP en un dispositivo 3Com o HPV1910 utilizando Paramiko.
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
        if modo == 'stp' or modo == 'rstp':
            conexion_ssh.send_command(channel, f"stp priority {prioridad}", wait_time=2)
        elif modo == 'pvst':
            conexion_ssh.send_command(channel, f"stp vlan {vlan} priority {prioridad}", wait_time=2)
        elif modo == 'mstp':
            conexion_ssh.send_command(channel, f"stp instance {instance} priority {prioridad}", wait_time=2)
        
        conexion_ssh.send_command(channel, "exit", wait_time=2)
        ssh.close()
        print("Configuración de STP Priority completada con éxito.")
    except Exception as e:
        print(f"Error al configurar STP en {ip}: {e}")
        ssh.close()

#################################################################
#################### Configuracion TPLINK #######################
def comandos_stp_tplink(region, modo):
    """
    Genera un archivo de texto con comandos de configuración para STP.

    Parámetros:
        region (str): El nombre de la región MSTP.
        modo (str): El modo de STP deseado ('stp', 'rstp' o 'mstp').
    """
    nombre_archivo = '/home/du/app_2024/modulo_automatizacion/comandos/comandos_stp.txt'
    # Preparar los comandos con los valores proporcionados
    if modo == 'mstp':  # Asegúrate de que el valor de modo esté correctamente chequeado
        comandos = dedent(f"""
        configure
        spanning-tree mode {modo}
        spanning-tree extend system-id
        spanning-tree mst configuration
        name {region}
        exit
        """)
    else:
        comandos = dedent(f"""
        configure
        spanning-tree mode {modo}
        exit
        """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return nombre_archivo  # Devuelve la variable correctamente definida

def comandos_stpPriority_tplink(prioridad, vlan):
    """
    Genera un archivo de texto con comandos de configuración para STP en una VLAN específica.

    Parámetros:
        prioridad: Número de prioridad que va de 0 a 61440.
        vlan: Identificador de la VLAN para la cual se está configurando la prioridad de STP.
    """
    nombre_archivo = '/home/du/app_2024/modulo_automatizacion/comandos/comandos_stp_prioridad.txt'
    
    # Preparar los comandos con los valores proporcionados
    comandos = dedent(f"""
        configure
        vlan {vlan}
        spanning-tree priority {prioridad}
        exit
    """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return nombre_archivo
