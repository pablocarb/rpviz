# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:21:48 2019

@author: anael
"""
#Usefull
import inspect
#inspect.getargspec(function)

import networkx as nx
from IPython.display import Image
import requests
import json
import pandas as pd

# Library for util
from py2cytoscape.data.cynetwork import CyNetwork
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape.data.style import StyleUtil

#List of elements from other functions
#LR = ['MNXR84948_MNXM556',
#  'MNXR17733_MNXM5901,MNXR84871_MNXM1208',
#  'MNXR15003_MNXM987,MNXR227_MNXM264',
#  'MNXR7111_MNXM505',
#  'MNXR7145_MNXM438,MNXR93681_MNXM438']
#Lreact= [['1.CMPD_0000000001'],
#  ['1.CMPD_0000000003', '1.MNXM40'],
#  ['1.CMPD_0000000010', '1.MNXM12'],
#  ['1.CMPD_0000000018', '1.MNXM4', '1.MNXM6'],
#  ['1.MNXM97']]
#Lprod= [['1.TARGET_0000000001'],
#  ['1.CMPD_0000000001'],
#  ['1.CMPD_0000000003'],
#  ['1.CMPD_0000000010'],
#  ['1.CMPD_0000000018']]

def network(LR,Lreact,Lprod,name):
    ###Create the network with networkx
    G=nx.DiGraph()
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
    print(dic_types)
    nx.set_node_attributes(G,name='category',values=dic_types)   
    
    
    #Connect with cytoscape
    cy = CyRestClient()
    
    # Reset
    #cy.session.delete()
    
    #To create the network in cytoscape
    network = cy.network.create_from_networkx(G, name='NetworkG', collection='My network collection')
    print('New network created with py2cytoscape.  Its SUID is ' + str(network.get_id()))
    
    #To get the SUID of all the components of the network
    all_suid = cy.network.get_all()
    net1 = cy.network.create(all_suid[0])
    print(net1.get_first_view())
    
    #Styles
    cy.layout.apply(name='hierarchical', network=network)
    
    # Get all existing Visual Styles
    styles = cy.style.get_all()
    print(json.dumps(styles, indent=4))
    
    
    # Get a reference to the existing style
    default_style = cy.style.create('default')
    print(default_style.get_name())
    
    # Get all available Visual Properties
    print(len(cy.style.vps.get_all()))
    node_vps=cy.style.vps.get_node_visual_props()
    edge_vps = cy.style.vps.get_edge_visual_props()
    network_vps=cy.style.vps.get_network_visual_props()
    print(pd.Series(edge_vps).head())
    print(pd.Series(node_vps).head())
    
    
    # Create a new style
    style1 = cy.style.create("My_style")
    print(style1.get_name())
    
    
    new_defaults = {
        # Node defaults
        'NODE_FILL_COLOR': '#00ddee',
        'NODE_SIZE': 20,
        'NODE_BORDER_WIDTH': 0,
        'NODE_LABEL_COLOR': 'black',
        
        # Edge defaults
        'EDGE_WIDTH': 3,
        'EDGE_STROKE_UNSELECTED_PAINT': '#aaaaaa',
        'EDGE_LINE_TYPE': 'LONG_DASH',
        'EDGE_TARGET_ARROW_SHAPE' : 'DELTA',
        
        # Network defaults
        'NETWORK_BACKGROUND_PAINT': 'white',
    }
    
    style1.update_defaults(new_defaults)
    #Apply style
    cy.style.apply(style1, network)
    
    # Passthrough mapping to get node labels
    style1.create_passthrough_mapping(column='name', col_type='String', vp='NODE_LABEL')
    
    # Discrete mapping for node colours:
    cat = {
        'reactant': '#4D833C',
        'product': '#C04E5D'
    }
    style1.create_discrete_mapping(column='category', 
                                   col_type='String', 
                                   vp='NODE_FILL_COLOR', 
                                   mappings=cat)
    
    # Discrete mapping for node shape:
    reac = {
        'reactions': 'RECTANGLE'
    }
    style1.create_discrete_mapping(column='category', 
                                   col_type='String', 
                                   vp='NODE_SHAPE', 
                                   mappings=reac)
    
