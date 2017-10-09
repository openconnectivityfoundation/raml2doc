#
# note that this script needs to be execute with python 2.7...
#

#python_exe=python3
python_exe="c:/python27/python.exe"

import os

try: 
    from unipath import Path
except:
    print("missing unipath:")
    print ("Trying to Install required module: unipath ")
    os.system(python_exe+' -m pip install unipath')
    
try:
    from docx import Document
except:
    print("missing spython-docx:")
    print ("Trying to Install required module: python-docx (docx)")
    os.system(python_exe+' -m pip install python-docx')
    
try:
    from yaml import CLoader
except:
    print("missing yaml:")
    print ("Trying to Install required module: pyyaml (yaml)")
    os.system(python_exe+' -m pip install pyyaml')
    
try:
    from jsonschema import _utils
except:
    print("missing jsonschema:")
    print ("Trying to Install required module: jsonschema")
    os.system(python_exe+' -m pip install jsonschema')