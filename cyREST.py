# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:27:46 2019

@author: anael
"""

import networkx as nx
from IPython.display import Image
import requests
import json

# Library for util
from py2cytoscape import util as cy 

#from collections import OrderedDict
#import numpy as np


#output_notebook()


# Basic Setup
PORT_NUMBER = 1234

#IP = '192.168.1.1'
IP = 'localhost'

BASE = 'http://' + IP + ':' + str(PORT_NUMBER) + '/v1/'

# Header for posting data to the server as JSON
HEADERS = {'Content-Type': 'application/json'}

# Delete all networks in current session
requests.delete(BASE + 'session')


#Test with sbml network

def network(LR,Lreact,Lprod):
    
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
    
    #Visualize network in Cytoscape
    cytoscape_network_sbml = cy.from_networkx(G)
    res1 = requests.post(BASE + 'networks', data=json.dumps(cytoscape_network_sbml), headers=HEADERS) #create the network in cytoscape
    res1_dict = res1.json()
    new_suid = res1_dict['networkSUID']
    requests.get(BASE + 'apply/layouts/hierarchical/' + str(new_suid)) 
    Image(BASE+'networks/' + str(new_suid) + '/views/first.png') #to see in python
    
    #Style
    res = requests.get(BASE + 'styles/default')
    print(json.dumps(json.loads(res.content), indent=4))
    
    style_name = 'My Visual Style'
    
    my_style = {
      "title" : style_name,
      "defaults" : [ {
        "visualProperty" : "EDGE_WIDTH",
        "value" : 2.0
      }, {
        "visualProperty" : "EDGE_STROKE_UNSELECTED_PAINT",
        "value" : "#555555"
      }, 
        {
            "visualProperty": "EDGE_TARGET_ARROW_SHAPE",
            "value": "DELTA"
        },
        {
        "visualProperty" : "NODE_FILL_COLOR",
        "value" : "#00ddee"
      },{
        "visualProperty" : "NODE_BORDER_WIDTH",
        "value" : 0
      }, {
        "visualProperty" : "NODE_SIZE",
        "value" : 30
      }],
      "mappings" : [ { #Color of nodes depends on the category
        "mappingType" : "discrete",
        "mappingColumn" : "category",
        "mappingColumnType" : "String",
        "visualProperty" : "NODE_FILL_COLOR",
        "map" : [ {
          "key" : "reactant",
          "value" : "#4D833C"
        }, {
          "key" : "product",
          "value" : "#C04E5D"
        } ]
      }, {
        "mappingType" : "passthrough", #To see labels
        "mappingColumn" : "name",
        "mappingColumnType" : "String",
        "visualProperty" : "NODE_LABEL"
      },
        {
        "mappingType" : "discrete", #To see labels
        "mappingColumn" : "category",
        "mappingColumnType" : "String",
        "visualProperty" : "NODE_SHAPE",
        "map" : [ {
          "key" : "reactions",
          "value" : "RECTANGLE"
        }]
      }
        ]
    }
    
    # Delete all style
    requests.delete(BASE + "styles")
    
    # Create new Visual Style
    res = requests.post(BASE + "styles", data=json.dumps(my_style), headers=HEADERS)
    new_style_name = res.json()['title']
    
    # Apply it to current netwrok
    requests.get(BASE + 'apply/styles/' + new_style_name + '/' + str(new_suid))
    
    # Display it here!
    Image(BASE+'networks/' + str(new_suid) + '/views/first.png')
