# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:23:04 2019

@author: anael
Read the output of retropath
To visualize a csv file
"""

import csv
import argparse
import os

def arguments():
    parser = argparse.ArgumentParser(description='Visualizing a network from csv')
    parser.add_argument('infile', 
                        help='Input csv file.')
    #parser.add_argument('outfile', 
                       # help='Input some file.')
    return parser

parser = arguments()
arg = parser.parse_args()

assert os.path.exists('infile/'+arg.infile)
file='infile/'+arg.infile
data=csv.reader(open(file))
tab=[]
for ligne in data :
    tab.append(ligne)
    
List=[] #List of different number of pathways in the file
for i in range(1,len(tab)):
    List.append(int(tab[i][0]))
    List=list(set(List))
    List.sort()
for i in range(len(List)) :
    nb=int(List[i])
    name=file+str(nb)
    LR=[]
    Lreact=[]
    Lprod=[]
    for i in range(len(tab)):
        if tab[i][0]==str(nb) :#we chose the pathway
            LR.append(tab[i][2]) #reaction = Unique ID
            Lreact.append(tab[i][3].split(":"))
            Lprod.append([tab[i][4]])
    #print('LR = '+ str(LR))
    #print('Lreact = '+ str(Lreact))
    #print('Lprod = '+ str(Lprod))
    #from nxvisualizer import network
    #network(LR,Lreact,Lprod,name)   
    from network2json import  network2 #to convert the lists in a json network
    network2(LR,Lreact,Lprod,name)
    

   

    
    