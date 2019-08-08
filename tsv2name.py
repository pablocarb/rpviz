# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:56:48 2019

@author: anael
"""

import pandas as pd
import cirpy

def id2name(id):
    """for MNX compounds"""
    dataname=pd.read_csv('rpviz/chem_prop.tsv', sep="\t", skiprows=385)
    dataname = dataname.rename(columns={'#MNX_ID': 'MNX_ID'})
    try : 
        name=dataname.loc[dataname['MNX_ID']==id,'Description'].values[0] 
    except :
        name=id                                
    return(name)
    

#smiles='[H]OC(=O)C([H])(N([H])[H])C([H])([H])c1c([H])c([H])c(O[H])c(O[H])c1[H]'
def smile2name(smiles,id):
    """for products compounds"""
    try :
        name=cirpy.query(smiles,'names')[0].value[0]
    except :
        name=id
    return(name)
    