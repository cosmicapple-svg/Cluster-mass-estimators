# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:51:12 2022

@author: Hugo
"""
from Estimadores import *
from Bootstrap import ErrorBootstrap2, ErrorBootstrap3
from PerfilesMasas import *
import numpy as np
import pandas as pd
import time
import os

"""

os.chdir("C://Users//hugos//Documents//Verano2022//Datos//DatosOut")
dirr = "A2670.csv"

#   1. CÁLCULO DE MASAS
ARrel, DECrel, N, Vrel, D, V = PosicionesRelativas(dirr)

masas = Masas2(ARrel, DECrel, Vrel, D)

#   2. CÁLCULO DE ERRORES
errores = ErrorBootstrap2(ARrel, DECrel, Vrel, D, nboot=10)

MasasTotal = pd.DataFrame(np.array([masas, errores] ), 
                          columns=['Virial', 'Mediana', 'Promedio', 'Proyectada'])

file = "A2670.csv" 
os.chdir("C://Users//hugos//Documents//Verano2022//Resultados")
nombre = "".join(["Mass", file])
MasasTotal.to_csv(nombre )



#   3. MASAS POR ANILLOS Y EXPORTACIÓN
MasasAnillos = MasasAnillos3(ARrel, DECrel, N, Vrel, D/(3.086e19)) #Distancia en kpc

Anillos = pd.DataFrame(MasasAnillos, 
            columns=['V', 'M', 'P', 'A','ErrA', 'ErrM', 'ErrP', 'ErrA' ])

nombre2 = "".join(["Anillo", file])
Anillos.to_csv(nombre2)



#  4. PERFILES DE MASA
nombrecumulo = file[:-4]
PerfilMasa(MasasAnillos, nombrecumulo)

"""

def Final(cumulo):
    os.chdir("C://Users//hugos//Documents//Verano2022//Datos//DatosOut")

    #   1. CÁLCULO DE MASAS
    ARrel, DECrel, N, Vrel, D, V = PosicionesRelativas(cumulo)

    masas = Masas2(ARrel, DECrel, Vrel, D)

    #   2. CÁLCULO DE ERRORES
    errores = ErrorBootstrap2(ARrel, DECrel, Vrel, D, nboot=1000)

    MasasTotal = pd.DataFrame(np.array([masas, errores] ), 
                              columns=['Virial', 'Mediana', 'Promedio', 'Proyectada'])

    os.chdir("C://Users//hugos//Documents//Verano2022//Resultados")
    nombre = "".join(["Mass", cumulo])
    MasasTotal.to_csv(nombre )



    #   3. MASAS POR ANILLOS Y EXPORTACIÓN
    MasasAnillos = MasasAnillos3(ARrel, DECrel, N, Vrel, D/(3.086e19)) #Distancia en kpc

    Anillos = pd.DataFrame(MasasAnillos, 
                columns=['V', 'M', 'P', 'A','ErrA', 'ErrM', 'ErrP', 'ErrA' ])

    nombre2 = "".join(["Anillo", cumulo])
    Anillos.to_csv(nombre2)



    #  4. PERFILES DE MASA
    nombrecumulo = cumulo[:-4]
    PerfilMasa(MasasAnillos, nombrecumulo)


filesdir = "C://Users//hugos//Documents//Verano2022//Datos//DatosOut"
os.chdir(filesdir)
archivos = os.listdir(filesdir)

for cumulo in archivos[1:]:
    print(cumulo)
    Final(cumulo)
    


