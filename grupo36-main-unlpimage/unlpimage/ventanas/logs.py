import csv
import os
from datetime import datetime
directorio=os.path.abspath(os.path.dirname(__file__))
ruta_archivo = os.path.abspath(os.path.join(directorio,'logs_sistema.csv'))


def Actualizacion (nombre,text):

    def agregar(datos,ruta_archivo):
        with open (ruta_archivo,'a',newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow((datos))



    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime('%Y-%M-%D')
    hora_formateada = fecha_actual.strftime('%H:%M:%S')

    fecha= (fecha_formateada , hora_formateada)

    datos_a_Agregar= [fecha,nombre,text]
    agregar(datos_a_Agregar,ruta_archivo)
