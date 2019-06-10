# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:29:59 2019

@author: anael
"""

from __future__ import print_function
from rdkit import Chem
from rdkit.Chem import Draw


def picture(smile):
    image={}
    for i in smile :
        m = Chem.MolFromSmiles(smile[i])
        Draw.MolToFile(m)
    return(image)
        
    
smile = '[H]OC(=O)C([H])=C([H])C([H])=C([H])C(=O)O[H]'
m=Chem.MolFromSmiles(smile)
image=Draw.MolToImage(m)
