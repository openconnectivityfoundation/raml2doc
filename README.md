# raml2doc
RAML to doc conversion tool

Tool to generate document section in word files from an RAMK file.

## Dependencies
python code uses: 
- python2.7 (default instalation on C:)

- docx - 0.76 (https://python-docx.readthedocs.org/en/latest/)
  For installing python-docx use the command “pip install python-docx” or “easy_install ….”. 
  If you are using “python setup.py install” then “lxml” needs to be installed manually.

- pyraml 
based on:
(https://github.com/an2deg/pyraml-parser)
but use uploaded version at:
pyraml-parser-385f952ed352fcaa9bb810de72d541767d433b09.zip
  Before installing pyraml-parser-master, “pyyaml” and “ImportHelpers” should be manually installed
 PYRAML fix
 default pyraml is installed at:
 C:\Python27\Lib\site-packages\pyraml
 the file fields.py needs to be replaced with the supplied version.
 the file entities.py needs to be replaced with the supplied version.
 the file parser.py needs to be replaced with the supplied version.

 note that the pyramloic directory contains these changes.
 
 
- jsonschema
pip install jsonschema
https://pypi.python.org/pypi/jsonschema
using version 2.5.1
note that it might that you have to install an missing dependency package "functools32" when using python 2.7.
this can be installed with: 
pip install functools32

 
# commandline

C:\Python27\python.exe  raml2doc.py <<raml.file>>


note that the resource should NOT have leading slash
example: /airqualityURI
input: airqualityURI


## Usage

usage: raml2doc.py [-h] 
(see current version for all options)

```
<<current version>>
===================================
version:  201511171441
===================================
===================================
HTTPPRoxy: serving at port 4321
usage: raml2doc [-h] [-docx DOCX] [-raml RAML] [-heading1 HEADING1]
                [-resource RESOURCE] [-annex ANNEX] [-put PUT]
                [-composite COMPOSITE] [-sensor SENSOR]
                [-schema [SCHEMA [SCHEMA ...]]]
                [-schemaWT [SCHEMAWT [SCHEMAWT ...]]]

Process RAML files.

optional arguments:
  -h, --help            show this help message and exit
  -docx DOCX, --docx DOCX
                        word template file
  -raml RAML, --raml RAML
                        raml input file
  -heading1 HEADING1, --heading1 HEADING1
                        creates an heading 1 to the document (and exit)
  -resource RESOURCE, --resource RESOURCE
                        resource to be processed
  -annex ANNEX, --annex ANNEX
                        uses a annex heading instead of normal heading
                        (--annex true)
  -put PUT, --put PUT   uses put command as property table input instead of
                        get (--put true)
  -composite COMPOSITE, --composite COMPOSITE
                        treats the resource as an composite resource, e.g. no
                        property definition table (--composite true)
  -sensor SENSOR, --sensor SENSOR
                        treats the resource as an sensor resource, e.g. add
                        the value "value" to the property table (--sensor
                        true)
  -schema [SCHEMA [SCHEMA ...]], --schema [SCHEMA [SCHEMA ...]]
                        additional (referenced) schema used in the resource
                        (--schema "schema file1" "schema file2" )
  -schemaWT [SCHEMAWT [SCHEMAWT ...]], --schemaWT [SCHEMAWT [SCHEMAWT ...]]
                        additional (referenced) schema (section With Table)
                        used in the resource (--schema "schema file1" "schema
                        file2" )
```

start tool:

C:\Python27\python.exe  raml2doc.py <args>



# how it works
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