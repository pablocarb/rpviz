#!/usr/bin/env python
# coding: utf-8
'''To visualize a SBML file'''
# In[3]:


import libsbml
#import networkx as nx
#import matplotlib.pyplot as plt



# In[4]:
def sbml2list(file):
    
    #open the SBML using libsbml
    
    doc = libsbml.readSBML(file)
    name=file.split('\\')[1]
    
    
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
    LR=[]
    
    heterologous_pathway_dG_prime_o = {}
    
    
    #loop through all the members of the rp_pathway
    for member in rp_pathway.getListOfMembers():
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
    
    Lreact=[]
    Lprod=[]
    
    for reaction in range(len(rlist)):
        Lreact.append([p.species for p in rlist[reaction].reactants]) #get list of reactants id
        Lprod.append([p.species for p in rlist[reaction].products]) #get list of products id
    
    mem = []
    for member in rp_pathway.getListOfMembers():
        reac = model.getReaction(member.getIdRef())
        for pro in reac.getListOfProducts():
            mem.append(pro.getSpecies())
            Lprod.append(pro.getSpecies())
        for rea in reac.getListOfReactants():
            mem.append(rea.getSpecies())
            Lreact.append(rea.getSpecies())
    
    #mem = list(set([i for i in mem if i[0:3]!='MNX']))
    species_smiles = {}
    species_links={}
    species_names={}
    #loop through all the members of the rp_pathway
    for member in list(set([i for i in mem])):
        #fetch the species according to the member id
        reaction = model.getSpecies(member)
        spname=reaction.getName()
        if spname:
            species_names[member]=spname
        #get the annotation of the species
        #includes the MIRIAM annotation and the IBISBA ones
        annotation = reaction.getAnnotation()
        ibisba_annotation = annotation.getChild('RDF').getChild('Ibisba').getChild('ibisba')
        #extract one of the ibisba annotation values
        smiles = ibisba_annotation.getChild('smiles').getChild(0).toXMLString()
        if smiles:
            species_smiles[member] = smiles
        link_annotation=annotation.getChild('RDF').getChild('Description').getChild('is').getChild('Bag')
        for i in range(link_annotation.getNumChildren()):
            str_annot = link_annotation.getChild(i).getAttrValue(0) #Here we get the attribute at location "0". It works since there is only one
            if str_annot.split('/')[-2]=='metanetx.chemical':
                species_links[member]=str_annot #here is the MNX code returned
    
    
    # In[64]:
    
    return(LR, Lreact, Lprod, name, species_smiles, species_names, species_links)
    #from smile2picture import picture
    #image=picture(species_smiles)
        
    
    #Cytoscape Network
    #from nxvisualizer import network
    #network(LR,Lreact,Lprod,name,species_smiles,image)
    
    #Convert network to json file
    #from network2json import  network2 #to convert the lists in a json network
    #network2(LR,Lreact,Lprod,name,species_smiles,image,species_names,species_links)