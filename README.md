# raml2doc
RAML to doc conversion tool

Tool to generate document section in word files from an RAML file.


## Installation raml2doc

- Install python2.7 
    - this is due to the pyraml parser, which only works with python 2.7
- Clone git repo
- Run the install script for 2.7 dependencies (in src) with python2.7 :
  - pip2.7 install -r requirements-2.7.txt



## Dependencies raml2doc

python code uses: 
- docx - 0.76 (https://python-docx.readthedocs.org/en/latest/)
  For installing python-docx use the command “pip install python-docx” or “easy_install ….”. 
  If you are using “python setup.py install” then “lxml” needs to be installed manually.

- pyraml (as part of the raml2doc tree)
based on:
(https://github.com/an2deg/pyraml-parser)

note that this package should NOT be installed, if it installed uninstall with pip2.7

pip2.7 uninstall pyraml


note that the pyramloic directory contains these changes.
- this needs unipath installed though, which is included in install.py

 
- jsonschema
pip install jsonschema
https://pypi.python.org/pypi/jsonschema
using version 2.5.1

~~
note that it might that you have to install an missing dependency package "functools32" when using python 2.7.
this can be installed with: 
pip install functools32~~

 

## Usage

usage: raml2doc.py [-h] 
(see current version for all options)

start tool:

C:\Python27\python.exe  raml2doc.py <args>

note that the resource should NOT have leading slash
example: /airqualityURI
input: airqualityURI

# how it works - word document generation
generating documentation:
-------------------------
- opens default word file (ResourceTemplate.docx)
- opens the raml file
    create parse tree of the raml file
- adds sections to the word file, using the raml parse tree
	(can use existing styles of opened word file)
- saves word file as <<>>.docx

## syntax checking
example (json) checking:
- example in the RAML are validated against the supplied schema.
- the examples and schemas are extracted from the raml parse tree.
    in case of schema if referenced in raml, the references are resolved to an actual file 
    the file is read from disk
    if the schema references schemas by means of an URL, then the validator reads and uses the referenced schema.
- schemas and referenced must be located in the same directory as the executable file (e.g. current directory)

## build in proxy

the raml2doc tool has an build in proxy
this means that the actual URLs can be used in the files.
the actual URL will be resolved on file name basis only (e.g. only the filename after an slash).
the drawback of this will be that all files needs to be in the same directory as the executable.
hence use copy commands in an batch file if other folder structures are needed.
e.g.:
http://openinterconnect.org/schemas/oic.rd.publish.json 
will be resolved to
oic.rd.publish.json 
in the local directory.
if not found in the local directory, the url will be used.


# resolve_json_schema
Python code to resolve schemas references.

The script looks for instances of $ref and replaces the tuple with the actual values.
Since the v2.0.0 version this also works for $ref with a URL as value.
e.g. uses WGET to get the file and processes it as a local file.

Note: to run the swagger generation, please run this tool to resolve all references.

## Installation resolve_json_schema

- Install python3.5 
- Run the install script for 3.5 dependencies (in src) with python3.5 :
  - pip3 install -r requirements-3.5.txt


# convert.sh script (in test folder)
script to convert an directory of RAML files to swagger2.0

usage:

convert.sh <input dir>  <output dir>


Where the <input dir> and <output dir> can be relative paths to the script.
The script needs to be run from the test folder.




# how it works - swagger generation
generating swagger:
-------------------

The swagger file is generated from the RAML + json schemas.
The swagger file is 1 file, that includes all the schema definitions.
to make this work correctly the schemas have to be 
- resolved (e.g. no external dependencies)
- no (or at least as minimal as possible) oneOff/allOf constructs
These functions are implemented with resolve_json_schema


# Issues:
- file draft3.json and/or draft4.json not found by the tool (executable)
  These files should be placed on the disk by the tool. 
  If this does not happen, then download them from the raml2doc folder and put them in the same directory as the exectuable.
  (part of github)
- placed all raml and json files in 1 directory (same dir as executable)
  this is due to that during verification the current directory is used by the tool. 
  no other directories are being searched if an include file exist.

# TODO list
 - replace proxy with direct calls
 - add mechanism to compare word output
 
 
# Fixes
- add derived modeling
- swagger2.0 generation