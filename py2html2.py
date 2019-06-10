# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:07:03 2019

@author: anael
"""

import json
import os
from bs4 import BeautifulSoup


def html2(jsondata,outfile):

    htmlfile= open(os.path.join("new_html","template2.html"))
    soup = BeautifulSoup(htmlfile, 'html.parser')    
        
    for key in jsondata.keys():
            name=key
            obj=json.loads(jsondata[key])
            elements=obj['elements']

            element_script=soup.find(id="elements") #select the script section containing elements
            element_script.append('\n var '+name+'='+str(elements)) #to modify
            
            form=soup.find('form')
            new_tag = soup.new_tag("input")
            new_tag["type"] = "button"
            new_tag["value"]=name
            new_tag["onclick"]="displaynet("+name+')'
            form.append(new_tag)
            
            select=soup.find(id="selectbox")
            new_tag=soup.new_tag("option")
            new_tag["value"]=str(name)
            new_tag.append(name)
            select.append(new_tag)
        
    htmlfile.close()
        
    html = soup.prettify("utf-8")
    with open(os.path.join(outfile), "wb") as file:
        file.write(html)    