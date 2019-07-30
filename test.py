# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:42:24 2019

@author: anael
"""
import rdkit
from rdkit import Chem
from rdkit.Chem.Draw import *

smiles="[H]N=C(O[H])C1=C([H])N(C2([H])OC([H])(C([H])([H])OP(=O)(O[H])OP(=O)(O[H])OC([H])([H])C3([H])OC([H])(n4c([H])nc5c(N([H])[H])nc([H])nc54)C([H])(OP(=O)(O[H])O[H])C3([H])O[H])C([H])(O[H])C2([H])O[H])C([H])=C([H])C1([H])[H]"
mol = Chem.MolFromSmiles(smiles)
filename=smiles+'.svg'
rdkit.Chem.Draw.MolToFile(mol,filename)

with open(smiles+".svg", 'w') as f:
    f.write("test")
    f.close()