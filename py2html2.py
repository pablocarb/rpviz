# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:07:03 2019

@author: anael
"""

import json
import os
from bs4 import BeautifulSoup
import networkx as nx
import pandas as pd
from color_grad import linear_gradient


def html2(G,folder,outfile,scores,scores_col):
    
    js = nx.readwrite.json_graph.cytoscape_data(G)
    elements=js['elements']
    
    
    htmlfile= open(os.path.join("new_html","template2.html"))
    soup = BeautifulSoup(htmlfile, 'html.parser')   

    ##Append elements
    element_script=soup.find(id="elements") #select the script section containing elements
    element_script.append("var obj ="+json.dumps(elements))  
    
    ##Append scores
    scores["Choose_a_score"]={i:0 for i in folder}
    element_script.append("var scores ="+json.dumps(scores))
    
        
    ##Append color dictionaries
    hex = linear_gradient("#3a46d5","#da3c29",len(folder))["hex"]
    for score in scores:
        L=[]
        dic=sorted(scores[score].items(), key=lambda x: float(x[1])) #Compare float not str
      
        for e in dic:
            L.append(e[0])
 
        
        col={L[i]:hex[i] for i in range(len(L))}
        scores_col["col_"+score]=col
        
    element_script.append("var scores_col ="+json.dumps(scores_col))
    select_script=soup.find(id="selectbox")

    
    for i in scores:
        new_tag=soup.new_tag("option")
        new_tag["value"]=i
        new_tag.append(i)
        select_script.append(new_tag)
    
    #Pathway table        
    pathways = [f for f in folder]
    d={'Pathway':pathways}
    df=pd.DataFrame(d)
    df["Select"]=[('<input type="checkbox" value="'+str(f)+'" />') for f in folder]
    df["Score"]=[''for f in folder]
    
    html_str=df.to_html(index=False)
    html_str=html_str.replace("&lt;","<").replace("&gt;",">")
                
    table=soup.find(id="table_choice")
    table.append(BeautifulSoup(html_str, 'html.parser'))  
      
        
    htmlfile.close()
        
    html = soup.prettify("utf-8")

    with open(os.path.join("new_html",outfile), "wb") as file:
        file.write(html)    
