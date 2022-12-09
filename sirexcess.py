#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:22:51 2022

@author: nbadolo
"""

"""
Calcul de l'excès infra rouge d'une étoiles

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


star_name = 'SW_Col'
file_path_r = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/magn/'+star_name+'.ods'

df_r = pd.read_excel(file_path_r) # ouverture du tableau en question

Fobs = df_r["flux"]   # colone du flux observé
Fobsdered = df_r["dered"] # colone du flux observé derougi
Fmod = df_r["model"] # colone du flux modelisé

Fd_lst = []     #flux de la poussière selon Iain
Fdust_lst = []   #flux de la poussière selon Eric
lmbd_interp = []
Fmod_lst = []
lmbd_interp1 =[]
dered_lst = []
lambda_lst = df_r["wavel"]    #liste des longueurs d'ondes
n_lambda_lst = len(lambda_lst) #taille de cette liste
#%% 
for i in range(n_lambda_lst) :
    if lambda_lst[i] >= 22000 and lambda_lst[i] <= 800000: # etape 3
        lmbd_interp1.append(lambda_lst[i]/10000) # recupère toutes les longueurs d'onnde >=2.2 µm, celles pour lesquelle le flusx sera interpolé
        dered_lst.append(Fobsdered[i]) #recupère le flux observés pour lesquels lambda >= 2.2µm
        Fmod_lst.append(Fmod[i])       # recupère le flux modelisés pour lesquels lambda >= 2.2µm
        #Fdust = Fobsdered[i] -Fmod[i] #calcul du flux de la poussière 
        #Fdust_lst.append(Fdust)       # constitue la liste du flux de la poussière


#Interpolation du flux obsevé derougi
x_obs = (lmbd_interp1)
y_obs = (dered_lst)
function_interp_obs = interp1d(x_obs, y_obs)
new_xobs = np.arange(np.min(x_obs), np.max(x_obs))
new_point_obs = function_interp_obs(new_xobs)

#Integration du flux observé dérougi
area_obs = np.trapz(new_point_obs)
F_obs_tot = area_obs


#Interpolation du flux stellaire (flux modelisé)
x_str = (lmbd_interp1)
y_str = ((Fmod_lst))
function_interp_str = interp1d(x_str, y_str)
new_xstr = np.arange(np.min(x_str), np.max(x_str), 1.5)
new_point_str = function_interp_str(new_xstr)

Remarque bizarre : plus jaugmente léchantillonage, plus E_IR baisse. 

#integration du flux stellaire
area_str = np.trapz(new_point_str)
F_str_tot = area_str

#calcul de l'excès IR(rapport du flux total observé derougi par le flux total stellaire(model))
E_IR  =  F_obs_tot/F_str_tot
print('Lexcès infra rouge de ' +star_name+ ' est E_IR = ' + str(E_IR))


# graphes
plt.figure(11)
plt.clf()
plt.plot(x_str, np.log10(y_str), 'o')
plt.plot(new_xstr, np.log10(new_point_str), '-x')
plt.xlabel('lambda(µm)', size=20)
plt.ylabel('Flux(Jy)', size=20)
plt.title('flux stellaire interpolé de  ' +star_name, size = 20)
plt.savefig('/home/nbadolo/Bureau/test_interpolation/F_str_'+star_name+'.png', 
                dpi=100, bbox_inches ='tight')
plt.tight_layout()
plt.show()

