# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:48:55 2019

@author: anael
"""

import argparse
import os
import json
from sbml2lists import sbml2list
from network2json import network2
from py2html import html
from py2html2 import html2
from nxvisualizer import network
import networkx as nx

def arguments():
    parser = argparse.ArgumentParser(description='Visualizing a network from sbml')
    parser.add_argument('inputfolder', 
                        help='Input folder with sbml files.')
    parser.add_argument('outfile',
                        help='html file.')
    return parser

def run(infolder,outfile):

    choice=input ("What kind of output do you want ?\n 1/Single HTML file \n 2/Separated HTML files \n 3/View directly in Cytoscape \n 4/Generate a file readable in Cytoscape \n")
    folders=os.listdir(infolder)

    json_elements={}
    for f in folders:
        file=os.path.join(infolder,f)   
        output=sbml2list(file)
        LR=output[0]
        Lreact=output[1]
        Lprod=output[2]
        name=output[3]
        species_smiles=output[4]
        images=output[5]
        species_names=output[6]
        species_links=output[7]
        roots=output[8]

        #from smile2picture import picture
        #image=picture(species_smiles)

        
        json_elements[name]=network2(LR,Lreact,Lprod,name,species_smiles,images,species_names,species_links,roots)[0]
    
        net = network2(LR,Lreact,Lprod,name,species_smiles,images,species_names,species_links,roots)[1]
        
        #If you want to visualize directly in Cytoscape:
        if choice == "3":
            network(net,name,outfile)
            
        elif choice =="4":
            path=os.path.join("cytoscape_files",str(name)+".gml")
            nx.write_gml(net,path)
            
    if choice =="1":
        html2(json_elements,outfile)
    
    elif choice=="2":
        html(json_elements,outfile)
        
    
    

if __name__ == '__main__':
    parser = arguments()
    arg = parser.parse_args()
    run(arg.inputfolder,arg.outfile)
