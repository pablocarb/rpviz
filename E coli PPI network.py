# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:38:34 2019

@author: Anaelle
"""


import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 
import requests


tab=np.loadtxt('HT.PMID-15690043.EcoliNet.303gene.3446link.txt',dtype='str',delimiter='\t') #Network file
smartab=np.loadtxt('Copy_of_All_genes_of_E._coli_K-12_substr._MG1655.txt', dtype='str',delimiter='\t',usecols=(0,1)) #Smart table to assign a link to each node

reseau=nx.Graph() 
dic_links={}
for i in range(len(tab)):
    reseau.add_edge(tab[i][0],tab[i][1],weight=tab[i][2]) #network construction
for nodes in range(len(list(reseau.nodes))):
    for j in range(len(smartab)):
        if smartab[j][1][1:-1]==list(reseau.nodes)[nodes]: 
            url=smartab[j][0][1:-1]
            left, right = url.split(':') 
            url_new = ':'.join( [left, requests.utils.quote(right)] ) #to avoid encoding problems
            dic_links[list(reseau.nodes)[nodes]]= url_new#each link is assigned to each node
            
nx.set_node_attributes(reseau,name='link',values=dic_links)
nx.write_gml(reseau,'reseau.gml') 