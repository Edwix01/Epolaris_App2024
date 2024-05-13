from pysnmp.entity.rfc3413.oneliner import cmdgen
import re
cmdGen = cmdgen.CommandGenerator()


def ma_int(direc,comunidad):
    d2={}
    f = 0
    fif = []
    for server_ip in direc:
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.2.2.1.2'
        )
        c=1
        d1 = {}
        if errorIndication != None:
            f = 1
            fif.append(server_ip)
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                # and  not("0/0" in val.prettyPrint()
                if "Ethernet" in val.prettyPrint()  :
                    # Utilizar una expresión regular para extraer la primera letra y los números
                    cadena = val.prettyPrint()
                    # Utilizar una expresión regular para encontrar solo los números y barras
                    numeros = re.sub(r'[^\d/]', '', cadena)
                    d1[str(c)] = cadena[0] + numeros
                    c+=1
        d2[str(server_ip.split(".")[-1])] = d1
    return d2,f,fif


