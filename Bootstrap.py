# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 11:05:37 2022

@author: Hugo
"""

import numpy as np
import pandas as pd
from cosmo import dist
from Estimadores import *
from astropy.stats import bootstrap
from astropy.utils.misc import NumpyRNGContext
from random import randint

"""
#Bootstrap con velocidades 


dirr = "Datos//DatosOut//A2593_dccoutcut.csv"

#Posiciones y velocidades relativas
ARrel, DECrel, N, Vrel, Z = PosicionesRelativas2(dirr)
#Las convertimos en Numpy Arrays
ARrel = np.array(ARrel)
DECrel = np.array(DECrel)
Vrel = np.array(Vrel)

#Reordenamos las velocidades y posiciones 1000 veces
nboot= 100
from random import randint

seed =randint(0, 1000) 
with NumpyRNGContext():
    Vboot = bootstrap(Vrel, nboot ) 
    ARboot = bootstrap(ARrel, nboot )
    DECboot = bootstrap(DECrel, nboot)
    
MV =[]; MA = []; MM = []; MP = []; D = dist(Z)*3.086e+22


for i in range(nboot):
    print(".")
    Mvir = EstimadorVirialBoot( ARboot[i, :], DECboot[i,:], Vboot[i,:],  D  )
    Mav = EstimadorPromedioBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D  )
    Mpro = EstimadorProyectadaBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D )
    Mmed = EstimadorMedianaBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D )
    
    MV.append(Mvir); MA.append(Mav); MM.append(Mmed); MP.append(Mpro)

plt.hist(MV)
plt.show()
plt.hist(MA)
plt.show()
plt.hist(MM)
plt.show()
plt.hist(MP)
plt.show()


errMV = round(np.std(MV)/1e14, 2)
errMA = round(np.std(MA)/1e14, 2)
errMM = round(np.std(MM)/1e14, 2)
errMP = round(np.std(MP)/1e14, 2)


"""
def ErrorBootstrap(dirr, nboot):
    
    #Posiciones relativas y distancia
    ARrel, DECrel, N, Vrel, D = PosicionesRelativas(dirr)

    #Conversión a numpy array
    ARrel = np.array(ARrel)
    DECrel = np.array(DECrel)
    Vrel = np.array(Vrel)
    
    #Reordenamos las velocidades y posiciones nboot veces
    seed =randint(0, 1000) 
    with NumpyRNGContext(seed):
        Vboot = bootstrap(Vrel, nboot )    #Matrices [ nboot x len(Vrel)  ]
        ARboot = bootstrap(ARrel, nboot )
        DECboot = bootstrap(DECrel, nboot)
    
    #Cálculamos nuevamente las masas con los reacomodos aleatorios
    
    ### Se podría simplificar corriendo un for en las funciones
    MV =[]; MA = []; MM = []; MP = []
    for i in range(nboot):
        #print(".\t ")
        Mvir = EstimadorVirialBoot( ARboot[i, :], DECboot[i,:], Vboot[i,:],  D  )
        Mav =  EstimadorPromedioBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D  )
        Mpro = EstimadorProyectadaBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D )
        Mmed = EstimadorMedianaBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D )
        
        MV.append(Mvir); MA.append(Mav); MM.append(Mmed); MP.append(Mpro)
    
    errMV = np.std(MV); errMA = np.std(MA)
    errMM = np.std(MM); errMP = np.std(MP)
    
    errores = np.array([errMV, errMM, errMP, errMA])
    
    return np.round(errores, 3)

def ErrorBootstrap2(ARrel, DECrel, Vrel, D, nboot):
    N = len(ARrel)
    #Conversión a numpy array
    ARrel = np.array(ARrel)
    DECrel = np.array(DECrel)
    Vrel = np.array(Vrel)
    
    #Reordenamos las velocidades y posiciones nboot veces
    seed =randint(0, 1000) 
    with NumpyRNGContext(seed):
        Vboot = bootstrap(Vrel, nboot )    #Matrices [ nboot x len(Vrel)  ]
        ARboot = bootstrap(ARrel, nboot )
        DECboot = bootstrap(DECrel, nboot)
    
    #Cálculamos nuevamente las masas con los reacomodos aleatorios
    
    ### Se podría simplificar corriendo un for en las funciones
    MV =[]; MA = []; MM = []; MP = []
    for i in range(nboot):
        #print(".\t ")
        Mvir = EstimadorVirialBoot( ARboot[i, :], DECboot[i,:], Vboot[i,:],  D  )
        Mav =  EstimadorPromedioBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D  )
        Mpro = EstimadorProyectadaBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D )
        Mmed = EstimadorMedianaBoot( ARboot[i, :], DECboot[i,:], Vboot[i, :], D )
        
        MV.append(Mvir); MA.append(Mav); MM.append(Mmed); MP.append(Mpro)
    
    errMV = np.std(MV); errMA = np.std(MA)
    errMM = np.std(MM); errMP = np.std(MP)
    
    errores = np.array([errMV, errMM, errMP, errMA])
    
    return np.round(errores, 3)

    
    
def ErrorBootstrap3(ARrel, DECrel, Vrel, D, nboot, Estimador):
    N = len(ARrel)
    #Conversión a numpy array
    ARrel = np.array(ARrel)
    DECrel = np.array(DECrel)
    Vrel = np.array(Vrel)
    
    #Reordenamos las velocidades y posiciones nboot veces
    seed =randint(0, 1000) 
    with NumpyRNGContext(seed):
        Vboot = bootstrap(Vrel, nboot )    #Matrices [ nboot x len(Vrel)  ]
        ARboot = bootstrap(ARrel, nboot )
        DECboot = bootstrap(DECrel, nboot)
    
    #Cálculamos nuevamente las masas con los reacomodos aleatorios
    
    Estimaciones = []
    for i in range(nboot):
        #print(".\t ")
        Estimacion = Estimador( ARboot[i, :], DECboot[i,:], Vboot[i,:],  D  )
        
        Estimaciones.append(Estimacion)
    
    ErrEst = np.std(Estimaciones)
    
    
    return round(ErrEst, 3)






















