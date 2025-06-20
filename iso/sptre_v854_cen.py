#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 17 23:28:19 2025

@author: nbadolo
"""


from astropy.io import fits
import matplotlib.pyplot as plt

main_path = '/home/nbadolo/Bureau/Aymard/Spectres_iso/'
filename = f'{main_path}29701401_pws.fit'
#filename = f'{main_path}29701401_sws.fit'

with fits.open(filename) as hdul:
    hdul.info()
    data = hdul[0].data  # shape (59795, 4)
    print("Shape des données :", data.shape)

    # Supposons les colonnes : 
    # data[:,0] = longueur d'onde (µm)
    # data[:,1] = flux (Jy)
    wavelength = data[:, 0]
    flux = data[:, 1]

plt.figure(figsize=(10, 5))
plt.plot(wavelength, flux, color='darkorange', label='V854 Cen (PWS)')
plt.xlabel("Longueur d'onde (µm)")
plt.ylabel("Flux (Jy)")
plt.title("Spectre infrarouge ISO – V854 Cen")
#plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

