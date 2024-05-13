import conexion_ssh
import config_stp

def procesar_dispositivos_stpActive(datos_yaml):
    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        region = datos_yaml[grupo]['vars']['region']
        modo = datos_yaml[grupo]['vars']['modo']
        device_type = datos_yaml[grupo]['vars']['device_type']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            print(f"Configurando STP ACTIVE en {ip} para el dispositivo de marca {marca}...")

            # Diferenciar entre dispositivos usando marca
            if marca == '3COM':
                # Usar Paramiko para dispositivos 3Com
                config_stp.configurar_STP_3com(ip, user, password, region, modo)
            elif marca == 'HPV1910':
                config_stp.configurar_STP_3com(ip, user, password, region, modo)
            elif marca == 'TPLINK':
                archivo = config_stp.comandos_stp_tplink(region, modo)
                conexion_ssh.epmiko(user, password, ip, archivo)
            else:
                # Para Cisco y HP, se utiliza Netmiko
                dispositivo = {
                    'device_type': device_type,
                    'host': ip,
                    'username': user,
                    'password': password,
                }
                # Establecer conexión usando Netmiko
                connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)
                if connection:
                    if marca == 'CISCO':
                        config_stp.configurar_stpMode_cisco(connection, region, modo)
                        print('CONFIGURACION EXITOSA')
                    elif marca == 'HPA5120':
                        config_stp.configurar_stpMode_hp(connection, region, modo)
                    # No olvides desconectar después de configurar
                    connection.disconnect()
                else:
                    print(f"No se pudo conectar al dispositivo {ip} con Netmiko.")

def procesar_dispositivos_stpPriority(datos_yaml):
    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        prioridad = datos_yaml[grupo]['vars']['prioridad']
        vlan = datos_yaml[grupo]['vars']['vlan']
        modo = datos_yaml[grupo]['vars']['modo']
        instance = datos_yaml[grupo]['vars']['instance']
        device_type = datos_yaml[grupo]['vars']['device_type']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            print(f"Configurando STP ACTIVE en {ip} para el dispositivo de marca {marca}...")

            # Diferenciar entre dispositivos usando marca
            if marca == '3COM':
                # Usar Paramiko para dispositivos 3Com
                config_stp.configurar_stpPriority_3com (ip, user, password, modo, prioridad, vlan, instance)
            elif marca == 'HPV1910':
                config_stp.configurar_stpPriority_3com(ip, user, password, modo, prioridad, vlan, instance)
            elif marca == 'TPLINK':
                archivo = config_stp.comandos_stpPriority_tplink(prioridad, vlan)
                conexion_ssh.epmiko(user, password, ip, archivo)
            else:
                # Para Cisco y HP, se utiliza Netmiko
                dispositivo = {
                    'device_type': device_type,
                    'host': ip,
                    'username': user,
                    'password': password,
                }
                # Establecer conexión usando Netmiko
                connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)
                if connection:
                    if marca == 'CISCO':
                        config_stp.configurar_stpPrioridad_cisco(connection, prioridad, vlan)
                        print('CONFIGURACION EXITOSA')
                    elif marca == 'HPA5120':
                        config_stp.configurar_stpPrioridad_hp(connection, instance, modo, prioridad, vlan)
                    # No olvides desconectar después de configurar
                    connection.disconnect()
                else:
                    print(f"No se pudo conectar al dispositivo {ip} con Netmiko.")
