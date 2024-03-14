import numpy as np
import matplotlib.pyplot as plt
import math

def readermatriz(filename):
    # Lee la matriz desde el archivo en el mismo directorio que el script o función
    matriz = np.genfromtxt(filename, dtype=float, delimiter=',')
    r=307.5
    intervalo= r / 50
    delta=[i * intervalo for i in range(51)]
    delta.pop(0)
    volumen=[(4/3)*math.pi * i**3 for i in delta]
    diferencias_volumen=np.insert(np.diff(volumen),0,volumen[0]) 
    densidad_L6 = []
    mean_L6 = []

    # Obtiene las dimensiones de la matriz
    rows, columns = matriz.shape
    grupos_filas = 20371

    # Calcula el número total de grupos
    total_grupos = rows // grupos_filas

    for i in range(total_grupos):
        inicio = i * grupos_filas
        fin = (i + 1) * grupos_filas
        grupos_filas_actual = matriz[inicio:fin, :]

        # Calcula la suma de filas para cada columna
        sumafilas = np.sum(grupos_filas_actual, axis=0)

        # Calcula la densidad para cada columna
        #densidad_columnas = sumafilas / volumen
        densidad_columnas = np.divide(np.sum(grupos_filas_actual, axis=0), volumen)
        # Almacena la densidad por columna en la lista
        densidad_L6.append(densidad_columnas)

    # Calcula el promedio de densidades por columna en toda la matriz
    mean_densidad = np.mean(densidad_L6, axis=0)

    return densidad_L6, mean_densidad, diferencias_volumen

# Llama a la función con el nombre del archivo en el mismo directorio
densidad_L6, mean_densidad= readermatriz("matrizL6_radial.dat")

# Imprime densidades por columna para cada grupo
for i, densidades_grupo in enumerate(densidad_L6):
    print(f"Densidades en el grupo {i + 1}:\n{densidades_grupo}")

    #Imprime el promedio de densidades por columna en toda la matriz
    print("\nPromedio de densidades por columna en toda la matriz:\n", mean_densidad)

def promedio_listas(densidad_L6):

    # Lee la matriz desde el archivo en el mismo directorio que el script o función
  
    listas_por_filas=[[] for _ in range(50)]
    for lista in densidad_L6:
        for indice,elemento in enumerate(lista):
            listas_por_filas[indice].append(elemento)
    print(listas_por_filas)

    promedio=[]
    for lista in listas_por_filas:
        promedio_lista=sum(lista)/len(lista) if len(lista)> 0 else 0
        promedio.append(promedio_lista)

    print(promedio)

    values=[i * 12.3 for i in range (50)]

  #  plt.plot(values,promedio)
  #  plt.show()
  #  plt.savefig('Densidad_surface-0.1')

        
    return listas_por_filas, promedio,values

def particulas(promedio):

    volumen=12.3 *615 *615
    particulas=sum(promedio)*volumen
    print(particulas)

    return particulas


a,b,c = promedio_listas(densidad_L6)
d = particulas(b)    
