import win32com.client
import wmi
import sys
import MySQLdb
import datetime
import socket
import threading
import thread
import pythoncom
import time
import connect

class analisis():
    con = None
    global userAccount
    global passAccount
    ipHost = connect.host                                   #ip del server
    userAccount = connect.user                              #Nombre de Usuario para la bdd
    passAccount = connect.paswd                             #Contraseña de la Base de Datos}
    tablaDB = connect.table                                 #Nombre de la Tabla en la BDD                
            
    #Conexion a la base de datos Procesos
    con = MySQLdb.connect(host=ipHost,user=userAccount,passwd=passAccount,db=tablaDB)
    cursor = con.cursor()
    cursor.execute("select id,app,ip,fhi,lab from agrupacionDatos order by lab,ip, app asc, id asc;")
    row = cursor.fetchone()
    results = []

    while row is not None:
        #print(row)
        row = cursor.fetchone()
        if row == None:
            break
        results.append(list(row))

    #print(results[0])
    testing = []
    borrar = []
    borrarEstos = open("Borrar.txt","w")
    borrarEstos.write("delete from procesos where ")

    for i in range(0,len(results),1):
        try:
            if(i[5]):
                continue
        except:
            for j in range(i+1,i+6,1):
                try:
                    if(j[5]):
                        continue
                except:
                    try:
                        if(results[i][1]==results[j][1] and results[i][2]==results[j][2] and (results[j][3] - results[i][3]).total_seconds() < 5 and results[i][3].date() == results[j][3].date()):
                            results[j].append("DELETE")
                            borrarEstos.write("id_proceso = "+str(results[j][0])+" or\n")
                            results[i].append("KEEP")
                            print("success: "+str(results[i][0])+" and "+str(results[j][0]))
                            print("FHI1: "+str(results[i][3])+" FHI2: "+str(results[j][3]))
                    except:
                        continue
    borrarEstos.write(";")
    borrarEstos.close()

    archivo = open("Results2.txt","w")
    for i in range(0,len(results),1):
        archivo.write(str(results[i]))
        archivo.write("\n")
    archivo.close()
    
    con.close()
    cursor.close()
    con = None
     
if __name__ == "__main__":
    analisis()
