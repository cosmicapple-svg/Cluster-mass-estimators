#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from cosmo import dist


#En el archivo tener encabezados 
#ra-> Ascensión recta, #dec-> declinación y #vel -> Velocidades 


#Constante de gravitación (SI)
G = 6.6743e-11
#Masa solar (kg)
MS = 1.9891e30


def PosicionesRelativas(dirr):
    """ Posiciones Relativas:
        
        Input:
            -dirr: directorio de archivo csv con los datos del cúmulo
        
        Output:
            -ARrel:     vector de ascenciones rectas relativas al centroide
            -DECrel:    vector de declinaciones relativas al centroide
            -N:         número de galaxias en el cúmulo
            -Vrel:      vector de velocidades relativas a la velocidad media
            -D:         distancia de luminosidad (módulo 'cosmo' al cúmulo por 
                        medio de su redshift medio obtenido por la velocidad media
            
    """
    
    datos = pd.read_csv(dirr)
    
    # Posiciones            
    AR = datos.ra*(np.pi/180)    #En radianes 
    DEC = datos.dec*(np.pi/180)  #En radianes
    V = datos.vel*1000           #En m/s
    N = len(AR)
    
    #Centroide y velocidad promedio
    centroide = [np.mean(AR), np.mean(DEC)]
    Vm = np.mean(V); Z = Vm/299792458
    D = dist(Z)*3.08567758128e22 #En metros 

    #Definimos arreglos, después los llenamos acorde a las posiciones y velocidades relativas
    ARrel = [ ]; DECrel = [ ]; Vrel =[];

    for i in range(N):
        ARrel.append( AR[i] - centroide[0] )   
        DECrel.append( DEC[i] - centroide[1] ) 
        Vrel.append( V[i] - Vm )
    
    #Devolvemos Ascencion recta relativa, declinación relativa, #de galaxias, velocidades y distancia 
    return ARrel, DECrel, N, Vrel, D, V

def PosicionesRelativas2(dirr):
    """ Posiciones Relativas:
        
        Input:
            -dirr: directorio de archivo csv con los datos del cúmulo
        
        Output:
            -ARrel:     vector de ascenciones rectas relativas al centroide
            -DECrel:    vector de declinaciones relativas al centroide
            -N:         número de galaxias en el cúmulo
            -Vrel:      vector de velocidades relativas a la velocidad media
            -D:         distancia de luminosidad (módulo 'cosmo' al cúmulo por 
                        medio de su redshift medio obtenido por la velocidad media
            -centroide  centroide del cúmulo
    """
    
    datos = pd.read_csv(dirr)
    
    # Posiciones            
    AR = datos.ra*(np.pi/180)    #En radianes 
    DEC = datos.dec*(np.pi/180)  #En radianes
    V = datos.vel*1000           #En m/s
    N = len(AR)
    
    #Centroide y velocidad promedio
    centroide = [np.mean(AR), np.mean(DEC)]
    Vm = np.mean(V); Z = Vm/299792458
    D = dist(Z)*3.08567758128e22 #En metros 

    #Definimos arreglos, después los llenamos acorde a las posiciones y velocidades relativas
    ARrel = [ ]; DECrel = [ ]; Vrel =[];

    for i in range(N):
        ARrel.append( AR[i] - centroide[0] )   
        DECrel.append( DEC[i] - centroide[1] ) 
        Vrel.append( V[i] - Vm )
    
    #Devolvemos Ascencion recta relativa, declinación relativa, #de galaxias, velocidades y distancia 
    return ARrel, DECrel, N, Vrel, D
    
 
def EstimadorVirial(dirr):

    ARrel, DECrel, N, Vrel, D = PosicionesRelativas(dirr)
    
    #Diferencia angular entre galaxias
    theta = []

    for i in range(N):
        for j in range(i+1, N):
            ARdif = ARrel[i] - ARrel[j]   
            DECdif = DECrel[i] - DECrel[j]
            #print(ARdif, DECdif)
            theta.append( 1/np.sqrt( ARdif**2 + DECdif**2) )  
            #print("(",i,",", j, ")", end='\t')
            #print(i==j, end='\t')
    
    #Sumamos el resultado
    SumTheta = sum(theta)
    
    #Suma de velocidades al cuadrado
    V2 =[];
    for i in range(N):
        V2.append(Vrel[i]*Vrel[i] )

    SumV2 = sum(V2)
    
    #Estimación
    M = (3*np.pi*D*N/(2*G))*(SumV2/SumTheta)
    #print("\nMASA VIRIAL (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa virial: {:.2E} ".format(M/MS))
    return M/MS



def EstimadorMediana(dirr):
    f = 6.5
    #Sacamos posiciones relativas, número de galaxias y velocidades
    ARrel, DECrel, N, Vrel, D = PosicionesRelativas(dirr)
    
    #Diferencia de ángulos
    thetas = np.zeros((N, N))

    for i in range(N):
        for j in range(i+1, N):
            ARdif = ARrel[i] - ARrel[j]   
            DECdif = DECrel[i] - DECrel[j]
            #print(i, j, ARdif, DECdif)
            thetas[i, j] = np.sqrt( ARdif**2 + DECdif**2  )
            #print(thetas[i, j])
            #print("(",i,",", j, ")", end='\t')
            #print(i==j, end='\t')
        
    #Realizamos la sumatoria
    Suma = []
    Matriz = np.zeros([N, N])

    for i in range(N):
        for j in range(N):
            #print(Suma)
            arg = ( (Vrel[i] - Vrel[j])**2)*thetas[i, j]
            Suma.append( arg)
            Matriz[i, j] = arg
    
    Suma = sum(Suma)

    #Sacamos mediana
    #Convertimos la matriz en un arreglo lineal
    array = Matriz.flatten()
    #Eliminamos los valores nulos y los guardamos en array2
    array2 = []

    for i in range(len(array)):
        if array[i]> 0: array2.append(array[i])

    mediana = np.median(array2)



    #Estimación de masa
    #M = f*Suma*D/G
    #print("\nMASA MEDIANA SUMA (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa: {:.2E}".format(M/MS))

    M = f*mediana*D/G

    #print("\nMASA MEDIANA MEDIANA (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa mediana: {:.2E}".format(M/MS))
    
    return M/MS
    
    

def EstimadorProyectada(dirr):
    #Constantes propias del estimador
    a = 1.5; f = 32/np.pi
    
    #Posiciones relativas, número de galaxias y velocidades
    ARrel, DECrel, N, Vrel, D = PosicionesRelativas(dirr)
    
    #Sumatoria
    theta = []
    for i in range(N):
        theta.append( np.sqrt( ARrel[i]**2 + DECrel[i]**2 )  )
    
    V2 =[]
    for i in range(N):
        V2.append(Vrel[i]*Vrel[i])

    suma = []
    for i in range(N):
        suma.append(V2[i]*theta[i])
    
    Suma = sum(suma)

    #Estimación
    M = (f*Suma*D)/(G*(N-a))
    #print("\nMASA PROYECTADA (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa proyectada: {:.2E}".format(M/MS))
    
    return M/MS

    
def EstimadorPromedio(dirr):
    #Constante propia del estimador
    f = 2.8
    
    #Posiciones relativas, número de galaxias y velocidades
    ARrel, DECrel, N, Vrel, D = PosicionesRelativas(dirr)
    
    #Diferencia de ángulos
    thetas = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            ARdif = ARrel[i] - ARrel[j]   
            DECdif = DECrel[i] - DECrel[j]
            #print(i, j, ARdif, DECdif)
            thetas[i, j] = np.sqrt( ARdif**2 + DECdif**2  )
            #print("(",i,",", j, ")", end='\t')
            #print(i==j, end='\t')
    
    #Realizamos la sumatoria
    Sum = []
    for i in range(N):
        for j in range(i+1, N):
            #print("(",i, j,")",  i<j)
            Sum.append(  ((Vrel[i] - Vrel[j])**2)*thetas[i, j] )
            #print("[V[",i,"] + V[", j,"]]R[", i, ",", j,"]") 
    Suma = sum(Sum)
            
    #Estimación
    M =  (f*2*D*Suma)/(G*N*(N-1))
    #print("\nMASA PROMEDIO (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa promedio: {:.2E}".format(M/MS))

    return M/MS



def Masas(dirr):
    """  MASAS(directorio):
        
        INPUT: directorio con archivo csv del cúmulo de galaxias
        OUTPUT: vector con estimaciones de masas (10^14 M☉)
                [Virial, Mediana, Promedio, Proyectada] 
    
    
    """
    MV  = EstimadorVirial(dirr)
    MM  = EstimadorMediana(dirr)
    MP  = EstimadorPromedio(dirr)
    MPr = EstimadorProyectada(dirr)
    
    masas = np.array([MV, MM, MP, MPr])/(1e14)
    return np.round(masas, 3)



#-----------------------------------------------------------------------------#


def EstimadorVirialBoot(ARrel, DECrel, Vrel, D):
    N = len(ARrel)
    #Diferencia angular entre galaxias
    theta = []

    for i in range(N):
        for j in range(i+1, N):
            ARdif = ARrel[i] - ARrel[j]   
            DECdif = DECrel[i] - DECrel[j]
            #print(ARdif, DECdif)
            theta.append( 1/np.sqrt( ARdif**2 + DECdif**2) )  
            #print("(",i,",", j, ")", end='\t')
            #print(i==j, end='\t')
    
    #Sumamos el resultado
    SumTheta = sum(theta)
    
    #Suma de velocidades al cuadrado
    V2 =[];
    for i in range(N):
        V2.append(Vrel[i]*Vrel[i] )

    SumV2 = sum(V2)
    
    #Estimación
    M = (3*np.pi*D*N/(2*G))*(SumV2/SumTheta)
    #print("\nMASA VIRIAL (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa virial: {:.2E} ".format(M/MS))
    return (M/MS)/1e14



def EstimadorMedianaBoot(ARrel, DECrel, Vrel, D):
    N = len(ARrel)
    f = 6.5
    #Diferencia de ángulos
    thetas = np.zeros((N, N))

    for i in range(N):
        for j in range(i+1, N):
            ARdif = ARrel[i] - ARrel[j]   
            DECdif = DECrel[i] - DECrel[j]
            #print(i, j, ARdif, DECdif)
            thetas[i, j] = np.sqrt( ARdif**2 + DECdif**2  )
            #print(thetas[i, j])
            #print("(",i,",", j, ")", end='\t')
            #print(i==j, end='\t')
        
    #Realizamos la sumatoria
    Suma = []
    Matriz = np.zeros([N, N])

    for i in range(N):
        for j in range(N):
            #print(Suma)
            arg = ( (Vrel[i] - Vrel[j])**2)*thetas[i, j]
            Suma.append( arg)
            Matriz[i, j] = arg
    
    Suma = sum(Suma)

    #Sacamos mediana
    #Convertimos la matriz en un arreglo lineal
    array = Matriz.flatten()
    #Eliminamos los valores nulos y los guardamos en array2
    array2 = []

    for i in range(len(array)):
        if array[i]> 0: array2.append(array[i])

    mediana = np.median(array2)



    #Estimación de masa
    #M = f*Suma*D/G
    #print("\nMASA MEDIANA SUMA (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa: {:.2E}".format(M/MS))

    M = f*mediana*D/G

    #print("\nMASA MEDIANA MEDIANA (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa mediana: {:.2E}".format(M/MS))
    
    return (M/MS)/1e14
    
    

def EstimadorProyectadaBoot(ARrel, DECrel, Vrel, D):
    N = len(ARrel)
    #Constantes propias del estimador
    a = 1.5; f = 32/np.pi 
   
    #Sumatoria
    theta = []
    for i in range(N):
        theta.append( np.sqrt( ARrel[i]**2 + DECrel[i]**2 )  )
    
    V2 =[]
    for i in range(N):
        V2.append(Vrel[i]*Vrel[i])

    suma = []
    for i in range(N):
        suma.append(V2[i]*theta[i])
    
    Suma = sum(suma)

    #Estimación
    M = (f*Suma*D)/(G*(N-a))
    #print("\nMASA PROYECTADA (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa proyectada: {:.2E}".format(M/MS))
    
    return (M/MS)/1e14

    
def EstimadorPromedioBoot(ARrel, DECrel, Vrel, D):
    N = len(ARrel)
    #Constante propia del estimador
    f = 2.8
    
    #Diferencia de ángulos
    thetas = np.zeros((N, N))
    for i in range(N):
        for j in range(i+1, N):
            ARdif = ARrel[i] - ARrel[j]   
            DECdif = DECrel[i] - DECrel[j]
            #print(i, j, ARdif, DECdif)
            thetas[i, j] = np.sqrt( ARdif**2 + DECdif**2  )
            #print("(",i,",", j, ")", end='\t')
            #print(i==j, end='\t')
    
    #Realizamos la sumatoria
    Sum = []
    for i in range(N):
        for j in range(i+1, N):
            #print("(",i, j,")",  i<j)
            Sum.append(  ((Vrel[i] - Vrel[j])**2)*thetas[i, j] )
            #print("[V[",i,"] + V[", j,"]]R[", i, ",", j,"]") 
    Suma = sum(Sum)
            
    #Estimación
    M =  (f*2*D*Suma)/(G*N*(N-1))
    #print("\nMASA PROMEDIO (kg): {:.2E}".format(M))
    #print("En masas solares")
    #print("Masa promedio: {:.2E}".format(M/MS))

    return (M/MS)/1e14


def Masas2(ARrel, DECrel, Vrel, D):
    """  MASAS(directorio):
        
        INPUT: directorio con archivo csv del cúmulo de galaxias
        OUTPUT: vector con estimaciones de masas (10^14 M☉)
                [Virial, Mediana, Promedio, Proyectada] 
    
    
    """
    MV  = EstimadorVirialBoot(ARrel, DECrel, Vrel, D)
    MM  = EstimadorMedianaBoot(ARrel, DECrel, Vrel, D)
    MP  = EstimadorPromedioBoot(ARrel, DECrel, Vrel, D)
    MPr = EstimadorProyectadaBoot(ARrel, DECrel, Vrel, D)
    
    masas = np.array([MV, MM, MP, MPr])
    return np.round(masas, 3)