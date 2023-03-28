#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:51:02 2022

@author: nbadolo
"""


"""
Calcule l'excès infra rouge  d'une liste d'étoiles ainsi que leur fraction de lumière retraitée dans l'infrarouge'
à partir de l'algorythme de Iain. Les valeurs des flux sont calculées à l'aide du code pyssed.py de Iain.

"""
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import  lagrange, interp1d
from astropy.table import Table 

# importation des tableau de données

# star_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/magn/'
# #star_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/Acsv/'
# star_path2 = '/home/nbadolo/Bureau/Aymard/Donnees_sph/log/'

#sub_folder = 'sample_stars'
sub_folder = 'large_table_stars'
star_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/'+sub_folder+'/folder_csv/'
#star_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/Acsv/'
#star_path2 = '/home/nbadolo/Bureau/Aymard/Donnees_sph/log/'
lst_str = os.listdir(star_path)
print(lst_str)
n_lst_str = len(lst_str)
print(n_lst_str)

## Pour retrouver un indice donné
# ind =''; name = ''; Id = ''
# for i in range(n_lst_str):
#     # print(lst_str[1])
#     # print(lst_str[1][4:10])
    
#     if lst_str[i][4:10]=='113249':
#         ind = i
#         name = lst_str[i]
#         Id = lst_str[i][4:10]
# print(ind)
# print(name)
# print(Id)
# stop
#print(lst_str[48])

Excess_vs_LIR_r = np.zeros((n_lst_str, 2)) # tableau de l'excess E_IR( 1ere val) et de la fraction  LIR_vs_L (2e val)
J_K_arr = np.zeros((n_lst_str, 2)) # tableau pour les valeurs du J-K (magnitude en [0], flux en  [1])
V_filter_ar = np.zeros((n_lst_str, 2)) # tableau pour les valeurs de magnitude en [0] et de fluxen [1]pour le filtre V
# Pour la sauvegarde des paramètres stellaire fichiers .txt
EIR_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/'+ sub_folder +'/txt_files/'
file_name = sub_folder +'_E_IR_L_LIR.txt'
Excess_IR = open("{}/{}".format(EIR_path, file_name), "w")
Excess_IR.write("{}, {}, {}, {}, {}, {}, {}\n".format('Star_name', 'E_IR', 'L_IR/L∗', 'M_J_K', 'F_J_K', 'V_mag', 'V_flux'))

for i in range(n_lst_str):
    # if lst_str[i][4:8]=='113249':
    #     print(i)
    #     print(lst_str[i])
    if lst_str[i][0] != '~' and lst_str[i][-1] !='#' and i != 128:
        print(lst_str[i][-1])
        print(lst_str[i][0])
        
        nb = len(lst_str[i])   # calcule le nombre de caractere du nom du fichier ods
        star_name = lst_str[i][:nb-4] #recuperation du nom de l'étoile 
        
        
        #if i ==1:
        #str_table = star_path + lst_str[i] +'.ods'
        print(star_name +' : ' + str(i + 1)+ '/' + str(n_lst_str))
        str_table = star_path + lst_str[i]
        df_r = Table.read(str_table, format="csv", delimiter="\t")
        #print(df_r.iloc[0:1])
        
        lambda_lst = df_r["wavel"].astype(float)    #wavelengths
        Fobs = df_r["flux"].astype(float)  # observed flux 
        Fobsdered =df_r["dered"].astype(float) # dereded flux (all values)
        Fmod = df_r["model"].astype(float)# modelled flux
        magn = df_r["mag"].astype(float)
        
        
        ratio = Fobsdered/Fmod
        # print(Fobsdered)
        # print(Fmod)
        # print('le ratio =' +str(ratio))
        
        # lists
        Fdust_lst = []   # dust flux
        Fr_lst = [] # flux ratio for excess calculation
        lmbd_interp = []  # the wavelengths to be interpolated(those larger than 2.2µm)
        Fmod_lst = []     # modelled flux to be interpolated
        dered_lst = []   # dereded flux to be interpolated
        
        # Determining the wavel >= 2.2µm and corresponding fluxes values 
        n_lambda_lst = len(lambda_lst) 
        J_mag = 0; K_mag = 0; V_mag = 0; V_flux = 0; E_IR = 0; LIR_vs_L = 0
        for j in range(n_lambda_lst) :
            if lambda_lst[j] >= 22000 : 
                lmbd_interp.append(lambda_lst[j]/10000) 
                dered_lst.append(Fobsdered[j]) 
                Fmod_lst.append(Fmod[j])
                Fdust_lst.append(float(Fobsdered[j])-float(Fmod[j]))
                Fr_lst.append(Fobsdered[j]/Fmod[j])
            
            # recuperation da la magnitude en J
            if lambda_lst[j] == float(12350.0) : # 2MASS J
                J_mag = magn[j]
            elif lambda_lst[j] == float(12480.995) : # Paranal.VISTA J
                J_mag = magn[j]
            elif lambda_lst[j]== float(12210.602) :# DENIS J
                J_mag = magn[j]
            elif lambda_lst[j] == float(12100.904) : #Johnson J
                J_mag = magn[j]
            
            #recuperation d la magnitude en K
            if lambda_lst[j] == float(21590.0) :# 2MASS Ks
                K_mag = magn[j]
            elif lambda_lst[j] == float(21465.009) : # DENIS Ks
                K_mag = magn[j]
            elif lambda_lst[j] == float(21435.460) :# Paranal.VISTA K
                K_mag = magn[j]
            elif lambda_lst[j] == float(21420.344): # Johnson K
                K_mag = magn[j]
            
            
            # recuperation de la magnitude et du flux en V
            if lambda_lst[j] == float(5466.113): # Johnson V
                V_mag = magn[j]
                V_flux = Fobsdered[j]
            elif lambda_lst[j] == float(5350.0): # TYCHO V
                V_mag = magn[j]
                V_flux = Fobsdered[j]
            elif lambda_lst[j] == float(5035.7505): # Gaia Gbp
                V_mag = magn[j]
                V_flux = Fobsdered[j]
            
            V_filter_ar[i][0] = V_mag
            V_filter_ar[i][1] = V_flux
            
            J_minus_K = J_mag - K_mag # calcul du J-K
            J_K_arr[i][0] = J_minus_K
            F_J_K = 10**(-J_minus_K/2.5) # flux correspondant au J-K
            J_K_arr[i][1] = F_J_K
        
        n_obs = len(lmbd_interp)  # number of observations at wavelengths >2.2 µm.
        
    
        
        #Calculation of infrared excess
    
        moy_ratio = np.sum(Fr_lst)/(n_obs)
        if moy_ratio <= 50 :
            E_IR = moy_ratio
        
        print('la magn en V est : ' + str(V_filter_ar[i][0]))
        print('le flux en V est : ' + str(V_filter_ar[i][1]))
        
        
        
        print('The infrared excess of ' + star_name + ' is E_IR = ' + str(E_IR))
        
        
        step = 0.05  # the step for interpolation
    
        """
        # Calculation of fraction of stellar light reprocessed into the infrared
        """
    
        #interpolation of dust flux
        x_d = (lmbd_interp)
        y_d = (Fdust_lst)
        # if not lmbd_interp:
        #     x_d = [2.2, 2.3]
        #     y_d = [1,1.1]
        #Excess_vs_LIR_r[i] = 0
        if lmbd_interp : #pour les étoiles qui ont  des  lambda >  2.2 µm
            
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
        
            print('The fraction of the ' + star_name +' stellar light into the IR is: L_IR/L∗ = '+ str(LIR_vs_L))
         
        # else : # pour les étoiles qui n'ont pas de lambda >  2.2 µm, on donne la valeur 0 à L_IR/L*
           
        #     Excess_vs_LIR_r[i][1] = 0 
        #     print(' 0 has been assigned to the value of the ' + star_name +'L_IR/L')
              
            # Enregistrement des parametres dans un fichier txt
        
        Excess_IR.write("{}, {}, {}, {}, {}, {}, {}\n".format(star_name, Excess_vs_LIR_r[i][0], Excess_vs_LIR_r[i][1],
                 J_K_arr[i][0], J_K_arr[i][1], V_filter_ar[i][0], V_filter_ar[i][1]))
        
    
        """
        # Other interpolations for the plots
        """
        
        # Interpolation of derered flux
        if lmbd_interp :
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
            plt.savefig('/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/'+sub_folder+'/plots/F_str_'+star_name+'.png', 
                            dpi=100, bbox_inches ='tight')
            plt.savefig('/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/'+sub_folder+'/plots/F_str_'+star_name+'.pdf', 
                            dpi=100, bbox_inches ='tight')
            plt.tight_layout()
            plt.show()
        print('process okay for : ' +star_name +' : ' + str(i + 1) + '/' + str(n_lst_str))
print('process okay for all the list ')
    
    
