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
        for line in dat:
            line = line.split()
            try:
                l = {'system': line[0], 'typ':line[1], 'id':int(line[2]), 'coorx':float(line[3]), 'coory':float(line[4]), 'coorz':float(line[5])}

                if len(l) == 3:
                    raise IndexError('se terminó')
                datos.append(l)

            except ValueError:
                print('Fin del archivo')
    
    return datos, head1, nseg, last

def re_set_datos(dat):
    '''dado un set de datos los re-setea y convierte todos los LJ2 en LJ1'''
    ''' Sirve para transformar str dentro de un archivo'''
    for i in dat:
        if i['typ'] == 'LJ2':
            i['typ'] = 'LJ1'
    return dat

def ids_aa(datos,at):
    '''Identifica los ìndices para un tipo de àtomos en especìfico'''
    ids = []
    j  = -1
    for i in datos:
        j += 1
        if i['typ'] == at:
            ids.append(j)
    return ids

def sorteo(dat,ids,nl,semilla):
    '''Realiza el sorteo para protonar/desprotonar'''
    '''nl:is the percent that i want of LJ2 in my nanogel 
       semilla: is the random value used in def'''
    import random
    random.seed(semilla)
    n = int(len(ids)*nl/100)
    count = 0
    while n > count:
        ind = random.randrange(0, len(ids))
        i = ids[ind]
        if dat[i]['typ'] == 'LJ1':
            dat[i]['typ'] = 'LJ2'
            count += 1
    return dat, n

'''Una forma de hacer un documento conf.gro'''
def write_gro_file(coordinates, atom_types, filename):
    '''Recibe una matriz con coordenadas, una con tipos de atomos y
    el nombre de un archivo de salida.
    -------
    retorna el el archivo en formato .gro para ser leido por vmd/gromacs'''
    num_atoms = len(coordinates)
    with open(filename, 'w') as f:
        f.write("molecule\n")
        f.write(str(num_atoms) + "\n")

        for i in range(num_atoms):
            f.write("{:>5}{:<5s}{:>5s}{:>5}{:>8.3f}{:>8.3f}{:>8.3f}\n".format(
                '1', 'MOL', atom_types[i], str(i + 1), coordinates[i][0], coordinates[i][1], coordinates[i][2]))

        f.write("   50.00000   50.00000   50.00000\n")  # Box dimensions

    return ()

'''Segunda forma de escribir un documento conf.gro'''

def make_conf(name, dat, head,num_atoms,typ,box2):
    '''Debe entregar una matriz con coordenadas(dat), con tipos de atoms(typ), dimension de la caja(box2), nombre del encabeza del conf.gro(head) y nombre del archivo de salida(name), que en este caso es conf.gro''' 
   
    with open (name,'w') as file:
        file.write(head)
        file.write(f'\n')
        file.write(2*'\t'+str(num_atoms)+'\n')
        for i,j in enumerate(dat):
            file.write(f'{"1GEL":^12s}{"LJ0":3s}{i+1:5d}{j[0]:8.3f}{j[1]:8.3f}{j[2]:8.3f}\n')
        file.write("{:<6.5f}{:>10.5f}{:>10.5f}\n".format(box2, box2, box2))
        return()

make_conf('conf.gro', dat, head, num_atoms, typ, box2)

#write_gro_file(cl_ngb2,typ,'conf.gro')

def new_conf(name, dat, head,nseg,last):
    '''Dada la informaciòn del conf.gro viejo escribe uno nuevo'''
    with open (name, 'w') as out:
        out.write(head)
        out.write(2*'\t'+str(nseg)+'\n')
        for i in dat:
            out.write(f'{i["system"]:^12s}{i["typ"]:3s}{i["id"]:5d}{i["coorx"]:8.3f}{i["coory"]:8.3f}{i["coorz"]:8.3f}\n')
        out.write(last)
    return ()

def bloques(archivo,salida,dat):
    '''Escribe un nuevo archivo topol.top'''
    '''archivo=is file that need be rewrite and salida=is new name for file did in this def'''
    mass = 1.000
    with open(archivo,'r') as f, open(salida,'w')as out:

        for line in f:
            out.write(line)
            if line == '; nr type resnr atom cgnr charge mass\n':
                break

        for i in dat:
            out.write(f'{i["id"]:6d} {i["typ"]:3s}    1      GEl     {i["typ"]:3s}{i["id"]:7d}  {0.0:8.3f}{mass:7.4}\n')


        out.write('\n')
        out.write('\n')
        for line in f:
            pass
            if line == '[ bonds ]\n':
                out.write(line)
                break
        for line in f:
            out.write(line)

    return ()

def archivos(grogro,topol,semilla,maa):

    '''This calls the above def'''

    datos, sistema,nseg,last = lectura_conf(grogro)
    dat = re_set_datos(datos)
    ids = ids_aa(dat, 'LJ1')
    dat, n = sorteo(dat, ids, maa, semilla)
    new_conf('prueba.gro', dat, sistema, nseg, last)
    dat = add_charge(dat)

    bloques(topol, 'otro.top', dat)

mm = "archivos"

def creador_directorios(corrida,semilla,maa):
    import os
    import shutil as sh

    ''' create and copy files'''

    os.mkdir(corrida)
    sh.copy(mm+'/conf.gro', corrida)
    sh.copy(mm+'/topol.top', corrida)
    os.chdir(corrida)

    '''changes files'''

    archivos('conf.gro','topol.top',semilla,maa)
    os.replace('prueba.gro','conf.gro')
    os.replace('otro.top','topol.top')
    os.system('ln -s ../tablas-LJ/* .')
    os.system('bash ../archivos/gromacs.sh')
    os.chdir('../')
    return()



'''if__name__='__main__':
import sys
k = int(sys.argv[1])
maa=int(sys.argv[2])
#import random
#random.seed(1386)
for j in range(k):
    creador_directorios(str(j),j,maa)
    #mm = str(j) '''
    



    
