import os
import numpy as np
import matplotlib.pyplot as plt

# Carga los datos de densidad desde el archivo

lmbd=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']
x=[[],[],[],[],[],[],[],[],[],[]]
density=[[],[],[],[],[],[],[],[],[],[]]

for l,lbd in enumerate(lmbd):
    os.chdir('surface25-'+lbd)
    with open('density.xvg','r') as gyrt:
        for line in gyrt:
            if line.startswith(('@','#')):
                continue
            columns=line.split()
            if len(columns)==2:
                x_value,density_value=map(float,columns)
                x[l].append(x_value)
                density[l].append(density_value)
    os.chdir('..')

                  

center=[[],[],[],[],[],[],[],[],[],[]]
x_centered=[[],[],[],[],[],[],[],[],[],[]]
x_positive=[[],[],[],[],[],[],[],[],[],[]]
density_positive=[[],[],[],[],[],[],[],[],[],[]]
          
# Calcula el centro del sistema
for j,xs in enumerate (x):
    center[j] = np.mean(x[j])

# Ajusta las coordenadas para centrarlas
x_centered[j] = [value -center[j] for value in x[j] ]

# Filtra los valores positivos en el eje x
x_positive[j] = [x for x[j] in x_centered if x[j] > 0]
density_positive[j] = [density[i] for i, x[j] in enumerate(x_centered) if x[j] > 0]

# Crea la gráfica de densidad
#plt.ion()
plt.plot(x_positive[0], density_positive[0])
plt.plot(x_positive[0], density_positive[0])
plt.plot(x_positive[0], density_positive[0])
plt.plot(x_positive[0], density_positive[0])
plt.plot(x_positive[0], density_positive[0])
plt.xlabel('Posición en x (nm)')
plt.ylabel('Densidad Kg \ m3')
plt.title('Densidad centrada en la caja')
plt.ylim(bottom=0)
plt.xlim(6,80)
#plt.grid(True)

# Guarda la gráfica en un archivo de imagen (por ejemplo, density_plot.png)
#plt.savefig('density_plot.png')

# Muestra la gráfica en una ventana (opcional)
plt.show()

