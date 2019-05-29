# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:23:04 2019

@author: anael
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 
import requests

import csv
data=csv.reader(open('pathways.csv'))
tab=[]
for ligne in data :
    tab.append(ligne)



def pathway(nb):
    LR=[]
    Lreact=[]
    Lprod=[]
    for i in range(len(tab)):
        if tab[i][0]==str(nb) :#we chose the pathway
            LR.append(tab[i][2]) #reaction = Unique ID
            Lreact.append(tab[i][3].split(":"))
            Lprod.append([tab[i][4]])
    print(LR)
    print(Lreact)
    print(Lprod)
    import cyREST
    cyREST.network(LR,Lreact,Lprod)   
    

   

    
    