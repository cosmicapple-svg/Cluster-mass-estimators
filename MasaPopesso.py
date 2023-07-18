# -*- coding: utf-8 -*-
"""

Estimador estilo Popesso 
Created on Mon Jul 25 09:15:16 2022

@author: Hugo

"""

import numpy as np
import pandas as pd


#Leemos los archivos
archivo = "Archivo"
datos = pd.read_csv(archivo)

AR = datos.ra*(np.pi/180)      #En radianes 
DEC = datos.dec*(np.pi/180)    #En radianes
V = datos.vel*1000             #En m/s
N = len(AR)



#SELECCIÓN DE MIEMBROS


#1. Galaxias dentro de un radio de Abell

RAbell = 2.15    #En Mpc
Vlim = 4000      #En km/s

centro = [np.mean(AR), np.mean(DEC)]
Vmean = np.mean(V)

#Posiciones y velocidades relativas filtradas
ARf=[]; DECf = []; Vf=[];  

for i in range(N):
    ARrel = AR[i] - centro[0]
    DECrel = DEC[i] - centro[1]
    Vrel = V[i] - Vmean
    r = np.sqrt(ARrel**2 + DECrel**2)
    
    if r<= RAbell and  np.abs(Vrel) < Vlim:
        ARf.append(ARrel); DECf.append(DECrel)
        Vf.append(Vrel)
        


        
        
    





























