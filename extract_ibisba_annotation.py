#!/usr/bin/env python
# coding: utf-8

# In[4]:


import libsbml
import networkx as nx
import matplotlib.pyplot as plt

# In[4]:


#open the SBML using libsbml
doc = libsbml.readSBML('rp_1')


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
    Lreact.append([p.species for p in rlist[reaction].reactants])
    Lprod.append([p.species for p in rlist[reaction].products])

print('LR = '+ str(LR))
print('Lreact = '+ str(Lreact))
print('Lprod = '+ str(Lprod))

##GML Network from those lists

G=nx.DiGraph()
G.add_nodes_from(LR) #add reactions nodes

for i in range(len(LR)):
    for j in range(len(Lreact[i])):
        G.add_edge(Lreact[i][j],LR[i]) #add reactants nodes
    for k in range(len(Lprod[i])):
        G.add_edge(LR[i],Lprod[i][k]) #add products nodes


colours_nodes = ["yellow"] * G.number_of_nodes()
for i in range(len(LR)):
    colours_nodes[i]='red' #reactions are in red
for j in range(len(Lreact)):
    colours_nodes[len(LR)+j]='green' #reactants are in green

options = {
      'node_color' : colours_nodes,
      'node_size'  : 550,
      'edge_color' : 'tab:grey',
      'with_labels': True
    }

nx.draw(G,**options)

nx.write_gml(G,'example.gml')

#Cytoscape Network
import cyREST
cyREST.network(LR,Lreact,Lprod)
