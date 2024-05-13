import conexion_ssh
import config_snmp

def procesar_dispositivos_snmp(datos_yaml):
    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        community = datos_yaml[grupo]['vars']['comunidad']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        device_type = datos_yaml[grupo]['vars']['device_type']
       

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            print(f"Configurando SNMP en {ip} para el dispositivo de marca {marca}...")

            # Diferenciar entre dispositivos usando marca
            if marca == '3COM':
                # Usar Paramiko para dispositivos 3Com
                config_snmp.configurar_snmp_3com(ip, user, password, community)
                print('CONFIGURACION EXITOSA')
            elif marca == 'HPV1910':
                config_snmp.configurar_snmp_3com(ip, user, password, community)
                print('CONFIGURACION EXITOSA')
            elif marca == 'TPLINK':
                archivo = config_snmp.comandos_snmp_tplink(community)
                conexion_ssh.epmiko(user, password, ip, archivo)
                print('CONFIGURACION EXITOSA')
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
                        config_snmp.configurar_snmp_cisco(connection, community)
                        print('CONFIGURACION EXITOSA')
                    elif marca == 'HPA5120':
                        config_snmp.configurar_snmp_hp(connection, community)
                    # No olvides desconectar después de configurar
                    connection.disconnect()
                else:
                    print(f"No se pudo conectar al dispositivo {ip} con Netmiko.")
