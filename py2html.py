# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:02:54 2019

@author: anael
"""


import json
import os
from bs4 import BeautifulSoup


def html(jsondata,outfile):
    htmlfile= open(os.path.join("new_html","template.html"))
    soup = BeautifulSoup(htmlfile, 'html.parser')   
    nt={}

    for key in jsondata.keys():
        name=key

        obj=json.loads(jsondata[key])
        elements=obj['elements']
        nt[name]=dict(elements)
        net=json.dumps(nt)
            
        select=soup.find(id="selectbox")
        new_tag=soup.new_tag("option")
        new_tag["value"]=str(name)
        new_tag.append(name)
        select.append(new_tag)
        
    with open("new_html/network_elements.js","w") as jsoutfile:
        jsoutfile.write("var obj= "+net)
    
    htmlfile.close()
        
    html = soup.prettify("utf-8")
    with open(os.path.join("new_html",outfile), "wb") as file:
        file.write(html)    