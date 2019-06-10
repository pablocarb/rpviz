# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:29:59 2019

@author: anael
"""

from __future__ import print_function
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D


def picture(smile):
    image={}
    for i in smile :
        mol = Chem.MolFromSmiles(smile[i])
        rdDepictor.Compute2DCoords(mol)
        drawer = rdMolDraw2D.MolDraw2DSVG(200,200)
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        image[i]=svg.split("?>\n")[1]
    return(image)
        
    
