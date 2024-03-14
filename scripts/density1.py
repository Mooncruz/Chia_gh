import os
import numpy as np
import matplotlib.pyplot as plt

# Lista de valores lambda
#lmbd = ['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']
lmbd = ['0.1','0.6','0.7','0.8','0.9','1.0']
#lmbd = ['0.1','0.2','0.3','0.4','0.5','0.8']

x = []
density = []

for lbd in lmbd:
    # Cambia al directorio de la carpeta actual
    os.chdir('surface25-' + lbd)
    
    x_values = []
    density_values = []

    # Abre el archivo 'density.xvg' y carga los datos
    with open('density.xvg', 'r') as gyrt:
        for line in gyrt:
            if line.startswith(('@', '#')):
                continue
            columns = line.split()
            if len(columns) == 2:
                x_value, density_value = map(float, columns)
                x_values.append(x_value)
                density_values.append(density_value)

    # Calcula el centro del sistema y ajusta las coordenadas
    center = np.mean(x_values)
    x_centered = [value - center for value in x_values]
    
    # Filtra los valores positivos en el eje x
    x_positive = [x for x in x_centered if x > 0]
    density_positive = [density for i, density in enumerate(density_values) if x_centered[i] > 0]

    x.append(x_positive)
    density.append(density_positive)

    # Cambia de nuevo al directorio principal
    os.chdir('..')

# Crea la gráfica de densidad para cada valor lambda
for i, lbd in enumerate(lmbd):
    plt.plot(x[i], density[i], label=f'λ = {lbd}')

plt.xlabel('Posición en x (nm)')
plt.ylabel('Densidad Kg / $m^3$')
plt.text(10,0.00015,'Surfacegel30-25',fontsize=12,color='black',backgroundcolor='white',bbox=dict(facecolor='white',edgecolor='black',boxstyle='round,pad=0.2'))
#plt.title('Densidad centrada en la caja')
plt.legend()
plt.xlim(6, 80)

# Muestra la gráfica en una ventana (opcional)
plt.show()
