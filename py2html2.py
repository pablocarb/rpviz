# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:07:03 2019

@author: anael
"""

import json

def html2(file,name):
    
    with open(file,'r') as jsonfile: #to get json information
        data=jsonfile.read()
        obj=json.loads(data)
        elements=obj['elements']
    
    with open("file_html/network_elements.js", "a") as fh:
        fh.write('\n var '+name+'='+str(elements))
        fh.close()
