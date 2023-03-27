#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:20:04 2023

@author: nbadolo
"""

import os
import pandas as pd


str_name_path1 = '/home/nbadolo/A_large_log/'
lst_str1 = os.listdir(str_name_path1)
n_lst_str1 = len(lst_str1)

out_path1 = '/home/nbadolo/Bureau/Aymard/Donnees_sph/pyssed_log/txt_files/'
out_path2 = '/home/nbadolo/SIM_CODES/PySSED/v0.2/src/'
lst_name1 = 'log_lst.list'
log_lst = open("{}/{}".format(out_path1, lst_name1), "w")
log_lst_ = open("{}/{}".format(out_path2, lst_name1), "w")
log_lst.write("{}\n".format('Star_name'))
log_lst_.write("{}\n".format('Star_name'))

for i in range(n_lst_str1) :
    #print('le premier element est ' + str(lst_str1[0]))
    print(lst_str1[i])
    log_lst.write("{}\n".format(lst_str1[i]))
    log_lst_.write("{}\n".format(lst_str1[i]))
print('le nombre d_objets total  à étudier est ' + str(n_lst_str1))

str_name_path2 = '/home/nbadolo/Bureau/Aymard/These/for_biblio_papers/used_tables/large_log.ods'
df_l = pd.read_excel(str_name_path2)
ident_str  = df_l["HIP"]
n_ident = len(ident_str)

lst_name2 = 'large_log.list'
large_log = open("{}/{}".format(out_path1, lst_name2), "w")
large_log_ = open("{}/{}".format(out_path2, lst_name2), "w")
large_log.write("{}\n".format('Star_name'))
large_log_.write("{}\n".format('Star_name'))
for i in range(n_ident):
    #print('le premier element est ' + str(ident_str[0]))    
    ID = ident_str[i]
    hip_id = 'HIP ' + str(ID)
    print(hip_id)
    large_log.write("{}\n".format(hip_id))
    large_log_.write("{}\n".format(hip_id))              

print('le nombre d_objets simbad est ' + str(n_ident))
