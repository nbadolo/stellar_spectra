#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 18 01:00:02 2025

@author: nbadolo
"""

import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
import os
import csv

# ————— CONFIGURATION GLOBALE DE MATPLOTLIB —————
plt.rcParams.update({
    # "text.usetex": True,  # A décommenter seulement si LaTeX est installé localement
    "font.family": "serif",       # Police style scientifique (Times New Roman ou similaire)
    "axes.labelsize": 16,         # Taille des labels axes
    "axes.titlesize": 15,         # Taille titre
    "xtick.labelsize": 16,        # Taille ticks
    "ytick.labelsize": 16,
    "legend.fontsize": 14
})

# ————— CHEMIN ET FICHIER FITS —————
main_path = '/home/nbadolo/Bureau/Aymard/Spectres_iso/'
output_path = os.path.join(main_path, 'Output')
os.makedirs(output_path, exist_ok=True)
filename = os.path.join(main_path, '29701401_pws.fit')

# ————— OUVERTURE DU FICHIER FITS —————
hdul = fits.open(filename)
print(hdul.info())  # Affiche les extensions et infos du fichier

# Le fichier contient une unique extension DATA dans la HDU0
data = hdul[0].data    # Dimensions: (59795, 4)
hdul.close()

# ————— EXTRACTION DES DONNÉES —————
wavelength = data[:, 0]    # 1ère colonne : longueur d'onde (µm)
flux = data[:, 1]          # 2ème colonne : flux (Jy)
flux_err = data[:, 2]      # 3ème colonne : erreur sur flux (Jy)

# ————— NORMALISATION PAR LE FLUX MAXIMAL —————
flux_max = np.max(flux)
flux_norm = flux / flux_max
flux_err_norm = flux_err / flux_max

# ————— SAUVEGARDE DES DONNÉES BRUTES —————
csv_raw = os.path.join(output_path, 'V854Cen_PWS_spectrum.csv')
with open(csv_raw, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Wavelength (um)', 'Flux (Jy)', 'Flux_Error (Jy)'])
    for wl, flx, err in zip(wavelength, flux, flux_err):
        writer.writerow([wl, flx, err])
print(f"Données brutes sauvegardées dans : {csv_raw}")

# ————— SAUVEGARDE DES DONNÉES NORMALISÉES —————
csv_norm = os.path.join(output_path, 'V854Cen_PWS_spectrum_normalized.csv')
with open(csv_norm, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Wavelength (um)', 'Normalized_Flux', 'Normalized_Flux_Error'])
    for wl, flx, err in zip(wavelength, flux_norm, flux_err_norm):
        writer.writerow([wl, flx, err])
print(f"Données normalisées sauvegardées dans : {csv_norm}")

# ————— TRACER DES SPECTRES —————

# 1) Figure comparaison sans et avec erreurs (flux non normalisé)
fig, axs = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

axs[0].plot(wavelength, flux, color='navy', label='V854 Cen (PWS)')
axs[0].set_xlabel(r'$\lambda$ ($\mu$m)')
axs[0].set_ylabel('Flux (Jy)')
axs[0].legend()
#axs[0].grid(True)

axs[1].errorbar(wavelength, flux, yerr=flux_err, fmt='-', ecolor='gray',
                elinewidth=0.7, capsize=1.5, color='darkorange', label='V854 Cen (PWS)')
axs[1].set_xlabel(r'$\lambda$ ($\mu$m)')
axs[1].legend()
#axs[1].grid(True)

plt.tight_layout()
#output_png_1 = os.path.join(output_path, 'V854Cen_PWS_spectra_comparison.png')
output_png_1 = os.path.join(output_path, 'V854Cen_PWS_spectra_comparison_Eng.png')
plt.savefig(output_png_1, dpi=300)
print(f"Figure comparaison sauvegardée sous : {output_png_1}")
plt.show()

# 2) Figure du spectre normalisé avec barres d'erreur
plt.figure(figsize=(10, 5))
plt.errorbar(wavelength, flux_norm, yerr=flux_err_norm, fmt='-', ecolor='gray',
             elinewidth=0.7, capsize=1.5, color='darkgreen', label='V854 Cen (PWS) Normalized')
plt.xlabel(r'$\lambda$ ($\mu$m)')
#plt.ylabel('Flux normalisé', fontweight='bold')
plt.ylabel('Normalized flux')
#plt.title('Spectre normalisé par le flux maximal', fontweight='bold')
#plt.grid(True)
plt.legend()
plt.tight_layout()

output_png_2 = os.path.join(output_path, 'V854Cen_PWS_spectrum_normalized_Eng.png')
plt.savefig(output_png_2, dpi=300)
print(f"Figure normalisée sauvegardée sous : {output_png_2}")
plt.show()
