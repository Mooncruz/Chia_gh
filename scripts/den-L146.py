import os
import matplotlib.pyplot as plt

lmbd=['0.1','0.6','1.0']
x=[i * 2.3925 for i in range(201)]
x.pop(0)

densityL6=[[],[],[]]
densityL14=[[],[],[]]

for l,lbd in enumerate (lmbd):
    os.chdir('surface50-'+lbd)
    with open ('densityL6_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                densityL6[l].append(float(line.split()[1]))
    with open('densityL14_radial.dat','r') as file:
        for line in file:
            densityL14[l].append(float(line.split()[1]))
    os.chdir('..')

densityL6_0=densityL6[0].copy()
densityL6_1=densityL6[1].copy()
densityL6_2=densityL6[2].copy()
densityL14_0=densityL14[0].copy()
densityL14_1=densityL14[1].copy()
densityL14_2=densityL14[2].copy()
    
plt.plot(x,densityL6_0,color='red',label='L6 λ=0.1')
plt.plot(x,densityL14_0,color='blue',label='L14 λ=0.1')
plt.plot(x,densityL6_1,color='maroon',label='L6 λ=0.6')
plt.plot(x,densityL14_1,color='navy',label='L14 λ=0.6')
plt.plot(x,densityL6_2,color='indianred', label='L6 λ=1.0')
plt.plot(x,densityL14_2,color='royalblue',label='L14 λ=1.0')
plt.xlim(2.3925,200)
plt.xlabel('Radio del gel (nm)')
plt.ylabel('Densidad (segmentos \ nm^3)')
plt.title('Densidades comparativas')
plt.legend(fontsize=12)
plt.subplots_adjust(left=0.15,right=0.85,top=0.9,bottom=0.1)
plt.gcf().set_size_inches(8,6)
plt.savefig('Densidad_comparativa')
plt.show()
