#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 18 00:42:12 2025

@author: nbadolo
"""

import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
import os

# ————— CONFIGURATION GLOBALE DE MATPLOTLIB —————
plt.rcParams.update({
    # "text.usetex": True,  # Décommente seulement si LaTeX est installé localement
    "font.family": "serif",       # Police style scientifique (Times New Roman ou similaire)
    "axes.labelsize": 16,         # Taille des labels axes
    "axes.titlesize": 15,         # Taille titre
    "xtick.labelsize": 16,        # Taille ticks
    "ytick.labelsize": 16,
    "legend.fontsize": 14
})

# ————— CHEMIN ET FICHIER FITS —————
main_path = '/home/nbadolo/Bureau/Aymard/Spectres_iso/'
output_path = f'{main_path}/Output/'
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

# ————— TRACER DES SPECTRES —————

fig, axs = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

# Spectre sans erreur
axs[0].plot(wavelength, flux, color='navy', label='V854 Cen (PWS)')
axs[0].set_xlabel(r'$\lambda$ ($\mu$m)', fontweight='bold')
axs[0].set_ylabel('Flux (Jy)', fontweight='bold')
#axs[0].set_title('Spectre sans barres d\'erreur', fontweight='bold')
#axs[0].grid(True)
axs[0].legend()

# Spectre avec barres d'erreur
axs[1].errorbar(wavelength, flux, yerr=flux_err, fmt='-', ecolor='gray',
                elinewidth=0.7, capsize=1.5, color='darkorange', label='V854 Cen (PWS)')
axs[1].set_xlabel(r'$\lambda$ ($\mu$m)', fontweight='bold')
#axs[1].set_title('Spectre avec barres d\'erreur', fontweight='bold')
#axs[1].grid(True)
axs[1].legend()

# Ajustement layout et sauvegarde
plt.tight_layout()
output_png = os.path.join(output_path, 'V854Cen_PWS_spectra_comparison.png')
plt.savefig(output_png, dpi=300)
print(f"Figure sauvegardée sous : {output_png}")

plt.show()
