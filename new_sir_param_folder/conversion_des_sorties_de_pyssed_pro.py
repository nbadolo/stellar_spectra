#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 17:46:05 2025

@author: nbadolo
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 15:59:32 2025

@author: nbadolo
"""

import pandas as pd
import os
import os
import jpype
import shutil
import glob



# Chemin du dossier où se trouvent les fichiers .sed
main_path = "/home/nbadolo/CODES_SIM/PySSED/v0.2/output/McD_simple/"

path_sed1 =main_path + "sed/"
path_sed2 = main_path + "Intermediate_sed/"
path_txt = main_path + "folder_txt/"
path_csv = main_path + "folder_csv/"

sed_folder = os.path.join(main_path, "sed")
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

        # Teste si la 2ᵉ ligne commence par "HIP " pour déterminer le format du fichier
        second_line = lines[1].strip() if len(lines) > 1 else ''
        starts_with_hip = second_line.startswith("HIP ")

        if starts_with_hip:
            # Cas anc.dat : en-tête = 1 ligne
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

        else:
            # Cas hrd.dat : en-tête = 2 lignes fusionnées
            header1 = lines[0].strip().split()
            header2 = lines[1].strip().split()
            max_len = max(len(header1), len(header2))
            while len(header1) < max_len:  # Complète les listes pour qu'elles aient la même longueur
                header1.append("")
            while len(header2) < max_len:
                header2.append("")

            col_names = [(a + "_" + b).strip("_") if a or b else f"col{i}" for i, (a, b) in enumerate(zip(header1, header2))]
            
            new_rows = []

            # Lire les données à partir de la ligne 2 (ignorer l'en-tête)
            for line in lines[2:]:
                parts = line.strip().split()
                if len(parts) >= len(col_names):
                    hip_id = f"{parts[0]} {parts[1]}"
                    row = [hip_id] + parts[2:len(col_names)]
                    new_rows.append(row)
            
            # Modifie les noms de colonnes : fusionne les deux premières en 'hip_id'
            col_names = ['hip_id'] + col_names[2:]
            
            # Crée le DataFrame avec les bonnes colonnes
            df = pd.DataFrame(new_rows, columns=col_names)

        # Sauvegarde du DataFrame en CSV
        out_file = os.path.join(output_folder_all, os.path.basename(dat_file_path).replace(".dat", ".csv"))
        df.to_csv(out_file, index=False)
        print(f"✅ {os.path.basename(dat_file_path)} bien converti avec succès.")

    except Exception as e:
        print(f"❌ Erreur pour {dat_file_path} : {e}")



# Conversion des fichiers .dat
for dat_file in dat_files:
    dat_file_path = os.path.join(dat_folder, dat_file)  # Chemin complet du fichier .dat
#     convert_dat_to_csv(dat_file_path)




# Démarrer le JVM (Java Virtual Machine) pour utiliser Aspose.Cells
#jpype.startJVM()

# 1. Copier les fichiers .sed dans un autre répertoire pour éviter d'écraser les originaux
def copy_files(source_dir, dest_dir):
    try:
        # Vérifier si le répertoire source existe
        if not os.path.exists(source_dir):
            print(f"Erreur : Le répertoire source '{source_dir}' n'existe pas.")
            return

        # Nettoyer le répertoire de destination avant de copier
        for filename in os.listdir(dest_dir):
            os.remove(os.path.join(dest_dir, filename))
        
        # Copier tous les fichiers du répertoire source vers le répertoire de destination
        for fic in os.listdir(source_dir):
            shutil.copy2(os.path.join(source_dir, fic), dest_dir)
        print(f"Tous les fichiers ont été copiés de '{source_dir}' vers '{dest_dir}'.")

    except Exception as e:
        print(f"Erreur lors de la copie des fichiers : {str(e)}")

# Copier les fichiers de 'path_sed1' vers 'path_sed2' puis de 'path_sed2' vers 'path_txt'
copy_files(path_sed1, path_sed2)
copy_files(path_sed2, path_txt)

# 2. Convertir les fichiers .sed en fichiers .txt
def convert_sed_to_txt(input_dir, output_dir):
    try:
        # Lister les fichiers .sed dans le répertoire d'entrée
        lst_sed = glob.glob(os.path.join(input_dir, "*.sed"))
        for file_path in lst_sed:
            # Créer un nouveau nom de fichier avec l'extension .txt
            txt_file_path = os.path.splitext(file_path)[0] + ".txt"
            os.rename(file_path, txt_file_path)  # Renommer le fichier .sed en .txt
        print(f"Conversion de {len(lst_sed)} fichiers .sed en .txt terminée.")

    except Exception as e:
        print(f"Erreur lors de la conversion des fichiers .sed en .txt : {str(e)}")

# Convertir les fichiers .sed en .txt dans 'path_txt'
convert_sed_to_txt(path_txt, path_txt)

# 3. Convertir les fichiers .txt en fichiers .csv
def convert_txt_to_csv(input_dir, output_dir):
    try:
        # Lister les fichiers .txt dans le répertoire d'entrée
        lst_txt = glob.glob(os.path.join(input_dir, "*.txt"))
        for txt_file in lst_txt:
            star_name = os.path.splitext(os.path.basename(txt_file))[0]
            try:
                # Lire le fichier .txt avec pandas et convertir en .csv
                file_txt = pd.read_csv(txt_file, delimiter=';')  # Ajuster le délimiteur selon le format
                file_csv_path = os.path.join(output_dir, f"{star_name}.csv")
                file_txt.to_csv(file_csv_path, index=False)  # Sauvegarder en .csv sans index
                print(f"Fichier '{txt_file}' converti en '{file_csv_path}'.")
            except Exception as e:
                print(f"Erreur lors de la conversion du fichier '{txt_file}' : {str(e)}")
            # Fermer la JVM après la conversion
            #jpype.shutdownJVM()

    except Exception as e:
        print(f"Erreur lors de la conversion des fichiers .txt en .csv : {str(e)}")

# Convertir les fichiers .txt en .csv dans 'path_txt' vers 'path_csv'
convert_txt_to_csv(path_txt, path_csv)

# Résultat final : Vérification du nombre de fichiers .csv générés
print(f"{len(os.listdir(path_csv))} fichiers .csv ont été générés dans '{path_csv}'.")



# # Boucle pour convertir tous les fichiers .sed dans le dossier
# for sed_file in os.listdir(sed_folder):
#     if sed_file.endswith(".sed"):  # Vérifie que ce soit un fichier .sed
#         sed_file_path = os.path.join(sed_folder, sed_file)  # Construit le chemin complet
#         check_sed_file(sed_file_path)  # Vérifie les erreurs avant de convertir
#         convert_sed_to_csv(sed_file_path)  # Convertit le fichier après la vérification
