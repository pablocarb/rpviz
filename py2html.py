# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:15:00 2019

@author: anael
"""

import json
import jinja2

def html(file,name):
        
    templateLoader = jinja2.FileSystemLoader( searchpath="." )
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template( "file_html/template.html" )
      
    with open(file,'r') as jsonfile: #to get json information
        data=jsonfile.read()
        obj=json.loads(data)
        elements=obj['elements']
       
    templateVars = {
            "name":name,
            "elements":elements}
    
    output = template.render( templateVars )
    with open("file_html/"+name+".html", "w") as fh:
        fh.write(output)
        fh.close()