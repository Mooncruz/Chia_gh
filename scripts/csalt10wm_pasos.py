#!/bin/python3
import os
import pandas as pd
import matplotlib.pyplot as plt

csalt=['1e-5','1e-4','1e-3','1e-2','1e-1']
#para poder utilizar nombres de carpeta con numero, debo ponerlo entre comillas para que no lo lea como numero sino como str

pH=['3.00','4.65','6.00']
# debo poner todas las variables que se analizaran en el script y estaran en el nombre del directorio donde buscara

Radio=[]
# este es el directorio donde se iran guardando los radios de cada una de los directorios que se analizaran

direct=[]

for i in csalt:
    # primero tendre en cuenta la concentracion de sal por eso llamo estos valores en primer lugar
    
    for j in pH:
        # despues llamo la otra variable, en este caso es el pH
        
        direc='csalt10-'+str(i)+"-pH-"+str(j)
        # cada una de la información leída debe ser guardada en esta variable (direc) y en el loop se tomará la información que allí está. Esta variable se modifica con cada una de los loop que se hagan 
        direct.append(direc)
        # creo una nueva lista con cada uno de los nombres que se registren en el loop. Acá si quedarán almacenadas
        
        os.chdir(direc)
        #abrir el direc creado en el paso anterior
        
        
        with open('results.dat','r') as rcsalt:
            #este comando me permite abrir un archivo que se encuentra en cada una de las carpetas que necesito inspeccionar. En este archivo se encuentra el valor del Radio del nanogel a unas condiciones específicas y le pongo el alias de rcsalt para llamarlo más fácil
            
            datcsalt=rcsalt.read()
            # creo una variable para que me vaya guardando los datos leídos en el archivo anterior
            
        r=float(datcsalt.split()[1])
        # esta es una lista de comprensión donde pido hacer varias cosas. lo primero es reconocer el tipo de número que se encuentrará en rcsalt (float) después a este número los divido con .split y por último que de esos que se han dividido tomar el segundo valor 1 (recordar que el primer valor es 0)
        
        Radio.append(r)
        # pido que me añada el valor de r extraído a la lista que tiene nombre Radio, establecido al inicio del script

        os.chdir('..')
        # salir de esta carpeta 



with open('datos_Csalt.dat','w') as datcsalt:
    # Aquí construiré un archivo donde debe escribir los datos en una tabla para poder ser graficados y le pongo el alias de datcsalt 
    for i,j in enumerate(direct):
        # pido que me enumere los datos que se encuentran en la carpeta direct (en este caso i es el índice y j hace alusión a los datos dentro de la carpeta)
        csaltt=j.split("-")[1]+"-"+j.split("-")[2]
        # solicito que los valores de j sean separados con un - y que me tome el número 2 y 3  que corresponde al valor de la concentración de sal 
        pH1=j.split("-")[4]
        # solicito que los valores de j sean separados con un - y pido que me tome el valor 5 que corresponde al valor del pH
        datcsalt.write(f'{csaltt}\t{pH1}\t{Radio[i]}\n')
        #pido que en el archivo datcsalt escriba los valores de csaltt, pH1 y Radio (\t + es igual a un tab y \n = es igual a un salto de línea


df=pd.read_csv("datos_Radio10.dat", sep="\t",header=None,names=['csalt','pH','R'])
# creo una variable donde usando el directorio de panda (pd) lea los datos en datos_Csalt.dat y los separe con un tab, sin poner encabezado (header: None) y poniendo nombres a las tres columnas.

pH1=df[df['pH'] == 3.0]
# estoy filtrando los datos que cumplen con esta condición: el pH sea igual a 3 y me crea una tabla con estos valores.

pH2=df[df['pH'] == 4.65]
pH3=df[df['pH'] == 6.00]

fig, ax = plt.subplots()
# fig, ax= se debe poner para realizar una grafica con varios opciones y plt esta llamando a la libreria matplotlib.pyplot y subplots () es la opcion de hacer varias graficas en una

print(df)
#esto lo hice para oder ver que hizo panda en la construccion de la tabla y las subtablas que le pedi que son pH1, pH2, pH3
print(pH1)
print(pH2)
print(pH3)


ax.plot(pH1['csalt'], pH1['R'],label='pH 3')
# grafico el radio en función de la concentracion de sal con pH1 constante (3) y etiqueto (label) con el nombre pH 3 esto debo ponerlo entre '' 

ax.plot(pH2['csalt'], pH2['R'],label='pH 4.65')
ax.plot(pH3['csalt'], pH3['R'],label='pH 6')

ax.set_xscale('log')
# solicito que la escala de x sea puesta logarítmica

ax.legend()
# indico que pondré nombres a los ejes habilito los label

ax.set_xlabel('Concentracion sal')
# etiqueta del eje x
ax.set_ylabel("Radio")
# etiqueta del eje y
plt.show()
# mostrar la gráfica

fig.savefig('Csaltvsradio10.png')
