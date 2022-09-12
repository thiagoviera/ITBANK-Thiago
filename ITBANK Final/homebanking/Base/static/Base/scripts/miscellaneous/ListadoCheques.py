import csv
from datetime import datetime
from datetime import date

NUMERO_CHEQUE_INDEX=0

FECHA_ORIGEN_INDEX=6
FECHA_PAGO_INDEX=7
DNI_INDEX=8
TIPO_INDEX=9
ESTADO_INDEX=10

f=open("../../test.csv", "r") #INSERTAR ARCHIVO CSV
#f=open("archivo.csv", "r")

campos= ["NroCheque","CodigoBanco","CodigoSucursal","NumeroCuentaOrigen","NumeroCuentaDestino","Valor","FechaOrigen","FechaPago","DNI","Estado"]

datosCsv= csv.reader(f)
datos=[]
for linea in datosCsv: #Mete los datos del csv en datos[]
    datos.append(linea)



def searchDNI(dni): #BUSCA EL USUARIO INGRESANDO EL DNI Y DEVUELVE UNA LISTA CON TODOS LOS CHEQUES DEL DNI
    listaDni=[]
    for usuario in datos:
        if(usuario[DNI_INDEX]==dni):
            listaDni.append(usuario)
    return listaDni

def doesChequeRepeat(listaUsuario):
    for usuario in listaUsuario:
        for entry in datos:
            if (usuario[NUMERO_CHEQUE_INDEX] == entry[NUMERO_CHEQUE_INDEX] and usuario[DNI_INDEX] != entry[DNI_INDEX]):
                return True
    return False

def csvOutputFirst(usuario): #INGRESA LA LISTA DEL USUARIO, CREA UN ARCHIVO CSV USANDO EL FORMATO Y IMPRIME LOS DATOS DEL PRIMER CHEQUE DEL USER
    for cheques in usuario:
        listToPrint=["Fecha Origen: "+ cheques[FECHA_ORIGEN_INDEX] , " Fecha Pago: "
        + cheques[FECHA_PAGO_INDEX]," Valor: "+cheques[5]," Cuenta: "+cheques[3]]
        with open(cheques[DNI_INDEX]+" "+str(datetime.timestamp(datetime.now()))+".csv", 'w', newline='') as output:
            writer=csv.writer(output)
            writer.writerow(listToPrint)
        pass



def csvOutputAll(usuario): #INGRESA LISTA DEL USUARIO, CREA ARCHIVO CSV CON EL FORMATO E IMPRIME LOS DATOS PEDIDOS DE TODOS LOS CHEQUES
    with open(usuario[0][DNI_INDEX]+" "+str(datetime.timestamp(datetime.now()))+".csv", 'a') as output:
        for cheques in usuario:
            for cheque in cheques:
                output.write(str(cheque) + ',')
            output.write('\n')

def pantallaOutput(usuario): #IMPRIME LA LISTA DEL USUARIO EN LA PANTALLA
    for cheques in usuario:
        print( "NroCheque: " +cheques[0]+" CodigoBanco: " +cheques[1]+
        " CodigoSucursal: "+cheques[2]+" NumeroCuentaOrigen: "+cheques[3]+
        " NumeroCuentaDestino: "+cheques[4]+" Valor: "+cheques[5]+
        " Fecha Origen: "+ cheques[FECHA_ORIGEN_INDEX] + " Fecha Pago: "+cheques[FECHA_PAGO_INDEX]+
        " Dni: " + cheques[DNI_INDEX] + " Estado: "+cheques[ESTADO_INDEX] + " Tipo: "+cheques[TIPO_INDEX])

def estadoCheque(usuario,estado): #MODIFICA LA LISTA DE CHEQUES SEGUN EL ESTADO
    listaFinal=[]
    for cheques in usuario:
        if (cheques[ESTADO_INDEX]==estado):
            listaFinal.append(cheques)
        elif (estado==""):
            listaFinal.append(cheques)
    return listaFinal

def tipoCheque(usuario,tipo): #MODIFICA LA LISTA DE CHEQUES SEGUN EL TIPO
    listaFinal=[]
    for cheques in usuario:
        if (cheques[TIPO_INDEX]==tipo):
            listaFinal.append(cheques)
    return listaFinal

def filtrarRangoFecha(usuario,desde,hasta): #PLANTILLA DE LA FUNCION PARA FILTRAR POR FECHA
    listaFinal=[]
    for cheques in usuario:
        if (desde<= date.fromtimestamp(cheques[FECHA_ORIGEN_INDEX]) <= hasta):
            listaFinal.append(cheques)
    return listaFinal

def main(): #MAIN DEL PROGRAMA
    # f=input("Ingrese nombre de archivo csv")
    listaUsuario=searchDNI(str(input("Ingrese DNI sin comas ni puntos: ")))
    # Chequea si hay actividad bajo este DNI
    if len(listaUsuario) == 0:
        # Salida de Error
        print("No hay cheques emitidos o depositados a este DNI")
    elif doesChequeRepeat(listaUsuario):
        # Salida de Error
        print("El identificador del cheque coincide con otros en el sistema.")
    else:
        # print(listaUsuario)
        salida=input("Ingrese tipo de salida. \nPANTALLA o CSV: ")
        
        # Modifica segun el tipo del cheque
        listaUsuario=tipoCheque(listaUsuario,input("Imprimir cheque por tipo.\nEMITIDO o DEPOSITADO: "))
        
        # Modifica segun el estado del cheque
        if("SI"==input("Filtrar por estado de cheque? INSERTE SI o NO: ")):
            listaUsuario=estadoCheque(listaUsuario,input("Imprimir cheque por estado.\nPENDIENTE, APROBADO, RECHAZADO: "))
        
        # Filtro de rango de fechas    
        if("SI"==input("Filtrar por rango de fecha? INSERTE SI o NO: ")):
            listaUsuario=filtrarRangoFecha(listaUsuario,date.fromtimestamp(input("Ingrese primer fecha de filtrado en timestamp: ")),date.fromtimestamp(input("Ingrese fecha de cierre de filtrado en timestamp: ")))
        
        if(salida=="CSV"): # Imprime segun la salida determinada previamente
            csvOutputAll(listaUsuario)
        elif(salida=="PANTALLA"):
            pantallaOutput(listaUsuario)

main()