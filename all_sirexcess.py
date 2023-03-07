#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:51:02 2022

@author: nbadolo
"""


"""
Calcule l'excès infra rouge  d'une liste d'étoiles ainsi que leur fraction de lumière retraitée dans l'infrarouge'


"""

import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import  lagrange, interp1d


# importation des tableau de données

star_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/magn/'
#star_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/Acsv/'
star_path2 = '/home/nbadolo/Bureau/Aymard/Donnees_sph/log/'
lst_str = os.listdir(star_path2)
print(lst_str)
n_lst_str = len(lst_str)

Excess_vs_LIR_r = np.zeros((n_lst_str, 2)) # tableau de l'excess E_IR( 1ere val) et de la fraction  LIR_vs_L (2e val)

#Pour la sauvegarde des paramètres stellaire fichiers .txt
EIR_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/txt_files/'
file_name = 'E_IR_L_LIR.txt'
Excess_IR = open("{}/{}".format(EIR_path, file_name), "w")
Excess_IR.write("{}, {}, {}\n".format('Star_name', 'E_IR', 'L_IR/L∗'))

for i in range(n_lst_str):
    #nb = len(lst_str[i])   # calcule le nombre de caractere du nom du fichier ods
    #star_name = lst_str[i][:nb-4] #recuperation du nom de l'étoile 
    star_name = lst_str[i]
    print(star_name)
    if i != 3 and i != 13 :
        str_table = star_path + lst_str[i] +'.ods'
        df_r = pd.read_excel(str_table) # open .sed file converted to .ods
        lambda_lst = df_r['wavel']    #wavelengths
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
        for j in range(n_lambda_lst) :
            if lambda_lst[j] >= 22000 : 
                lmbd_interp.append(lambda_lst[j]/10000) 
                dered_lst.append(Fobsdered[j]) 
                Fmod_lst.append(Fmod[j])
                Fdust_lst.append(Fobsdered[j]-Fmod[j])
                Fr_lst.append(Fobsdered[j]/Fmod[j])
    
        n_obs = len(lmbd_interp)  # number of observations at wavelengths >2.2 µm.
    
        #Calculation of infrared excess
    
        E_IR = np.sum(Fr_lst)/(n_obs)
    
        print('The infrared excess of ' +star_name+ ' is E_IR = ' + str(E_IR))
    
        step = 0.05  # the step for interpolation
    
        """
        # Calculation of fraction of stellar light reprocessed into the infrared
        """
    
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
        Excess_vs_LIR_r[i] = E_IR, LIR_vs_L  # tableau de l'excess E_IR et de la fraction  LIR_vs_L 
    
        print('The fraction of the ' +star_name+' stellar light into the IR is: L_IR/L∗ = '+ str(LIR_vs_L))
        
        # Enregistrement des parametres dans un fichier txt
        
        # EIR_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/magn/'
        # file_name = 'E_IR_L_LIR.txt'
        # Excess_IR = open("{}/{}".format(EIR_path, file_name), "w")
        Excess_IR.write("{}, {}, {}\n".format(lst_str[i], E_IR, LIR_vs_L))
    
        """
        # Other interpolations for the plots
        """
        
        # Interpolation of derered flux
        x_obs = (lmbd_interp)
        y_obs = (dered_lst)
        function_interp_obs = interp1d(x_obs, y_obs)   # interpolation
        new_xobs = np.arange(np.min(x_obs), np.max(x_obs), step)
        new_point_obs = function_interp_obs(new_xobs)


        #Interpolation of stellar flux (modelled flux)
        x_str = (lmbd_interp)
        y_str = ((Fmod_lst))
        function_interp_str = interp1d(x_str, y_str) # interpolation
        new_xstr = np.arange(np.min(x_str), np.max(x_str), step) # bizare
        new_point_str = function_interp_str(new_xstr)

    
        #graphes
        plt.clf()
        fig=plt.figure(star_name)
        fig.set_size_inches(18.5, 10, forward = True)
        plt.plot(x_obs,(y_obs), '^r')
        plt.plot(new_xobs, (new_point_obs), 'r-x')
        plt.plot(x_str, (y_str), 'ob')
        plt.plot(new_xstr, (new_point_str), 'b-x')
        plt.xlabel('lambda(µm)', size=20)
        plt.ylabel('Flux(Jy)', size=20)
        plt.text(15, 0.95*np.max(y_str), 'E_IR = ' + f'{Excess_vs_LIR_r[i][0]}', color='k', fontsize='large', ha='center')
        plt.text(15, 0.95*np.max(y_str)-70, 'L_IR/L* = ' + f'{Excess_vs_LIR_r[i][1]}', color='k', fontsize='large', ha='center')
        plt.xlim(0, 30)
        plt.legend(["dereded flux","interpolated dereded fux","stellar fux","interpolated stellar fux"], prop={'size': 20})
        plt.title(star_name, size = 20)
        plt.savefig('/home/nbadolo/Bureau/test_interpolation/F_str_'+star_name+'.png', 
                        dpi=100, bbox_inches ='tight')
        plt.savefig('/home/nbadolo/Bureau/test_interpolation/F_str_'+star_name+'.pdf', 
                        dpi=100, bbox_inches ='tight')
        plt.tight_layout()
        plt.show()
        
