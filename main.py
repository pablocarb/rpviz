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
from .downloadcsv import downloadcsv
import networkx as nx
import tarfile
import tempfile
import uuid
import shutil,glob
import json

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
    

def run(tarfolder,outfolder,typeformat="sbml",choice="2",selenzyme_table="N"):
    print(typeformat)
    
    #Initialization
   
    scores={}
    scores_col={}
    RdfG_o={}
    RdfG_m={}
    RdfG_uncert={}
    Path_flux_value={}
    Length={}
    dict_net={}
  
    #CREATE DIC WITH MNX COMPOUNDS
    reader = csv.reader(open(os.path.join(os.path.dirname(__file__),"chem_prop.tsv")),delimiter="\t")
    d={}
    for i in range(385): #skip &st rows
        next(reader)
    for row in reader:
        d[row[0]]=list(row[1:])[0]
    
    def readoutput(f,output,outfolder):
        """either from libsbml, or from readcsv"""
        G=nx.DiGraph() #new pathway = new network
        LR=output[0]
        Lreact=output[1]
        Lprod=output[2]
        name='path'+output[3]
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
        
        #CREATE NETWORK DICTIONNARY
        js = nx.readwrite.json_graph.cytoscape_data(G)
        elements=js['elements']
        dict_net[name]=elements
                
        downloadcsv(outfolder,f,LR,reac_smiles,Lreact,Lprod,species_names,dfG_prime_o,dfG_prime_m,dfG_uncert,flux_value,\
                    rule_id,rule_score,RdfG_o,RdfG_m, RdfG_uncert,Path_flux_value)
                
        return(G,name,RdfG_o,RdfG_m,RdfG_uncert,Path_flux_value,Length)
        
    #READ AND EXTRACT TARFILE
    try:
        tar = tarfile.open(tarfolder) ##read tar file
        isFolder = False
    except:
        isFolder = True
    with tempfile.TemporaryDirectory() as tmpdirname:
        if not isFolder:
            print('created temporary directory', tmpdirname)
            tar.extractall(path=tmpdirname)
            tar.close()
            infolder=tmpdirname
        else:
            infolder=tarfolder
            tmpdirname=tarfolder #the folder is directly the input, not temporary
       
        #DEPEND ON THE FORMAT
        if typeformat=='sbml':
            """extract files in a temporary folder"""
    
            pathways=os.listdir(infolder)
            for f in pathways:
                print(f)
               
                file=os.path.join(infolder,f)   
                output=sbml2list(file, selenzyme_table,d)
                data=readoutput(f, output,outfolder)
                RdfG_o=data[2]
                RdfG_m=data[3]
                RdfG_uncert=data[4]
                Path_flux_value=data[5]
                Length=data[6]
              
            
        if typeformat=='csv':
            
            # READ CSV FILE WITH PATHWAYS (out_path)
            csvfilepath=os.path.join(tmpdirname,"path","out1","out_paths.csv")
            datapath=[]
            with open(csvfilepath, 'r') as csvFile:
                reader = csv.reader(csvFile)       
                for row in reader:
                    datapath.append(row)
            csvFile.close()
            nbpath=int(datapath[-1][0])
   
            for path in range(1,nbpath+1): #for each pathway
                print(path)
                output=csv2list2(tmpdirname,path, datapath, selenzyme_table,d)
                data=readoutput(path, output,outfolder)
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
  

    if choice=="2":#view in separated files
        for f in glob.glob(os.path.join(os.path.dirname(__file__),'new_html','*')): #to copy the required files in the outfolder
            shutil.copy(f,outfolder)
        html(outfolder,pathways,scores,scores_col,dict_net)
        os.chdir( outfolder )
        return (os.path.join(os.path.abspath(outfolder), 'index.html'))
        
    elif choice=="5":
        for f in glob.glob(os.path.join(os.path.dirname(__file__),'new_html','*')):
            shutil.copy(f,outfolder)
        html(outfolder,pathways,scores,scores_col,dict_net)
        #CREATE TAR FILE AS OUTPUT
        fid = str(uuid.uuid4())
        newtarfile = os.path.join(os.path.abspath(outfolder),fid+'.tar')
        files = os.listdir(outfolder)
        os.chdir( outfolder )        
        tFile = tarfile.open(newtarfile, 'w')
        for f in files:
            tFile.add(f)
        tFile.close()
        return(newtarfile)  
        
            

  
if __name__ == '__main__':
    parser = arguments()
    arg = parser.parse_args()
    run(arg.inputtarfolder,arg.outfile,arg.typeformat,arg.choice,arg.selenzyme_table)
