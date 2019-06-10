# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:48:55 2019

@author: anael
"""

import argparse
import os
from sbml2lists import sbml2list

def arguments():
    parser = argparse.ArgumentParser(description='Visualizing a network from sbml')
    parser.add_argument('inputfolder', 
                        help='Input folder with sbml files.')
    parser.add_argument('outfile', 
                        help='html file.')
    return parser

def run(infolder,outfile):

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
        species_names=output[5]
        species_links=output[6]

        #from smile2picture import picture
        #image=picture(species_smiles)

        from network2json import network2
        json_elements[name]=network2(LR,Lreact,Lprod,name,species_smiles,species_names,species_links)

    from py2html2 import html2
    html2(json_elements, outfile)

if __name__ == '__main__':
    parser = arguments()
    arg = parser.parse_args()
    run(arg.inputfolder,arg.outfile)
