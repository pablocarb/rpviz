# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 16:02:42 2019

@author: anael
"""
import csv

def downloadcsv(f,LR,reac_smiles,dfG_prime_o,dfG_prime_m,dfG_uncert,flux_value,\
            rule_id,rule_score,RdfG_o,RdfG_m, RdfG_uncert,Path_flux_value):
    """create a csv file for each pathway"""
  
    del LR[-1]
    with open(str(f)+'.csv', 'w') as csvfile:
        fieldnames = ['Pathway', 'Reaction','Reaction SMILES']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in LR:     
            writer.writerow({'Pathway': f, 'Reaction': i,'Reaction SMILES':reac_smiles[i]})
    csvfile.close()