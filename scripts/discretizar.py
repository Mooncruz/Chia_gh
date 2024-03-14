
def reader_outgro(filename):
    frames=[]
    current_frame=[]
    with open (filename, 'r') as file:
        lines =[]
        contador=0
        for line in file:
            line=line.split()
            lines.append(line)
        length_file=(len(lines))
        length_one_frame=67569
        frame_total= length_file/length_one_frame

        for line in lines:
            current_frame.append(line)
            contador +=1
            if contador == length_one_frame:
                frames.append(current_frame)
                current_frame=[]
                contador=0

    return frames
		
def read_data(lineas):
    '''recibe lineas de texto y las guarda'''
    records=[]
    for line in lineas:
        records.append(line)
    return records


def lectura_conf(archivo):
    '''recibe un archivo de tipo conf.gro, extrae y guarda los datos: 
Encabezado, número de segmentos y la información de cada segmento'''
    with open (archivo,'r') as f:
        d = read_data(f)
        last = d[-1]
        head1 = d[0]
        nseg = int(d[1])
        dat = d[2:]
        datos = []
        for i,line in enumerate(dat):
            line = line.split()           
            if i <= 9998:	  
                try:
                    l = {'system': line[0], 'typ': line[1], 'id': int(line[2]), 'coorx': float(line[3]),'coory': float(line[4]), 'coorz': float(line[5])}
                    datos.append(l)
                    
                except (ValueError, IndexError):
                    print("Error en el bloque:", current_block)

        #for i,line in enumerate(dat):
            elif i >= 9999: #cambie if por elif verificar si funciona

                parte=line[1]
                parte1 = parte[:2]
                parte2 = parte[2:]
                
                try:
                    l = {'system': line[0], 'typ': parte1, 'id': int(parte2), 'coorx': float(line[2]),'coory': float(line[3]), 'coorz': float(line[4])}
               
                
                    if len(l) == 3:
                        raise IndexError('Se terminó')
                    datos.append(l)
                       

                except (ValueError, IndexError):
                    print("Se terminó el archivo")

    return datos
   
def discretiza(datos):
    import numpy as np
    
    alfas=datos.copy()
    coordinate_z_L6=[]
    coordinate_z_L4=[]
    coordinate_z_L1=[]
    count1=0
    count2=0
    count3=0
    for index,configuration in enumerate(alfas):
        if configuration['typ'] =='L6':
            count1 += 1
            coordinate_z_L6.append(configuration['coorz'])

        elif configuration['typ'] =='L4':
            count2 += 1
            coordinate_z_L4.append(configuration['coorz'])

        elif configuration['typ'] =='L1':
            count3 += 1
            coordinate_z_L1.append(configuration['coorz'])

    num_columnasL6=len(coordinate_z_L6)
    num_columnasL4=len(coordinate_z_L4)
    num_columnasL1=len(coordinate_z_L1)
    num_filas=100
    valores =[round(i * 6.15,2) for i in range(num_filas)]
    
    matriz_L6=np.zeros((num_columnasL6,num_filas),dtype=float)
    matriz_L4=np.zeros((num_columnasL4,num_filas),dtype=float)
    matriz_L1=np.zeros((num_columnasL1,num_filas),dtype=float)

            
    for x,valor in enumerate (valores):
        for t,i in enumerate (coordinate_z_L6):
            if valor<=  i < valor + 6.15:
                matriz_L6[t,x] += 1
                

    
    for x,valor in enumerate (valores):
        for t,i in enumerate (coordinate_z_L4):
            if valor<=  i < valor + 6.15:
                matriz_L4[t,x] += 1

    
    for x,valor in enumerate (valores):
        for t,i in enumerate (coordinate_z_L1):
            if valor<=  i < valor + 6.15:
                matriz_L1[t,x] += 1

    
    np.savetxt('matriz_L6.dat', matriz_L6, fmt='%d', delimiter=',')
    np.savetxt('matriz_L4.dat', matriz_L4, fmt='%d', delimiter=',')
    np.savetxt('matriz_L1.dat', matriz_L1, fmt='%d', delimiter=',')

        
    return matriz_L6, matriz_L4, matriz_L1, valores

def densidad(matriz_L6, matriz_L4, matriz_L1, valores):
    import numpy as np

    volumen_slide= (6.15*615*615)
    densidad_L6= []
    densidad_L4= []
    densidad_L1= []

    suma_filas_L6=np.sum(matriz_L6,axis=0) #sum number of segment in each configuration
    suma_filas_L4=np.sum(matriz_L4,axis=0) #sum number of segment in each configuration
    suma_filas_L1=np.sum(matriz_L1,axis=0) #sum number of segment in each configuration

    densidades_L6=np.divide(suma_filas_L6,volumen_slide)
    densidad_L6=np.column_stack((valores,densidades_L6))
    

    densidades_L4=np.divide(suma_filas_L4,volumen_slide)
    densidad_L4=np.column_stack((valores,densidades_L4))
    #densidad_L4.append(densidades_L6)

    densidades_L1=np.divide(suma_filas_L1,volumen_slide)
    densidad_L1=np.column_stack((valores,densidades_L1))
    #densidad_L1.append(densidades_L6)

  
    np.savetxt('densidad_L6.dat', densidad_L6, fmt=['%.3f','%.6e'], delimiter='\t')
    np.savetxt('densidad_L4.dat', densidad_L4, fmt=['%.3f','%.6e'], delimiter='\t')
    np.savetxt('densidad_L1.dat', densidad_L1, fmt=['%.3f','%.6e'], delimiter='\t')
  
    #print(densidad_L1)
    #exit()
    return densidad_L6, densidad_L4, densidad_L1


def graficar_densidad(densidad_L6,densidad_L4,densidad_L1):
    import matplotlib.pyplot as plt

    plt.plot(densidad_L6[:,0],densidad_L6[:,1])
    #plt.plot(densidad_L4[1],densidad_L4[0])
    #plt.plot(densidad_L1[1],densidad_L1[0])
    
    plt.show()

    return()
    
#frames = reader_outgro('out.gro')

datos=lectura_conf('simu.gro')

matriz_L6, matriz_L4,matriz_L1,values=discretiza(datos)

densidad_L6, densidad_L4, densidad_L1=densidad(matriz_L6, matriz_L4,matriz_L1,values)

graficar_densidad(densidad_L6, densidad_L4, densidad_L1)


