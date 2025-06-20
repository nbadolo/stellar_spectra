#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 15 16:28:01 2025

@author: nbadolo
"""


from astroquery.vizier import Vizier
import pandas as pd
import time

# -----------------------
# 1. Charger le fichier .list et nettoyer les HIP IDs
# -----------------------

main_path = "/home/nbadolo/Bureau/Aymard/Tables/Query_tables"
input_path = f"{main_path}/input/"
output_path = f"{main_path}/output/"
#file_name = "McD_plus_5"
file_name= "all_hip_simbad"
#%%
with open(input_path +file_name +".list", "r") as f:
    hip_ids = [line.strip().replace("HIP", "").strip() for line in f if line.strip()]

# -----------------------
# 2. Configurer Vizier
# -----------------------

# Aucune limite sur le nombre de lignes retournées
Vizier.ROW_LIMIT = -1

# Laisser columns=None pour récupérer toutes les colonnes (tu pourras filtrer plus tard)
viz = Vizier()
#viz = Vizier(columns=["HIP", "Teff", "Lum", "Fe_H", "IRexcess"]) # Pour specifier des colonnes
# ID du catalogue McDonald+ (2012)
catalog_id = "J/MNRAS/427/343"


# -----------------------
# 3. Interroger le catalogue pour chaque HIP
# -----------------------

results = []
for hip in hip_ids:
    try:
        res = viz.query_constraints(catalog=catalog_id, HIP=hip)
        if res:
            df = res[0].to_pandas()
            results.append(df)
        time.sleep(0.3)  # Petite pause pour ne pas surcharger le serveur
    except Exception as e:
        print(f"Erreur pour HIP {hip}: {e}")

# -----------------------
# 4. Fusionner et sauvegarder
# -----------------------

if results:
    final_df = pd.concat(results, ignore_index=True)
    final_df.to_csv(output_path + file_name +".csv", index=False)
    print(f"✅ Résultats enregistrés dans /{output_path}{file_name}.csv")
else:
    print("❌ Aucun résultat trouvé.")
