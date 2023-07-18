#!/usr/bin/env python
# coding: utf-8

# # Estimador de masa mediana

# In[30]:


import numpy as np
import pandas as pd


# In[31]:


data = pd.read_table("a2804_final.cat", sep='\s+')
data


# La masa mediana está dada por
# 
# $M_{med} = \dfrac{f_{me}}{G} \sum_{i} \sum_{j} [ (V_{zi}^2 - V_{zj}^2) R_{\perp, ij} ]$

# In[32]:


#Se toman los datos de interés
AR = data.ra_arcsec;    
DEC = data.dec_arcsec;  
V = data.col4
N = len(AR)


# Centroide:
# 
# $r_{av} = \dfrac{1}{N} \sum_{i=1}^{N} r_i$

# In[33]:


cent = [sum(AR)/N, sum(DEC)/N]


# Posiciones relativas al centroide:
# 
# $R_i  = r_i - r_{av}$ 

# In[34]:


#Definimos arreglos, después los llenamos acorde a las posiciones relativas
ARrel  = [ ] 
DECrel = [ ]
for i in range(N):
    ARrel.append(AR[i] - cent[0]);   # ARasrel.append( ARas[i] - centas[0]  )
    DECrel.append(DEC[i] - cent[1]); # DECasrel.append( DECas[i] - centas[1])
    


# Ahora guardamos la diferencia de posiciones relativas
# 
# $R_{\perp, ij} = R_{\perp, i} - R_{\perp, j}$

# In[35]:


Rij = np.zeros((N, N))
for i in range(N):
    for j in range(i+1, N):
        ARdif = ARrel[i] - ARrel[j]   
        DECdif = DECrel[i] - DECrel[j]
        #print(i, j, ARdif, DECdif)
        Rij[i, j] = np.sqrt( ARdif**2 + DECdif**2  )
        #print("(",i,",", j, ")", end='\t')
        #print(i==j, end='\t')

Rij


# In[49]:


Rij[N-2,:]


# In[ ]:




