#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 12:47:58 2025

@author: nbadolo
"""



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyse de l'excès infrarouge et de la fraction de lumière réémise pour une liste d’étoiles.
Basé sur les tables générées par pyssed.py et l'algorithme d'Iain.
"""

import numpy as np
import os
import matplotlib.pyplot as plt
from astropy.table import Table
from scipy.interpolate import interp1d

# Constante
c = 2.998e14  # vitesse de la lumière en µm/s (car λ est en µm)

# === Chemins ===


# === Chemins ===
sub_folder = 'McD_simple'
base_path = "/home/nbadolo/Bureau/Aymard/Tables"
# star_path = f"{base_path}/{sub_folder}/single_csv/"
# EIR_path = f"{base_path}/{sub_folder}/txt_files"
# plot_path = f"{base_path}/{sub_folder}/plots/"
# os.makedirs(plot_path, exist_ok=True)

# sub_folder = 'large_table_stars'
# base_path = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/used_tables'
star_path = f"{base_path}/{sub_folder}/folder_csv/"
EIR_path = f"{base_path}/{sub_folder}/txt_files/"
plot_path = f"{base_path}/{sub_folder}/plots/"
os.makedirs(plot_path, exist_ok=True)

# === Initialisation ===
lst_str = [f for f in os.listdir(star_path) if not f.startswith('.') and not f.endswith('#')]
n_lst_str = len(lst_str)

Excess_vs_LIR_r = np.zeros((n_lst_str, 2))
J_K_arr = np.zeros((n_lst_str, 2))
V_filter_ar = np.zeros((n_lst_str, 2))

# === Fonctions ===

def read_table(filepath):
    try:
        return Table.read(filepath, format="csv", delimiter="\t")
    except Exception as e:
        print(f"Erreur de lecture pour {filepath}: {e}")
        return None

def extract_magnitudes(lambda_lst, magn, Fobsdered):
    J_mag = K_mag = V_mag = V_flux = 0
    for j, lmbd in enumerate(lambda_lst):
        if lmbd in [12350.0, 12480.995, 12210.602, 12100.904]:
            J_mag = magn[j]
        elif lmbd in [21590.0, 21465.009, 21435.460, 21420.344]:
            K_mag = magn[j]
        elif lmbd in [5466.113, 5350.0, 5035.7505]:
            V_mag = magn[j]
            V_flux = Fobsdered[j]
    return J_mag, K_mag, V_mag, V_flux

def plot_star_flux(star_name, lmbd_IR, Fdered_IR, Fmod_IR, E_IR, LIR_vs_L):
    step = 0.05
    if not lmbd_IR:
        return
    interp_obs = interp1d(lmbd_IR, Fdered_IR)
    interp_mod = interp1d(lmbd_IR, Fmod_IR)
    new_lmbd = np.arange(min(lmbd_IR), max(lmbd_IR), step)
    plt.clf()
    plt.figure(figsize=(18.5, 10))
    plt.plot(lmbd_IR, Fdered_IR, '^r', label='flux déréd')
    plt.plot(new_lmbd, interp_obs(new_lmbd), 'r-', label='interp. déréd')
    plt.plot(lmbd_IR, Fmod_IR, 'ob', label='flux modèle')
    plt.plot(new_lmbd, interp_mod(new_lmbd), 'b--', label='interp. modèle')
    plt.xlabel('λ (µm)', size=20)
    plt.ylabel('Flux (Jy)', size=20)
    plt.title(star_name, size=20)
    plt.text(15, max(Fmod_IR)*0.95, f"E_IR = {E_IR:.3f}\nL_IR/L* = {LIR_vs_L:.3f}", fontsize=14)
    plt.xlim(0, 30)
    plt.legend(fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{plot_path}/F_str_{star_name}.png", dpi=100)
    plt.savefig(f"{plot_path}/F_str_{star_name}.pdf", dpi=100)
    plt.close()

# === Traitement principal ===
with open(f"{EIR_path}/{sub_folder}_E_IR_L_LIR.txt", "w") as Excess_IR:
    Excess_IR.write("Star_name, E_IR, L_IR/L*, M_J_K, F_J_K, V_mag, V_flux\n")

    for i, filename in enumerate(lst_str):
        star_name = filename[:-4]
        print(f"Traitement de {star_name} ({i+1}/{n_lst_str})")

        table = read_table(os.path.join(star_path, filename))
        if table is None:
            continue

        lambda_lst = table["wavel"].astype(float)  # en Å
        Fobs = table["flux"].astype(float)
        Fobsdered = table["dered"].astype(float)
        Fmod = table["model"].astype(float)
        magn = table["mag"].astype(float)

        # Extraction magnitudes
        J_mag, K_mag, V_mag, V_flux = extract_magnitudes(lambda_lst, magn, Fobsdered)
        J_minus_K = J_mag - K_mag
        F_J_K = 10**(-J_minus_K/2.5)
        J_K_arr[i] = [J_minus_K, F_J_K]
        V_filter_ar[i] = [V_mag, V_flux]

        # --------------------------------------------------------------------
        # Formule utilisée :
        # L_IR / L_* = ∫ (F_ν_obs - F_ν_model) dν  (de 2.2 μm à ∞)
        #            -----------------------------------------------
        #                  ∫ F_ν_obs dν  (de 0 à ∞)
        #
        # Où :
        # - F_ν_obs : flux observé (déréddé) en fréquence
        # - F_ν_model : flux du modèle (photosphère seule)
        # - ν : fréquence (nu = c / lambda)
        # --------------------------------------------------------------------

        # F_dust = F_obs - F_model pour lambda >= 22000 Å (2.2 µm)
        mask_IR = lambda_lst >= 22000
        lambda_IR = lambda_lst[mask_IR] / 1e4  # conversion en µm
        Fdust_lst = Fobsdered[mask_IR] - Fmod[mask_IR]
        
        # Conversion λ → ν
        nu_IR = c / lambda_IR
        F_dust_nu = Fdust_lst

        # Interpolation et tri pour intégration du numérateur
        sort_idx = np.argsort(nu_IR)
        nu_IR_sorted = nu_IR[sort_idx]
        F_dust_nu_sorted = F_dust_nu[sort_idx]
        interp_dust_nu = interp1d(nu_IR_sorted, F_dust_nu_sorted, kind='linear', fill_value="extrapolate")
        nu_grid_dust = np.linspace(np.min(nu_IR_sorted), np.max(nu_IR_sorted), 1000)
        F_dust_interp = interp_dust_nu(nu_grid_dust)
        F_dust_tot = np.trapz(F_dust_interp, nu_grid_dust)

        # Dénominateur : flux total de l'étoile Fobsdered sur tout le domaine spectral
        lambda_full = lambda_lst / 1e4
        nu_full = c / lambda_full
        Fobs_nu = np.array(Fobsdered)
        sort_idx_full = np.argsort(nu_full)
        nu_full_sorted = nu_full[sort_idx_full]
        Fobs_nu_sorted = Fobs_nu[sort_idx_full]
        interp_obs_nu = interp1d(nu_full_sorted, Fobs_nu_sorted, kind='linear', fill_value="extrapolate")
        nu_grid_obs = np.linspace(np.min(nu_full_sorted), np.max(nu_full_sorted), 2000)
        F_obs_interp = interp_obs_nu(nu_grid_obs)
        F_str_tot = np.trapz(F_obs_interp, nu_grid_obs)

        # Fraction de lumière réémise :
        LIR_vs_L = F_dust_tot / F_str_tot if F_str_tot > 0 else 0

        # Excès infrarouge (simple ratio moyen F_obs/F_mod à λ > 2.2 µm)
        ratio_list = [Fobsdered[j]/Fmod[j] for j in range(len(lambda_lst)) if lambda_lst[j] >= 22000 and Fmod[j] > 0]
        E_IR = np.mean(ratio_list) if ratio_list else 0
        if E_IR > 50:
            E_IR = 0

        Excess_vs_LIR_r[i] = [E_IR, LIR_vs_L]

        # Sauvegarde texte
        Excess_IR.write(f"{star_name}, {E_IR:.4f}, {LIR_vs_L:.4f}, {J_minus_K:.3f}, {F_J_K:.4f}, {V_mag:.2f}, {V_flux:.4f}\n")

        # Graphique
        plot_star_flux(star_name, lambda_IR, Fobsdered[mask_IR], Fmod[mask_IR], E_IR, LIR_vs_L)

        print(f"OK pour {star_name} ({i+1}/{n_lst_str})")

print("Traitement terminé pour toute la liste.")