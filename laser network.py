# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:23:04 2019

@author: anael
Read the output of retropath
To visualize a csv file
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 
import requests

import csv
file='pathways.csv'
data=csv.reader(open(file))
tab=[]
for ligne in data :
    tab.append(ligne)



def pathway(nb):
    name=file+str(nb)
    LR=[]
    Lreact=[]
    Lprod=[]
    for i in range(len(tab)):
        if tab[i][0]==str(nb) :#we chose the pathway
            LR.append(tab[i][2]) #reaction = Unique ID
            Lreact.append(tab[i][3].split(":"))
            Lprod.append([tab[i][4]])
    print('LR = '+ str(LR))
    print('Lreact = '+ str(Lreact))
    print('Lprod = '+ str(Lprod))
    from nxvisualizer import network
    network(LR,Lreact,Lprod,name)   
    

   

    
    