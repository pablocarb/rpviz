# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:29:59 2019

@author: anael
"""

from __future__ import print_function
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem import rdChemReactions
from rdkit.Chem.Draw import ReactionToImage
from lxml import etree

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
 
def picture2(rsmile):
    image2={}
    image2big={}
    for i in rsmile:
        r = rdChemReactions.ReactionFromSmarts(rsmile[i], useSmiles=True)
        m = ReactionToImage(r,useSVG=True)
        image=m.split("?>\n")[1] 
        root = etree.fromstring(image, parser=etree.XMLParser()) #resizing html
        header=root.attrib
        width=header['width'][:-2]
        header['width']='385px'
        header['height']='100px'
        header['viewbox']='0 0 '+width+' 200'
        imagemod=etree.tostring(root)
        image2[i]=imagemod.decode("utf-8")
        image2big[i]=image
    return(image2,image2big)
 