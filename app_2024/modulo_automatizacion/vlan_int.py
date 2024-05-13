import conexion_ssh
import config_vlan

def procesar_dispositivos_vlan(datos_yaml):
    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        id_vlan= datos_yaml[grupo]['vars']['id']
        name_vlan= datos_yaml[grupo]['vars']['name_vlan']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        device_type = datos_yaml[grupo]['vars']['device_type']
       

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            print(f"Creando VLAN en {ip} para el dispositivo de marca {marca}...")

            # Diferenciar entre dispositivos usando marca
            if marca == '3COM':
                # Usar Paramiko para dispositivos 3Com
                config_vlan.configurar_vlan_3com(ip, user, password, id_vlan, name_vlan)
            elif marca == 'HPV1910':
                config_vlan.configurar_vlan_3com(ip, user, password, id_vlan, name_vlan)
            elif marca == 'TPLINK':
                archivo = config_vlan.comandos_vlan_tplink(id_vlan, name_vlan)
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
                        config_vlan.configurar_vlan_cisco(connection, id_vlan, name_vlan)
                        print('CONFIGURACION EXITOSA')
                    elif marca == 'HPA5120':
                        config_vlan.configurar_vlan_hp(connection, id_vlan, name_vlan)
                    # No olvides desconectar después de configurar
                    connection.disconnect()
                else:
                    print(f"No se pudo conectar al dispositivo {ip} con Netmiko.")
