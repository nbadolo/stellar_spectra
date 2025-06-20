#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:22:51 2022

@author: nbadolo
"""

"""
Calcule l'excès infra rouge  d'une étoile ainsi que sa fraction de lumière retraitée dans l'infrarouge'

"""


import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import  lagrange, interp1d




star_name = '17_Lep'

#opening
file_path_r = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/magn/'+star_name+'.ods'
df_r = pd.read_excel(file_path_r) # open .sed file converted to .ods
lambda_lst = df_r["wavel"]    #wavelengths
Fobs = df_r["flux"]   # observed flux 
Fobsdered = df_r["dered"] # dereded flux (all values)
Fmod = df_r["model"] # modelled flux

# lists
Fdust_lst = []   # dust flux
Fr_lst = [] # flux ratio for excess calculation
lmbd_interp = []  # the wavelengths to be interpolated(those larger than 2.2µm)
Fmod_lst = []     # modelled flux to be interpolated
dered_lst = []   # dereded flux to be interpolated

# Determining the wavel >= 2.2µm and corresponding fluxes values 
n_lambda_lst = len(lambda_lst) 
for i in range(n_lambda_lst) :
    if lambda_lst[i] >= 22000 : 
        lmbd_interp.append(lambda_lst[i]/10000) 
        dered_lst.append(Fobsdered[i]) 
        Fmod_lst.append(Fmod[i])
        Fdust_lst.append(Fobsdered[i]-Fmod[i])
        Fr_lst.append(Fobsdered[i]/Fmod[i])

n_obs = len(lmbd_interp)  # number of observations at wavelengths >2.2 µm.
print(n_obs)

#Calculation of infrared excess
E_IR = np.sum(Fr_lst)/(n_obs)

print('The infrared excess of ' +star_name+ ' is E_IR = ' + str(E_IR))

step = 0.05  # the step for interpolation




# =============================================================================
# Calculation of fraction of stellar light reprocessed into the infrared
# =============================================================================



#interpolation of dust flux
x_d = (lmbd_interp)
y_d = (Fdust_lst)
function_interp_d = interp1d(x_d, y_d)   # interpolation
new_d = np.arange(np.min(x_d), np.max(x_d), step)
new_point_d = function_interp_d(new_d)

#Integration of dust flux
area_d = np.trapz(new_point_d)
F_dust_tot = area_d


# Great interpolation of dereded (observed) flux for determination of the total flux of the star

x_g = lambda_lst/10000
y_g = Fobsdered
function_interp_g = interp1d(x_g, y_g) 
new_g = np.arange(np.min(x_g), np.max(x_g), step)
new_point_g = function_interp_g(new_g)

# Great integration of dereded(observed) flux
area_g = np.trapz(new_point_g)
F_str_tot = area_g

LIR_vs_L  =  F_dust_tot/F_str_tot 

print('the fraction of the ' +star_name+' stellar light into the IR is: L_IR/L∗ = '+ str(LIR_vs_L))



# graphs
plt.figure(star_name)
plt.clf()
#plt.plot(x_obs, (y_obs), 'o')
plt.plot(lambda_lst/10000,(Fobsdered), '^')
#plt.plot(x_str, (y_str), 'o')
plt.plot(lambda_lst/10000, (Fmod), 'o')
plt.xlabel('lambda(µm)', size=20)
plt.ylabel('Flux(Jy)', size=20)
plt.xlim(0, 30)
plt.legend(["dereded flux","stellar fux"], prop={'size': 20})
plt.title(star_name, size = 20)
plt.savefig('/home/nbadolo/Bureau/test_interpolation/F_str_'+star_name+'.png', 
                dpi=100, bbox_inches ='tight')
plt.savefig('/home/nbadolo/Bureau/test_interpolation/F_str_'+star_name+'.pdf', 
                dpi=100, bbox_inches ='tight')
plt.tight_layout()
plt.show()




