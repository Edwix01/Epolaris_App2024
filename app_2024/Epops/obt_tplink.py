import yaml


def filtplink(nombre):
    """
    Funcion para consultar la información de los switch TpLink

    Parameters:
    nombre(str):    

    Return:
    ips_tplink(list):           Lista de Direcciones IP de los switch TpLink
    credenciales_tplink(list):  Lista con las credenciales de los switch TpLink
    """
    with open(nombre, "r") as archivo:
       datos = yaml.safe_load(archivo)
    ips_tplink = []
    credenciales_tplink = {}
    # Obtener las IPs de los switches TPLink y las credenciales SSH
    if 'switches_tplink' in datos:
        configuracion_tplink = datos['switches_tplink']
        for switch, detalles in configuracion_tplink['hosts'].items():
            if 'epops_host' in detalles:
                ip = detalles['epops_host']
                ips_tplink.append(ip)
                credenciales_tplink[ip] = {
                    'usuario': configuracion_tplink['vars'].get('epops_user'),
                    'contraseña': configuracion_tplink['vars'].get('epops_ssh_pass')
                }
    return ips_tplink, credenciales_tplink

