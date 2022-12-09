#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:51:02 2022

@author: nbadolo
"""


"""
Calcul de l'excès infra rouge des étoiles

"""

import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import  lagrange, interp1d


# importation des tableau de données



file_path_rp = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/radiative_parameters.ods'  # dossier contenant la luminosiité
file_path_pp = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/position_parameters.ods'  # dossier contenant la distance de l'étoile

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