#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 14:28:37 2023

@author: nbadolo
"""


"""
Calcule l'excès infra rouge  d'une étoile (ici 17_Lep ) ainsi que sa fraction de
lumière retraitée dans l'infrarouge en utilisant les mêmes valeurs du flux (en ligne de l'étoile) 
que Iain. Ainsi, je cherche à valider mon code pour le calcul de l'excès infrarouge en comparant les 
valeurs trouvées  à celle de Iain

"""


import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import  lagrange, interp1d
import dask.dataframe as dd



star_name = 'S_Lep'

### opening

##code_test
file_path_r = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/'+ star_name +'_code_test.ods'
df_r = pd.read_excel(file_path_r) # open .sed file converted to .ods
df_r.round(1)
lambda_lst = df_r["wavel"]    #wavelengths
Fobs = df_r["dered"]/1000 # dereded flux (all values)

ratio = df_r["ratio_f_m"] # Ratio of observed (dered) to modelled flux
Fmod = Fobs/ratio  # modelled flux
#Fobs_nu = lambda_lst**2 *Fobs*1e-28/3 #conversion in to frequency flux
#Fmod_nu=  lambda_lst**2 *Fmod*1e-28/3

##17_Lep_code_test2
# file_path_r = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/'+ star_name +'_code_test2.ods'
# df_r = pd.read_excel(file_path_r) # open .sed file converted to .ods
# lambda_lst = df_r["wavel"]    #wavelengths
# Fobs = df_r["obs"]/1000   # observed flux 
# ratio = df_r["ratio_f_mod"] # Ratio of observed (dered) to modelled flux
# Fobsdered = Fobs/ratio  # dereded flux (all values)
# Fmod = Fobsdered/ratio  # modelled flux


# lists for lambda > 2.2 µm  
Fdust22_lst = []   # dust flux
Fr22_lst = [] # flux ratio for excess calculation
lmbd22_interp = []  # the wavelengths to be interpolated(those larger than 2.2µm)
Fmod22_lst = []     # modelled flux to be interpolated
dered22_lst = []   # dereded flux to be interpolated
nu22_interp = []  # frequency corresponding to lmbd22_interp
lmbd22_metr = [] # conversion of wl in to meter units
F22_lst = []

# lists for lambda > 4.3 µm
Fdust43_lst = []   # dust flux
Fr43_lst = [] # flux ratio for excess calculation
lmbd43_interp = []  # the wavelengths to be interpolated(those larger than 4.3µm)
Fobs43_lst = []  #observed flux
Fmod43_lst = []     # modelled flux to be interpolated
dered43_lst = []   # dereded flux to be interpolated
nu43_interp = []  # frequency corresponding to lmbd43_interp
# =============================================================================
#  Calculations for lambda > 2.2 µm
# =============================================================================

# Determining the wavel >= 2.2µm and corresponding fluxes values 
n_lambda_lst = len(lambda_lst) 
for i in range(n_lambda_lst) :
    lmbd22_metr.append(lambda_lst[i]/1e10)
    #F22 = 3e28*Fobs_nu[i]/lambda_lst[i]**2
    #F22_lst.append(F22.round(2))
    if lambda_lst[i] >= 20000: 
        lmbd22_interp.append(lambda_lst[i]/10000) 
        #lmbd22_interp.append(lambda_lst[i]/1e10)
        nu22_interp.append(3e18/lambda_lst[i])
        dered22_lst.append(Fobs[i]) 
        Fmod22_lst.append(Fmod[i])
        Fdust22_lst.append(Fobs[i]-Fmod[i])
        #Fr22_lst.append(Fobs[i]/Fmod[i])
        #Fdust22_lst.append(3e28*(Fobs_nu[i]-Fmod_nu[i])/lambda_lst[i]**2)
       # Fr22_lst.append((lambda_lst[i]**2 *Fobs_nu[i])/(lambda_lst[i]**2 *Fmod_nu[i]))
        Fr22_lst.append(ratio[i])
print(lmbd22_interp)
print(Fr22_lst)
n22_obs = len(lmbd22_interp)  # number of observations at wavelengths >2.2 µm.
print(n22_obs)
#Calculation of infrared excess

E_IR = np.sum(Fr22_lst)/(5)
#print(np.sum(Fr22_lst))
print('The infrared excess of ' +star_name+ ' is E_IR = ' + str(E_IR))

stop
step = 1e-5  # the step for the interpolations

"""
# Calculation of fraction of stellar light reprocessed into the infrared
"""

#interpolation of dust flux
x_d22 = lmbd22_interp
y_d22 = Fdust22_lst
#x_d22 = nu22_interp
#y_d22 = Fdust22_lst
function_interp_d22 = interp1d(x_d22, y_d22)   # interpolation
new_d22 = np.arange(np.min(x_d22), np.max(x_d22), step)

new_point_d22 = function_interp_d22(new_d22)

#Integration of dust flux
area_d22 = np.trapz(new_point_d22)
F_dust_tot22 = area_d22


# Great interpolation of dereded (observed) flux for determination of the total flux of the star


x_g22 = lambda_lst/10000
y_g22=  Fobs 
function_interp_g22 = interp1d(x_g22, y_g22) 
new_g22 = np.arange(np.min(x_g22), np.max(x_g22), step)
new_point_g22 = function_interp_g22(new_g22)

# Great integration of dereded(observed) flux
area_g22 = np.trapz(new_point_g22)
F_str_tot22 = area_g22
F_str_tot22.round(1)
LIR_vs_L = F_dust_tot22/F_str_tot22

print('the fraction of the ' +star_name+' stellar light into the IR is: L_IR/L∗ = '+ str(LIR_vs_L))


# =============================================================================
# Calculations for lambda > 4.3 µm
# =============================================================================

# #Calcul of ℜNIR
# Rnir_lst = []
# for i in range(n_lambda_lst) :
#     if lambda_lst[i] == 7519  or  lambda_lst[i]==7960 or lambda_lst[i] == 12350 or lambda_lst[i] == 16620 or lambda_lst[i] == 21590 or  lambda_lst[i] == 35395 or lambda_lst[i] == 115608 or lambda_lst[i] == 220883 : # wavel of over the near-IR ﬁlters (IJHK s L, iz, and WISE [3.4])
#         Rnir_lst.append(Fobs[i]/Fmod[i])
# print('Rnir_lst = ' + str(Rnir_lst))
# n_Rnir_lst = len(Rnir_lst)
# ℜNIR = sum(Rnir_lst)/n_Rnir_lst
# print('ℜNIR ='  + str(ℜNIR))
# #ℜNIR = 1

# # Determining the wavel >= 4.3 µm and corresponding fluxes values 
# n_lambda_lst = len(lambda_lst) 
# for i in range(n_lambda_lst) :
#     if lambda_lst[i] >= 22000: 
#         lmbd43_interp.append(lambda_lst[i]/10000) 
#         #dered43_lst.append(Fobs[i])
#         Fobs43_lst.append(Fobs[i])
#         Fmod43_lst.append(Fmod[i])
#         Fdust43_lst.append(Fobs[i]-ℜNIR*Fmod[i])
#         Fr43_lst.append(Fobs[i]/(ℜNIR*Fmod[i]))
        
#         #Fr43_lst.append(ratio[i])
# print(lmbd43_interp)
# print(Fr43_lst)
# n43_obs = len(lmbd43_interp)  # number of observations at wavelengths > 4.3 µm.
# print(n43_obs)

# E_IR43 = np.sum(Fr43_lst)/(n22_obs)
# print('E_IR43 = ' + str(E_IR43))

# """
# # Calculation of fraction of stellar light re-emitted into the infrared
# """
# step = 0.05
# #interpolation of dust flux for determination of the total flux of the star
# x_d43 = lmbd43_interp
# y_d43 = Fdust43_lst
# function_interp_d43 = interp1d(x_d43, y_d43)   # interpolation
# new_d43 = np.arange(np.min(x_d43), np.max(x_d43), step)
# new_point_d43 = function_interp_d43(new_d43)

# #Integration of dust flux
# area_d43 = np.trapz(new_point_d43)
# F_dust_tot43 = area_d43


# # Great interpolation of stellar(model) flux for determination of the total flux of the star


# x_g43 = lambda_lst/10000
# y_g43 = ℜNIR*Fmod
# function_interp_g = interp1d(x_g43, y_g43) 
# new_g43 = np.arange(np.min(x_g43), np.max(x_g43), step)
# new_point_g43 = function_interp_g(new_g43)

# # Great integration of stellar (flux flux
# area_g43 = np.trapz(new_point_g43)
# F_str_tot43 = area_g43

# fxs = F_dust_tot43/F_str_tot43

# print('the fraction of the ' +star_name+ ' stellar light re-emitted into the IR is: fxs = ' + str(fxs))


# graphs
plt.figure(star_name)
plt.clf()
#plt.plot(x_obs, (y_obs), 'o')
plt.plot(lambda_lst/10000,(Fobs), '^-')
#plt.plot(x_str, (y_str), 'o')
plt.plot(lambda_lst/10000, (Fmod), 'o-')
plt.xlabel('lambda(µm)', size=14)
plt.ylabel('Flux(Jy)', size=14)
plt.xlim(0, 30)
plt.legend(["Fobs","Fmod"], prop={'size': 16})
plt.title(star_name, size = 20)
plt.savefig('/home/nbadolo/Bureau/test_interpolation/F_str_'+star_name+'.png', 
                dpi=100, bbox_inches ='tight')
plt.savefig('/home/nbadolo/Bureau/test_interpolation/F_str_'+star_name+'.pdf', 
                dpi=100, bbox_inches ='tight')
plt.tight_layout()
plt.show()




