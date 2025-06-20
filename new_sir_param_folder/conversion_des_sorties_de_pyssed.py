#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 15:59:32 2025

@author: nbadolo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 15:30:43 2025

@author: nbadolo
"""

import pandas as pd
import os

# Chemin du dossier où se trouvent les fichiers .sed
main_path = "/home/nbadolo/CODES_SIM/PySSED/v0.2/output/McD_simple/"

sed_folder = os.path.join(main_path, "sed_test")
dat_folder = os.path.join(main_path, "dat")
# Chemin du dossier de sortie où enregistrer les fichiers .csv convertis
output_folder_single = os.path.join(main_path, "single_csv")
output_folder_all = os.path.join(main_path, "all_csv")

# Assure-toi que les dossiers de sortie existent
os.makedirs(output_folder_single, exist_ok=True)
os.makedirs(output_folder_all, exist_ok=True)

# Liste des fichiers .dat dans le dossier
dat_files = [f for f in os.listdir(dat_folder) if f.endswith(".dat")]

# Fonction pour convertir un fichier .dat en .csv

def convert_dat_to_csv(dat_file_path):
    try:
        with open(dat_file_path, 'r') as f:
            lines = f.readlines()

        # Lire et nettoyer l'en-tête
        header = lines[0].strip().split()
        header = header[:8]
        col_names = ['hip_id'] + header[2:8]  # On remplace les 2 premiers noms par 'hip_id'

        new_rows = []

        for line in lines[1:]:
            parts = line.strip().split()

            # Vérifie qu'il y a au moins 8 éléments (2 pour HIP + 6 autres)
            if len(parts) >= 8:
                hip_id = f"{parts[0]} {parts[1]}"
                row = [hip_id] + parts[2:8]  # 1 + 6 = 7 colonnes
                new_rows.append(row)

        # Crée le DataFrame seulement avec les lignes valides
        df = pd.DataFrame(new_rows, columns=col_names)

        # Export CSV
        out_file = os.path.join(output_folder_all, os.path.basename(dat_file_path).replace(".dat", ".csv"))
        df.to_csv(out_file, index=False)
        print(f"✅ {os.path.basename(dat_file_path)} bien converti avec ID HIP dans une seule cellule.")

    except Exception as e:
        print(f"❌ Erreur pour {dat_file_path} : {e}")
        
        
# def convert_dat_to_csv(dat_file):
#     try:
#         # Lecture sans en-tête, on traite tout comme données
#         data = pd.read_csv(dat_file, header=None, delim_whitespace=True, engine='python', on_bad_lines='skip')
        
#         # Sélectionne au max les 8 premières colonnes si disponibles
#         max_cols = min(data.shape[1], 8)
#         data = data.iloc[:, :max_cols]
        
#         # Sauvegarde
#         csv_filepath = os.path.join(output_folder_all, os.path.basename(dat_file).replace(".dat", ".csv"))
#         data.to_csv(csv_filepath, index=False, header=False)
#         print(f"Fichier {dat_file} converti en {csv_filepath} avec {max_cols} colonnes.")
#     except Exception as e:
#         print(f"Erreur lors de la conversion du fichier {dat_file}: {e}")

# Conversion des fichiers .dat
for dat_file in dat_files:
    dat_file_path = os.path.join(dat_folder, dat_file)  # Chemin complet du fichier .dat
    convert_dat_to_csv(dat_file_path)

# # Fonction pour convertir un fichier .sed en .csv
# def convert_sed_to_csv(sed_file):
#     try:
#         # Lire le fichier .sed en ignorant les lignes mal formées avec on_bad_lines
#         data = pd.read_csv(sed_file, header=None, delim_whitespace=True, on_bad_lines='skip')
#         # Sauvegarder en .csv
#         csv_filepath = os.path.join(output_folder_single, os.path.basename(sed_file).replace(".sed", ".csv"))
#         data.to_csv(csv_filepath, index=False, header=False)
#         print(f"Fichier {sed_file} converti en {csv_filepath}")
#     except Exception as e:
#         print(f"Erreur lors de la conversion du fichier {sed_file}: {e}")




                
           
# # Créer le répertoire de sortie s'il n'existe pas
# if not os.path.exists(output_folder_single):
#     os.makedirs(output_folder_single)

# def convert_sed_to_csv(sed_file, expected_columns=20):
#     try:
#         # Lecture en supposant un fichier tabulé
#         data = pd.read_csv(sed_file, header=None, sep='\t', engine='python')
        
#         # Vérification du nombre de colonnes
#         if data.shape[1] != expected_columns:
#             print(f"Avertissement : {sed_file} contient {data.shape[1]} colonnes au lieu de {expected_columns}. Les lignes problématiques seront ignorées.")
#             # Limiter le nombre de colonnes à `expected_columns` si nécessaire
#             data = data.iloc[:, :expected_columns]
        
#         # Générer le nom du fichier .csv
#         csv_filepath = os.path.join(output_folder_single, os.path.basename(sed_file).replace(".sed", ".csv"))
        
#         # Sauvegarde sans les index ni les en-têtes
#         data.to_csv(csv_filepath, index=False, header=False)
#         print(f"Fichier {sed_file} converti en {csv_filepath}")
    
#     except Exception as e:
#         print(f"Erreur lors de la conversion du fichier {sed_file} : {e}")




# # Fonction pour convertir une valeur et remplacer les virgules par des points
# def convert_comma_to_dot(val):
#     try:
#         # Remplacer les virgules par des points et convertir en float
#         return float(str(val).replace(',', '.'))
#     except ValueError:
#         return val  # Si la conversion échoue, on retourne la valeur d'origine

# # Vérifier et créer le dossier de sortie s'il n'existe pas
# if not os.path.exists(output_folder_single):
#     os.makedirs(output_folder_single)

# # Fonction de conversion du fichier .sed en .csv
# def convert_sed_to_csv(sed_file, expected_columns=20):
#     try:
#         # Lecture du fichier avec tabulation comme séparateur
#         data = pd.read_csv(sed_file, header=None, sep='\t', engine='python')
        
#         # Vérification du nombre de colonnes
#         if data.shape[1] != expected_columns:
#             print(f"Avertissement : {sed_file} contient {data.shape[1]} colonnes au lieu de {expected_columns}. Les lignes problématiques seront ignorées.")
#             # Limiter le nombre de colonnes à `expected_columns` si nécessaire
#             data = data.iloc[:, :expected_columns]
        
#         # Appliquer la conversion des virgules en points dans toutes les cellules du dataframe
#         data = data.applymap(convert_comma_to_dot)

#         # Supprimer les lignes contenant des valeurs NaN
#         data_cleaned = data.dropna()

#         # Générer le nom du fichier de sortie (.csv)
#         csv_filepath = os.path.join(output_folder_single, os.path.basename(sed_file).replace(".sed", ".csv"))
        
#         # Sauvegarder le fichier CSV sans les index et les en-têtes
#         data_cleaned.to_csv(csv_filepath, index=False, header=False)
#         print(f"Fichier {sed_file} converti en {csv_filepath}")
    
#     except Exception as e:
#         print(f"Erreur lors de la conversion du fichier {sed_file} : {e}")












# Vérification des lignes dans le fichier .sed avant de le convertir
def check_sed_file(sed_file):
    with open(sed_file, 'r') as file:
        for i, line in enumerate(file):
            if len(line.split()) != 19:  # Compare le nombre de colonnes avec le nombre attendu
                print(f"Ligne {i+1} a un nombre incorrect de colonnes : {line.strip()}")
                
 
#%%
# # Boucle pour convertir tous les fichiers .sed dans le dossier
# for sed_file in os.listdir(sed_folder):
#     if sed_file.endswith(".sed"):  # Vérifie que ce soit un fichier .sed
#         sed_file_path = os.path.join(sed_folder, sed_file)  # Construit le chemin complet
#         check_sed_file(sed_file_path)  # Vérifie les erreurs avant de convertir
#         convert_sed_to_csv(sed_file_path)  # Convertit le fichier après la vérification
      