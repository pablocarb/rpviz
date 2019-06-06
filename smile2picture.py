# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:29:59 2019

@author: anael
"""

from __future__ import print_function
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem

def picture(smile):
    image={}
    for i in smile :
        m = Chem.MolFromSmiles(smile[i])
        AllChem.Compute2DCoords(m)
        Draw.MolToFile(m,"file_html/molecules/"+i+".svg") #to save the picture in svg format
        image[i]="molecules/"+i+".svg"
    return(image)
        
    

