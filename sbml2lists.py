#!/usr/bin/env python
# coding: utf-8
'''To visualize a SBML file'''
# In[3]:


import libsbml
#import networkx as nx
#import matplotlib.pyplot as plt
import argparse
import os

def arguments():
    parser = argparse.ArgumentParser(description='Visualizing a network from sbml')
    parser.add_argument('infile', 
                        help='Input sbml file.')
#    parser.add_argument('outfile1', 
#                        help='json file.')
#    parser.add_argument('outfile2', 
#                        help='html file.')
    return parser

parser = arguments()
arg = parser.parse_args()


# In[4]:


#open the SBML using libsbml
assert os.path.exists('infile/'+arg.infile)
file='infile/'+arg.infile
doc = libsbml.readSBML(file)
name=arg.infile
name=name.split(".")[0]


# In[8]:


#return the model from the SBML document using libsbml
model = doc.model


# In[9]:


#we will use the groups package to return the retropath pathway
#that is all the reactions that are associated with the heterologous 
#pathway
groups = model.getPlugin('groups')


# In[10]:


#in the rpFBA script, rp_pathway is the default name
rp_pathway = groups.getGroup('rp_pathway') 


# In[63]:

rlist=[]
Lreact=[]
Lprod=[]
LR=[]

heterologous_pathway_dG_prime_o = {}


#loop through all the members of the rp_pathway
for member in rp_pathway.getListOfMembers():
    print(member)
    print(type(member))
    #fetch the reaction according to the member id
    reaction = model.getReaction(member.getIdRef())
    rlist.append(reaction)
    LR.append(str(reaction))
    #get the annotation of the reaction
    #includes the MIRIAM annotation and the IBISBA ones
    annotation = reaction.getAnnotation()
    ibisba_annotation = annotation.getChild('RDF').getChild('Ibisba').getChild('ibisba')
    #extract one of the ibisba annotation values
    heterologous_pathway_dG_prime_o[member.getIdRef()] = ibisba_annotation.getChild('dG_prime_o').getAttrValue('value')



# In[64]:


heterologous_pathway_dG_prime_o

for reaction in range(len(rlist)):
    Lreact.append([p.species for p in rlist[reaction].reactants]) #get list of reactants
    Lprod.append([p.species for p in rlist[reaction].products]) #get list of products


    Lelement=[] #List of all elements
    for i in range(len(Lreact)):
        for j in range(len(Lreact[i])):
            Lelement.append(Lreact[i][j])
        for k in range(len(Lprod[i])):
            Lelement.append(Lprod[i][k])
    Lelement=set(Lelement)
        
    smile={}
    for sp in Lelement :
        species=model.getSpecies(sp)
        annotation = species.getAnnotation()
        ibisba_annotation = annotation.getChild('RDF').getChild('Ibisba').getChild('ibisba')
        smile_str=ibisba_annotation.getChild('smiles').toXMLString()
        smile[sp]=smile_str.split(">")[1].split("<")[0] #to get only the smile

        
from smile2picture import picture
image=picture(smile)
    

#Cytoscape Network
#from nxvisualizer import network
#network(LR,Lreact,Lprod,name,smile,image)

#Convert network to json file
from network2json import  network2 #to convert the lists in a json network
network2(LR,Lreact,Lprod,name,smile,image)