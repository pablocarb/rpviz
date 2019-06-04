# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:23:33 2019

@author: anael
"""

import networkx as nx
import json


def network2(LR,Lreact,Lprod,name,smile,image):
    ###Create the network with networkx
    G=nx.DiGraph()
    LR.reverse()
    G.add_nodes_from(LR) #add reactions nodes
    
    
    for i in range(len(LR)):
        for j in range(len(Lreact[i])):
            G.add_edge(Lreact[i][j],LR[i]) #add reactants nodes
        for k in range(len(Lprod[i])):
            G.add_edge(LR[i],Lprod[i][k]) #add products nodes
    
    #Attribute category
    
    dic_types={}
    for i in range(len(LR)):
        dic_types[(list(G.nodes))[i]]='reactions'
        for node in range(len(list(G.nodes))):
            if list(G.nodes)[node] in Lprod[i]:
                dic_types[list(G.nodes)[node]]='product'
            if list(G.nodes)[node] not in dic_types:
                dic_types[list(G.nodes)[node]]='reactant'
    nx.set_node_attributes(G,name='category',values=dic_types)   
    #nx.draw(G)
    
    #Attribute smile
    nx.set_node_attributes(G, name='smiles', values=smile)
    
    #Attribute image
    nx.set_node_attributes(G,name='image', values=image)

    
    js = nx.readwrite.json_graph.cytoscape_data(G)
    #json.dump(js,open(os.path.join('file_json',name,'.json'),'w')) #doesn't work on Windows
    file = 'file_json/'+name+'.json'
    json.dump(js,open(file,'w'))

    from py2html import html
    html(file, name)