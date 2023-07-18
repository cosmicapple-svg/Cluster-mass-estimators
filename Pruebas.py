#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from Estimadores import *
from cosmo import *
import os
import time

start = time.time()


def Masas(dirr, d):
    MV  = EstimadorVirial(dirr, d)
    MM  = EstimadorMediana(dirr, d)
    MP  = EstimadorPromedio(dirr, d)
    MPr = EstimadorProyectada(dirr, d)
    
    masas = np.array([MV, MM, MP, MPr])/(1e14)
    return np.round(masas,2)
    


#
#----------------------------------------------------------------#
filesdir = "C://Users//hugos//Documents//Verano2022//Datos//DatosOut"
os.chdir(filesdir)
archivos = os.listdir(filesdir)

#Hay que buscar como sacar estos automáticamente
Zs = [0.0690, 0.0550, 0.0450, 0.0690, 0.0858, 0.0705, 0.0795, 0.0801, 
      0.0579, 0.0419, 0.0761]

MasasPopesso = [6.63, 4.03, 3.57,10.27, 11.57, 5.83, 19.56, 4.09, 4.53, 9.40 ]



Ms = []

n= len(archivos)
MatrizMasas = np.empty([n, 8])

err = lambda x, y: round(np.abs( (y - x)/y  ), 2)
    

i=0
for archivo in archivos:
    #print(archivo)
    d = dist(Zs[i])*3.086e+22
    masas = Masas(archivo, d)
    #print("\n")
    #Llenamos masa y su error respecto a Popesso
    MatrizMasas[i, 0:2] = masas[0], err(MasasPopesso[i], masas[0])
    MatrizMasas[i, 2:4] = masas[1], err(MasasPopesso[i], masas[1])
    MatrizMasas[i, 4:6] = masas[2], err(MasasPopesso[i], masas[2])
    MatrizMasas[i, 6:8] = masas[3], err(MasasPopesso[i], masas[3])
    i +=1

MatrizMasas 
nombres = ["MV", "ErrMV", "MM", "ErrMM", "MP", "ErrMP", "MPr", "ErrMPr"]
DatosMasas = pd.DataFrame(MatrizMasas, columns= nombres)
DatosMasas.insert(0,"Nombre", archivos)
DatosMasas.insert(9, "Popesso", MasasPopesso)

os.chdir("C://Users//hugos//Documents//Verano2022//Datos")
DatosMasas.to_csv("DatosMasas.csv")

end= time.time()

print("Tiempo: ", end-start)
 

# Cálculo de errores por bootstrap


from astropy.stats import bootstrap
from astropy.utils import NumpyRNGContext






















