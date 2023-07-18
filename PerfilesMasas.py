# -*- coding: utf-8 -*-



import numpy as np
import pandas as pd
from cosmo import dist
from Estimadores import *
import matplotlib.pyplot as plt 
from Bootstrap import*
"""
dirr = "Datos//DatosOut//A2255_dccoutcut.csv"

datos = pd.read_csv(dirr)

# Posiciones            
AR = datos.ra*(np.pi/180)  #En radianes 
DEC = datos.dec*(np.pi/180)  #En radianes
V = datos.vel*1000          #En m/s
N = len(AR)

#Centroide y Velocidad media
centro = [np.mean(AR), np.mean(DEC)]; Vmean = np.mean(V)
#Redshift
Z = Vmean/299792458
#Distancia
D = dist(Z)*1000 #En kpc
"""

"""
radios = []

for i in range(N):
    ARrel = AR[i] - centro[0]
    DECrel = DEC[i] - centro[1]
    Vrel = V[i] - Vmean
    r = np.sqrt(ARrel**2 + DECrel**2)*D
    radios.append(r)

Rmax = max(radios)

interval = 10
delta = Rmax/10
"""

"""
AR500 =[];  AR1000=[];  AR1500=[];  AR2000=[];  AR2500=[]
DEC500 =[]; DEC1000=[]; DEC1500=[]; DEC2000=[]; DEC2500=[]
V500 =[];   V1000=[];   V1500=[];   V2000=[];   V2500=[]

for i in range(N):
    ARrel = AR[i] - centro[0]
    DECrel = DEC[i] - centro[1]
    Vrel = V[i] - Vmean
    r = np.sqrt(ARrel**2 + DECrel**2)*D
   
    if r <= 500:
        AR500.append(ARrel); DEC500.append(DECrel); V500.append(Vrel)
    elif r<=1000:
        AR1000.append(ARrel); DEC1000.append(DECrel); V1000.append(Vrel)
    elif r<=1500:
        AR1500.append(ARrel); DEC1500.append(DECrel); V1500.append(Vrel)
    elif r<=2000:
        AR2000.append(ARrel); DEC2000.append(DECrel); V2000.append(Vrel)
    else:
        AR2500.append(ARrel); DEC2500.append(DECrel); V2500.append(Vrel)
        
        
Sep = np.array( [AR500, DEC500, V500,
                 AR1000, DEC1000, V1000,
                 AR1500, DEC1500, V1500,
                 AR2000, DEC2000, V2000,
                 AR2500, DEC2500, V2500], dtype='object')

Sep = Sep.reshape(5, 3)


Masas = np.zeros([5, 4])
Funciones = [EstimadorVirialBoot, 
             EstimadorMedianaBoot,
             EstimadorProyectadaBoot,
             EstimadorPromedioBoot]

for i in range(5):
    j=0
    for Estimador in Funciones:
        Masas[i, j] = Estimador(Sep[i, 0], Sep[i, 1], Sep[i, 2], D*3.086e19)
        j+=1
   
MATRIZ DE MASAS

        Virial      Mediana     Proyectada      Promedio
 500
 
1000

1500

2000

2500


Rs = [500, 1000, 1500, 2000, 2500]
Mass = [sum(Masas[:1,0]), sum(Masas[:2, 0]), 
        sum(Masas[:3, 0]), sum(Masas[:4,0]), sum(Masas[:5, 0]) ]
    
plt.scatter(Rs, Mass, marker='.' )
plt.xlabel("Radio (Kpc)"); plt.ylabel("Masa (1e14 M0)")
plt.show()
"""

def MasasAnillos(dirr):
    datos = pd.read_csv(dirr)

    # Posiciones            
    AR = datos.ra*(np.pi/180)  #En radianes 
    DEC = datos.dec*(np.pi/180)  #En radianes
    V = datos.vel*1000          #En m/s
    N = len(AR)

    #Centroide y Velocidad media
    centro = [np.mean(AR), np.mean(DEC)]; Vmean = np.mean(V)
    #Redshift
    Z = Vmean/299792458
    #Distancia
    D = dist(Z)*1000 #En kpc
    
    #Se llenan arreglos con datos para cada 500 kpc
    AR500 =[];  AR1000=[];  AR1500=[];  AR2000=[];  AR2500=[]
    DEC500 =[]; DEC1000=[]; DEC1500=[]; DEC2000=[]; DEC2500=[]
    V500 =[];   V1000=[];   V1500=[];   V2000=[];   V2500=[]

    for i in range(N):
        ARrel = AR[i] - centro[0]
        DECrel = DEC[i] - centro[1]
        Vrel = V[i] - Vmean
        r = np.sqrt(ARrel**2 + DECrel**2)*D
       
        if r <= 500:
            AR500.append(ARrel); DEC500.append(DECrel); V500.append(Vrel)
        elif r<=1000:
            AR1000.append(ARrel); DEC1000.append(DECrel); V1000.append(Vrel)
        elif r<=1500:
            AR1500.append(ARrel); DEC1500.append(DECrel); V1500.append(Vrel)
        elif r<=2000:
            AR2000.append(ARrel); DEC2000.append(DECrel); V2000.append(Vrel)
        elif r<=2500:
            AR2500.append(ARrel); DEC2500.append(DECrel); V2500.append(Vrel)
    
    #Creamos un vector con los arreglos (así será la forma de la matriz)
    Sep = np.array( [AR500, DEC500, V500,
                     AR1000, DEC1000, V1000,
                     AR1500, DEC1500, V1500,
                     AR2000, DEC2000, V2000,
                     AR2500, DEC2500, V2500], dtype='object')
    #Se escribe en forma matricial
    Sep = Sep.reshape(5, 3)
    
    #Creamos una matriz vacía y un vector con la funciones para estimar masas
    Masas = np.zeros([5, 4])
    Funciones = [EstimadorVirialBoot, 
                 EstimadorMedianaBoot,
                 EstimadorProyectadaBoot,
                 EstimadorPromedioBoot]
    
    #Se llena la matriz de masas
    #Ciclo por radio
    for i in range(5): 
        j=0
        #Ciclo para estimar masas
        for Estimador in Funciones:
            #Llenado de la matrizP
            Masas[i, j] = Estimador(Sep[i, 0], Sep[i, 1], Sep[i, 2], D*3.086e19)
            j+=1
    
    """ MATRIZ DE MASAS

            Virial      Mediana     Proyectada      Promedio
     500
     
    1000

    1500

    2000

    2500
    """
    
    return Masas


#Distancia en kiloparsec
def MasasAnillos2(ARrel, DECrel, N, Vrel, D):
    #Se llenan arreglos con datos para cada 500 kpc
    AR500 =[];  AR1000=[];  AR1500=[];  AR2000=[];  AR2500=[]
    DEC500 =[]; DEC1000=[]; DEC1500=[]; DEC2000=[]; DEC2500=[]
    V500 =[];   V1000=[];   V1500=[];   V2000=[];   V2500=[]

    for i in range(N):
        r = np.sqrt(ARrel[i]**2 + DECrel[i]**2)*D
        #print(r)
       
        if r <= 500:
            AR500.append(ARrel[i]); DEC500.append(DECrel[i]); V500.append(Vrel[i])
        elif r<=1000:
            AR1000.append(ARrel[i]); DEC1000.append(DECrel[i]); V1000.append(Vrel[i])
        elif r<=1500:
            AR1500.append(ARrel[i]); DEC1500.append(DECrel[i]); V1500.append(Vrel[i])
        elif r<=2000:
            AR2000.append(ARrel[i]); DEC2000.append(DECrel[i]); V2000.append(Vrel[i])
        else: 
            AR2500.append(ARrel[i]); DEC2500.append(DECrel[i]); V2500.append(Vrel[i])
    
    #Creamos un vector con los arreglos (así será la forma de la matriz)
    Sep = np.array( [AR500, DEC500, V500,
                     AR1000, DEC1000, V1000,
                     AR1500, DEC1500, V1500,
                     AR2000, DEC2000, V2000,
                     AR2500, DEC2500, V2500], dtype='object')
    #Se escribe en forma 
    Sep = Sep.reshape(5, 3)
    #print( len(AR500)+ len(AR1000)+ len(AR1500)+len(AR2000) +len(AR2500)== N)
    #print( EstimadorVirialBoot( Sep[0, 0], Sep[0, 1], Sep[0, 2], D*(3.086e19) ) )
    
    #Creamos una matriz vacía y un vector con la funciones para estimar masas
    Masas = np.zeros([5, 4])
    Funciones = [EstimadorVirialBoot, 
                 EstimadorMedianaBoot,
                 EstimadorProyectadaBoot,
                 EstimadorPromedioBoot]
    
    #Se llena la matriz de masas
    #Ciclo por radio
    D = D*(3.086e19) #En metros
    for i in range(5): 
        j=0
        #Ciclo para estimar masas
        for Estimador in Funciones:
            #Llenado de la matrizP
            Masas[i, j] = Estimador(Sep[i, 0], Sep[i, 1], Sep[i, 2], D)
            errores = ErrorBootstrap2(Sep[i, 0], Sep[i, 1], Sep[i, 2], D, nboot=10)
            j+=1
            
    
    """ MATRIZ DE MASAS

            Virial      Mediana     Proyectada      Promedio3
     500
     
    1000

    1500

    2000

    2500
    """
    
    return Masas


def PerfilMasa(Masas):
    
    Rs = [500, 1000, 1500, 2000, 2500]
    Mass = [sum(Masas[:1,0]), sum(Masas[:2, 0]), 
            sum(Masas[:3, 0]), sum(Masas[:4,0]), sum(Masas[:5, 0]) ]
        
    plt.scatter(Rs, Mass, marker='.' )
    plt.xlabel("Radio (Kpc)"); plt.ylabel("Masa (1e14 M0)")
    plt.show()
    
    

def MasasAnillos3(ARrel, DECrel, N, Vrel, D):
    #Se llenan arreglos con datos para cada 500 kpc
    AR500 =[];  AR1000=[];  AR1500=[];  AR2000=[];  AR2500=[]
    DEC500 =[]; DEC1000=[]; DEC1500=[]; DEC2000=[]; DEC2500=[]
    V500 =[];   V1000=[];   V1500=[];   V2000=[];   V2500=[]

    for i in range(N):
        r = np.sqrt(ARrel[i]**2 + DECrel[i]**2)*D
        #print(r)
       
        if r <= 500:
            AR500.append(ARrel[i]); DEC500.append(DECrel[i]); V500.append(Vrel[i])
        elif r<=1000:
            AR1000.append(ARrel[i]); DEC1000.append(DECrel[i]); V1000.append(Vrel[i])
        elif r<=1500:
            AR1500.append(ARrel[i]); DEC1500.append(DECrel[i]); V1500.append(Vrel[i])
        elif r<=2000:
            AR2000.append(ARrel[i]); DEC2000.append(DECrel[i]); V2000.append(Vrel[i])
        else: 
            AR2500.append(ARrel[i]); DEC2500.append(DECrel[i]); V2500.append(Vrel[i])
    
    #Creamos un vector con los arreglos (así será la forma de la matriz)
    Sep = np.array( [AR500, DEC500, V500,
                     AR1000, DEC1000, V1000,
                     AR1500, DEC1500, V1500,
                     AR2000, DEC2000, V2000,
                     AR2500, DEC2500, V2500], dtype='object')
    #Se escribe en forma 
    Sep = Sep.reshape(5, 3)
    #print( len(AR500)+ len(AR1000)+ len(AR1500)+len(AR2000) +len(AR2500)== N)
    #print( EstimadorVirialBoot( Sep[0, 0], Sep[0, 1], Sep[0, 2], D*(3.086e19) ) )
    
    #Creamos una matriz vacía y un vector con la funciones para estimar masas
    Masas = np.zeros([5, 4])
    Funciones = [EstimadorVirialBoot, 
                 EstimadorMedianaBoot,
                 EstimadorProyectadaBoot,
                 EstimadorPromedioBoot]
    
    #Se llena la matriz de masas
    #Ciclo por radio
    D = D*(3.086e19) #En metros
    Errores = np.zeros([5, 4])
    for i in range(5): 
        j=0
        #Ciclo para estimar masas
        for Estimador in Funciones:
            #Llenado de la matrizP
            Masas[i, j] = Estimador(Sep[i, 0], Sep[i, 1], Sep[i, 2], D)
            Errores[i, j] = ErrorBootstrap3(Sep[i, 0], Sep[i, 1], Sep[i, 2], D, 1000, Estimador)
            j+=1
    
    return np.concatenate((Masas, Errores), axis=1)


    """ MATRIZ DE MASAS Y ERRORES

            Virial  Mediana  Proyectada Promedio ErrV ErrM ErrP ErrAv
     500
     
    1000

    1500

    2000

    2500
    """


def PerfilMasa(MasasAnillos, nombrecumulo):   
    R = np.arange(500, 3000, 500)
    plt.style.use('ggplot')
    plt.xlabel(r"$Radio\;\; (kpc)$"); plt.ylabel(r"$Masa\;\; (10^{14} M_{\odot})$")
    plt.title(nombrecumulo)  
    est = ['Virial', 'Mediana', 'Proyectada', 'Promedio']           
    colores = ['#1279c8', '#e53939', '#68a247', '#14c5b6']

    for i in range(4):
        plt.errorbar(R, MasasAnillos[:, i], yerr=MasasAnillos[:, i+4], fmt='.k', 
                     label=est[i], c = colores[i], elinewidth=0.5)
        
    name = "".join(["Perfil", nombrecumulo])
    plt.legend()
    plt.savefig(name, dpi=300)
    plt.show()
    








