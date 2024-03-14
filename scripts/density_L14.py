import os
import numpy as np
import matplotlib.pyplot as plt

# Carga los datos de densidad desde el archivo

lmbd=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']
x=[i * 2.3925 for i in range(201)]
x.pop(0)
densityL4=[[]for _ in range(10)]
densityL1=[[]for _ in range(10)]
promedio=[]

for l,lbd in enumerate(lmbd):
    os.chdir('surface50-'+ lbd)
    with open('densityL4_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                densityL4[l].append(float(line.split()[1]))
    with open('densityL1_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                densityL1[l].append(float(line.split()[1]))
    os.chdir('..')
    
    promedio.append(sum(densityL4[l]+densityL1[l])/len(densityL4[l]+densityL1[l]))
    print(sum(densityL4[l]))
    print(sum(densityL1[l]))
    print(len(densityL4[l]))
    print(len(densityL1[l]))

print(promedio)

plt.plot(lmbd, promedio,color='blue',label='Surfacegel30-50')
plt.xlabel('λ')
plt.ylabel('Densidad (segmento \ nm^3)')
plt.title('Densidad de segmentos L1-L4')
plt.legend(fontsize=12)
plt.subplots_adjust(left=0.15, right=0.85, top=0.9, bottom=0.1)
plt.gcf().set_size_inches(8, 6)
#plt.ylim(bottom=0)
#plt.xlim(6,80)
#plt.grid(True)

# Guarda la gráfica en un archivo de imagen (por ejemplo, density_plot.png)
plt.savefig('Density_radial_L14_30-50.png')

# Muestra la gráfica en una ventana (opcional)
plt.show()

