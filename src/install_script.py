#
# note that this script needs to be execute with python 2.7...
#
python_exe = "c:/python27/python.exe"

import os

try: 
    from unipath import Path
except:
    print("missing unipath:")
    print ("Trying to Install required module: unipath ")
    os.system(python_exe+' -m pip install unipath')