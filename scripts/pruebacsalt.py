import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import Akima1DInterpolator 

csalt=['1e-1','1e-2','1e-3','1e-4']
density=['0.2','0.4','0.6','0.8']#'1.0','2.5','5.0']
Radio=[[],[],[],[]]

#open de directoy and search the file that contains the average radiu and the save in Radio variable 
for i,cs in enumerate(csalt):
    for d in density:
        os.chdir('csalt-'+str(cs)+'-density-'+str(d)+'-25C-4.65')
        with open('averages.dat','r') as av:
            datos=av.read()
        averages=float(datos.split()[7])
        Radio[i].append(averages)
        os.chdir('..')

# create a new file where organize radius according to density of the MG and the salt concentration
with open ('Rcsalt_35.dat','w') as datf:
    for j, d in enumerate (density):
        datf.write(f'{d}\t{Radio[0][j]}\t{Radio[1][j]}\t{Radio[2][j]}\t{Radio[3][j]}\n')

#convert datas of string to numbers
Radio1=Radio[0].copy()
Radio2=Radio[1].copy()
Radio3=Radio[2].copy()
Radio4=Radio[3].copy()
density=[0.2,0.4,0.6,0.8]#,1.0,2.5,5.0]
        
#create an Akima spline interpolator for each variable
spline1=Akima1DInterpolator(density,Radio1)
#spline1=Akima1DInterpolator(csalt,Radio1)
spline2=Akima1DInterpolator(density,Radio2)
#spline2=Akima1DInterpolator(csalt,Radio2)
spline3=Akima1DInterpolator(density,Radio3)
#spline3=Akima1DInterpolator(csalt,Radio3)
spline4=Akima1DInterpolator(density,Radio4)
#spline4=Akima1DInterpolator(csalt,Radio4)

#Generate interpolated data
density_interpolated=np.linspace(0.2, 0.8, 100) #adjust the number of points as needed
Radio1_interpolated=spline1(density_interpolated)
Radio2_interpolated=spline2(density_interpolated)
Radio3_interpolated=spline3(density_interpolated)
Radio4_interpolated=spline4(density_interpolated)

#plot the data and Akima spline
plt.plot(density,Radio1,'bo',label='[KCl]=$10^-1$ M')
plt.plot(density_interpolated, Radio1_interpolated, 'blue')
plt.plot(density,Radio2,'ro', label='$10^-2$ M')
plt.plot(density_interpolated, Radio2_interpolated, 'red')
plt.plot(density,Radio3,'go', label='$10^-3$ M')
plt.plot(density_interpolated, Radio3_interpolated, 'green')
plt.plot(density,Radio4,'ko', label='$10^-4$ M')
plt.plot(density_interpolated, Radio4_interpolated, 'black')

#plt.plot(csalt,Radio2,'bo',label=r'$\rho$=0.2 mg/mL')
#plt.plot(csalt_interpolated, Radio2_interpolated, 'blue')
#plt.plot(csalt,Radio3,'ro', label='0.4 mg/mL')
#plt.plot(csalt_interpolated, Radio3_interpolated, 'red')
#plt.plot(csalt,Radio4,'go', label='0.6 mg/mL')
#plt.plot(csalt_interpolated, Radio4_interpolated, 'green')
#plt.plot(csalt,Radio5,'ko', label='0.8 mg/mL')
#plt.plot(csalt_interpolated, Radio5_interpolated, 'black')


plt.xlabel('Density MG (mg/mL)')
plt.ylabel('Averages Radius')
#plt.text(42.6,180,'pH=4.65')
plt.grid(True)
plt.legend(frameon=False)
plt.savefig('Rcsalt35_Vmin.png')
plt.show()


                 
