#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 16:58:35 2022

@author: nbadolo
"""



"""
Essaie de recuperation des paramètres dans des fichiers ods

"""


import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import  lagrange, interp1d


# importation des tableau de données
# 
# 


file_path_rp = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/radiative_parameters.ods'  # dossier contenant les données à extraire
file_path_pp = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/position_parameters.ods'



# Pour la recuperation de la luminosité de l'étoile 
df_rp = pd.read_excel(file_path_rp) # ouverture du tableau en question
df_rp_name = df_rp["#Object"]  # lecture de la colonne des noms des objets
df_rp_lum = df_rp["Luminosity"] # lecture de la colonne des  luminosités


n_targ = len(df_rp_name) # taille de la colonne des noms
df_r = pd.read_excel(file_path_r)
for i in range(n_targ):
    if df_rp_name[i] == star_name:
        Lstr = df_rp_lum[i]   # recuperation de la luminosité de l'objet
        print(Lstr)



# Pour la recuperation de la distance de l'étoile 
df_pp = pd.read_excel(file_path_pp)
df_pp_name = df_pp["#Object"]  # lecture de la colonne des noms des objets
df_pp_dist = df_pp["Distance"] # lecture de la colonne des  distances

n_obj = len(df_pp_name)
for i in range(n_obj):
    if df_pp_name[i]== star_name:
        dstr = df_pp_dist[i]
        print(dstr)
        
        
print(n_lambda_lst)
Fobs = df_r["flux"]   # colone du flux observé
Fobsdered = df_r["dered"] # colone du flux observé derougi
Fmod = df_r["model"] # colone du flux modelisé

for i in range(n_lambda_lst) :
    if lambda_lst[i] >= 22000: # etape 3
        lmbd_interp.append(lambda_lst[i]/10000) # recupère toute longueur d'onnde 2.2 micron
        ratio = Fmod[i]/Fobs[i] # etape 1
        Fstr = Fobs[i]/ratio    
        Fd = Fobs[i] -Fstr   # flux de poussière pour chaque longueur d'onde (etape 2)
        #Fd_lst[i] = Fd 
        Fd_lst.append(Fd)  # constitution de la liste des valeurs du fux de la poussière
        print(Fd)

# pour l'interpolation
x = (lmbd_interp)
y = (Fd_lst)
function_interp = interp1d(x, y)
new_x = np.arange(np.min(x), np.max(x))
new_point = function_interp(new_x)

# area = np.trapz(new_point)   # Integration du flux interpolé
# print(area)
#print(new_point)


for i in range(n_lambda_lst) :
    if lambda_lst[i] >= 22000: # etape 3
        lmbd_interp1.append(lambda_lst[i]/10000) # recupère toutes les longueurs d'onnde >=2.2 µm, celles pour lesquelle le flusx sera interpolé
        dered_lst.append(Fobsdered[i]) #recupère les flux observés pour lesquels lambda >= 2.2µm
        Fmod_lst.append(Fmod[i])       # recupère les flux modelisés pour lesquels lambda >= 2.2µm
        Fdust = Fobsdered[i] -Fmod[i] #calcul du flux de la poussière 
        Fdust_lst.append(Fdust)       # constitue la liste du flux de la poussière

#Interpolation du flux de la poussière

xp = (lmbd_interp1)
yp = ((Fdust_lst))
function_interp1 = interp1d(xp, yp)
new_xp = np.arange(np.min(xp), np.max(xp))
new_pointp = function_interp1(new_xp)

#Itegration de la poussière
area_p = np.trapz(new_pointp)  # flux de poussière totale integrée
Ldust = area_p*4*np.pi*dstr**2



"""
# Calculation of the excess using 
"""

# Interpolation of derered flux
x_obs = (lmbd_interp)
y_obs = (dered_lst)
function_interp_obs = interp1d(x_obs, y_obs)   # interpolation
new_xobs = np.arange(np.min(x_obs), np.max(x_obs), step)
new_point_obs = function_interp_obs(new_xobs)

#Integration of dereded flux 
area_obs = np.trapz(new_point_obs)
F_obs_tot = area_obs

#Interpolation of stellar flux (modelled flux)
x_str = (lmbd_interp)
y_str = ((Fmod_lst))
function_interp_str = interp1d(x_str, y_str) # interpolation
new_xstr = np.arange(np.min(x_str), np.max(x_str), step) # bizare
new_point_str = function_interp_str(new_xstr)

 

#integration of stellar flux
area_str = np.trapz(new_point_str)
F_str_tot = area_str

# calculation of the infrared excess ( ratio of total observed flux to total stellar flux(model))
LIR_vs_L  =  F_obs_tot/F_str_tot
#print('The infrared excess of ' +star_name+ ' is E_IR = ' + str(E_IR))


plt.figure(10)
plt.clf()
plt.plot(x, y, 'o')
plt.plot(new_x, new_point, '-x')
plt.xlabel('lambda(µm)', size=20)
plt.ylabel('Flux(W/m^2)', size=20)
plt.title('flux de la poussière de '+star_name, size = 20)
plt.savefig('/home/nbadolo/Bureau/test_interpolation/Fdust_'+star_name+'.png', 
                dpi=100, bbox_inches ='tight')
plt.tight_layout()
plt.show()


# Pour la recuperation de la luminosité de l'étoile 
df_rp = pd.read_excel(file_path_rp) # ouverture du tableau en question
df_rp_name = df_rp["#Object"]  # lecture de la colonne des noms des objets
df_rp_lum = df_rp["Luminosity"] # lecture de la colonne des  luminosités
n_targ = len(df_rp_name) # taille de la colonne des noms
print(n_targ)

# Pour la recuperation de la distance de l'étoile 
df_pp = pd.read_excel(file_path_pp)
df_pp_name = df_pp["#Object"]  # lecture de la colonne des noms des objets
df_pp_dist = df_pp["Distance"] # lecture de la colonne des  distances

def CalcExcess(star_name) :
    file_path_r = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/magn/'+star_name+'.ods'