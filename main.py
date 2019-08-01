# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:48:55 2019

@author: anael
"""

import argparse
import os
import csv
from .sbml2lists import sbml2list
from .csv2list_ind import csv2list2
from .network2json import network2
from .py2html import html
from .py2html2 import html2
from .nxvisualizer import network
import networkx as nx
import tarfile
import tempfile
import uuid

def arguments():
    parser = argparse.ArgumentParser(description='Visualizing a network from sbml')
    parser.add_argument('typeformat', 
                        help='Which format ? sbml/csv')
    parser.add_argument('inputtarfolder', 
                        help='Input folder with sbml files in tar format.')
    parser.add_argument('outfile',
                        help='html file.')
    parser.add_argument('--choice',
                        default="2",
                        help='What kind of input do you want ? \n 1/Single HTML file \n 2/Separated HTML files \n 3/View directly in Cytoscape \n 4/Generate a file readable in Cytoscape \n')
    parser.add_argument('--selenzyme_table',
                        default="N",
                        help='Do you want to display the selenzyme information ? Y/N')
    return parser
    

def run(tarfolder,outfile,typeformat="sbml",choice="2",selenzyme_table="N"):
    
    #Initialization
    G=nx.DiGraph()
    scores={}
    scores_col={}
    RdfG_o={}
    RdfG_m={}
    RdfG_uncert={}
    Path_flux_value={}
    Length={}
    
    def readoutput(G,f,output):
        """either from libsbml, or from readcsv"""
        
        LR=output[0]
        Lreact=output[1]
        Lprod=output[2]
        name=output[3]
        species_smiles=output[4]
        reac_smiles=output[5]
        images=output[6]
        images2=output[7]
        species_names=output[8]
        species_links=output[9]
        roots=output[10]
        dic_types=output[11]
        image2big=output[12]
        data_tab=output[13]
        dfG_prime_o=output[14]
        dfG_prime_m=output[15]
        dfG_uncert=output[16]
        flux_value=output[17]
        rule_id=output[18]
        rule_score=output[19]
        fba_obj_name=output[20]
        
        RdfG_o[f]=output[21]
        RdfG_m[f]=output[22]
        RdfG_uncert[f]=output[23]
        if flux_value !={}:
            Path_flux_value[f]=list(flux_value.values())[-1]
        Length[f]=len(LR)-1
        revers=output[24]
        
        G=network2(G,LR,Lreact,Lprod,name,species_smiles,reac_smiles,images,\
                   images2,species_names,species_links,roots,dic_types,\
                   image2big,data_tab, dfG_prime_o,dfG_prime_m, dfG_uncert,\
                   flux_value, rule_id,rule_score, fba_obj_name,revers)
                
        return(G,name,RdfG_o,RdfG_m,RdfG_uncert,Path_flux_value,Length)
        
    #READ AND EXTRACT TARFILE    
    tar = tarfile.open(tarfolder) ##read tar file
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        tar.extractall(path=tmpdirname)
        tar.close()
        infolder=tmpdirname
       
        #DEPEND ON THE FORMAT
        if typeformat=='sbml':
            """extract files in a temporary folder"""
    
            pathways=os.listdir(infolder)
            
            for f in pathways:
                print(f)
               
                file=os.path.join(infolder,f)   
                output=sbml2list(file, selenzyme_table)
                data=readoutput(G,f, output)
                G=data[0]
                name=data[1]
                RdfG_o=data[2]
                RdfG_m=data[3]
                RdfG_uncert=data[4]
                Path_flux_value=data[5]
                Length=data[6]
            
        if typeformat=='csv':
            
            # READ CSV FILE WITH PATHWAYS (out_path)
            csvfilepath=os.path.join(tmpdirname,"pathfile","out_paths.csv")
            datapath=[]
            with open(csvfilepath, 'r') as csvFile:
                reader = csv.reader(csvFile)       
                for row in reader:
                    datapath.append(row)
            csvFile.close()
            nbpath=int(datapath[-1][0])
   
            for path in range(1,nbpath+1): #for each pathway
                print(path)
                output=csv2list2(tmpdirname,path, datapath, selenzyme_table)
                data=readoutput(G,path, output)
                G=data[0]
                name=data[1]
                RdfG_o=data[2]
                RdfG_m=data[3]
                RdfG_uncert=data[4]
                Path_flux_value=data[5]
                Length=data[6]
                
            pathways=range(1,nbpath+1)
                
            
    scores["dfG_prime_o (kJ/mol)"]=RdfG_o
    scores["dfG_prime_m (kJ/mol)"]=RdfG_m
    scores["dfG_uncert (kJ/mol)"]=RdfG_uncert
    scores["flux_value (mmol/gDW/h)"]=Path_flux_value
    scores["length"]=Length
  
    
    #DISPLAY THE OUTPUT
    if choice == "3": #view in cytoscape
        network(G,name,outfile)
        
    elif choice =="4":
        path=os.path.join("cytoscape_files",str(name)+".gml")
        nx.write_gml(G,path)
            
    if choice =="1": #view in single html
        html2(G,pathways,outfile,scores,scores_col)

    elif choice=="2":#view in separated files
        html(G,pathways,outfile,scores,scores_col)
        
           
    #CREATE TAR FILE AS OUTPUT
    fid = str(uuid.uuid4())
    tFile = tarfile.open(fid+".tar", 'w')
    
    files = os.listdir("outfile")
    print(files)
    for f in files:
        tFile.add(os.path.join(os.path.abspath("outfile"),f))
        
    tFile.close()
            

  
if __name__ == '__main__':
    parser = arguments()
    arg = parser.parse_args()
    run(arg.inputtarfolder,arg.outfile,arg.typeformat,arg.choice,arg.selenzyme_table)
