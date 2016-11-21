
try:
    import pyramloic.parser as ramlparser
except ImportError:
    import pyraml.parser as ramlparser
    pass


import os
import sys
import string
import traceback
import getopt
import argparse

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree


# fix for py2exe
from jsonschema import _utils

import json

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper, SafeDumper


draft3schemafile = """{
    "$schema": "http://json-schema.org/draft-03/schema#",
    "dependencies": {
        "exclusiveMaximum": "maximum",
        "exclusiveMinimum": "minimum"
    },
    "id": "http://json-schema.org/draft-03/schema#",
    "properties": {
        "$ref": {
            "format": "uri",
            "type": "string"
        },
        "$schema": {
            "format": "uri",
            "type": "string"
        },
        "additionalItems": {
            "default": {},
            "type": [
                {
                    "$ref": "#"
                },
                "boolean"
            ]
        },
        "additionalProperties": {
            "default": {},
            "type": [
                {
                    "$ref": "#"
                },
                "boolean"
            ]
        },
        "default": {
            "type": "any"
        },
        "dependencies": {
            "additionalProperties": {
                "items": {
                    "type": "string"
                },
                "type": [
                    "string",
                    "array",
                    {
                        "$ref": "#"
                    }
                ]
            },
            "default": {},
            "type": [
                "string",
                "array",
                "object"
            ]
        },
        "description": {
            "type": "string"
        },
        "disallow": {
            "items": {
                "type": [
                    "string",
                    {
                        "$ref": "#"
                    }
                ]
            },
            "type": [
                "string",
                "array"
            ],
            "uniqueItems": true
        },
        "divisibleBy": {
            "default": 1,
            "exclusiveMinimum": true,
            "minimum": 0,
            "type": "number"
        },
        "enum": {
            "minItems": 1,
            "type": "array",
            "uniqueItems": true
        },
        "exclusiveMaximum": {
            "default": false,
            "type": "boolean"
        },
        "exclusiveMinimum": {
            "default": false,
            "type": "boolean"
        },
        "extends": {
            "default": {},
            "items": {
                "$ref": "#"
            },
            "type": [
                {
                    "$ref": "#"
                },
                "array"
            ]
        },
        "format": {
            "type": "string"
        },
        "id": {
            "format": "uri",
            "type": "string"
        },
        "items": {
            "default": {},
            "items": {
                "$ref": "#"
            },
            "type": [
                {
                    "$ref": "#"
                },
                "array"
            ]
        },
        "maxDecimal": {
            "minimum": 0,
            "type": "number"
        },
        "maxItems": {
            "minimum": 0,
            "type": "integer"
        },
        "maxLength": {
            "type": "integer"
        },
        "maximum": {
            "type": "number"
        },
        "minItems": {
            "default": 0,
            "minimum": 0,
            "type": "integer"
        },
        "minLength": {
            "default": 0,
            "minimum": 0,
            "type": "integer"
        },
        "minimum": {
            "type": "number"
        },
        "pattern": {
            "format": "regex",
            "type": "string"
        },
        "patternProperties": {
            "additionalProperties": {
                "$ref": "#"
            },
            "default": {},
            "type": "object"
        },
        "properties": {
            "additionalProperties": {
                "$ref": "#",
                "type": "object"
            },
            "default": {},
            "type": "object"
        },
        "required": {
            "default": false,
            "type": "boolean"
        },
        "title": {
            "type": "string"
        },
        "type": {
            "default": "any",
            "items": {
                "type": [
                    "string",
                    {
                        "$ref": "#"
                    }
                ]
            },
            "type": [
                "string",
                "array"
            ],
            "uniqueItems": true
        },
        "uniqueItems": {
            "default": false,
            "type": "boolean"
        }
    },
    "type": "object"
}
"""

draft4schemafile = """{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "default": {},
    "definitions": {
        "positiveInteger": {
            "minimum": 0,
            "type": "integer"
        },
        "positiveIntegerDefault0": {
            "allOf": [
                {
                    "$ref": "#/definitions/positiveInteger"
                },
                {
                    "default": 0
                }
            ]
        },
        "schemaArray": {
            "items": {
                "$ref": "#"
            },
            "minItems": 1,
            "type": "array"
        },
        "simpleTypes": {
            "enum": [
                "array",
                "boolean",
                "integer",
                "null",
                "number",
                "object",
                "string"
            ]
        },
        "stringArray": {
            "items": {
                "type": "string"
            },
            "minItems": 1,
            "type": "array",
            "uniqueItems": true
        }
    },
    "dependencies": {
        "exclusiveMaximum": [
            "maximum"
        ],
        "exclusiveMinimum": [
            "minimum"
        ]
    },
    "description": "Core schema meta-schema",
    "id": "http://json-schema.org/draft-04/schema#",
    "properties": {
        "$schema": {
            "format": "uri",
            "type": "string"
        },
        "additionalItems": {
            "anyOf": [
                {
                    "type": "boolean"
                },
                {
                    "$ref": "#"
                }
            ],
            "default": {}
        },
        "additionalProperties": {
            "anyOf": [
                {
                    "type": "boolean"
                },
                {
                    "$ref": "#"
                }
            ],
            "default": {}
        },
        "allOf": {
            "$ref": "#/definitions/schemaArray"
        },
        "anyOf": {
            "$ref": "#/definitions/schemaArray"
        },
        "default": {},
        "definitions": {
            "additionalProperties": {
                "$ref": "#"
            },
            "default": {},
            "type": "object"
        },
        "dependencies": {
            "additionalProperties": {
                "anyOf": [
                    {
                        "$ref": "#"
                    },
                    {
                        "$ref": "#/definitions/stringArray"
                    }
                ]
            },
            "type": "object"
        },
        "description": {
            "type": "string"
        },
        "enum": {
            "minItems": 1,
            "type": "array",
            "uniqueItems": true
        },
        "exclusiveMaximum": {
            "default": false,
            "type": "boolean"
        },
        "exclusiveMinimum": {
            "default": false,
            "type": "boolean"
        },
        "format": {
            "type": "string"
        },
        "id": {
            "format": "uri",
            "type": "string"
        },
        "items": {
            "anyOf": [
                {
                    "$ref": "#"
                },
                {
                    "$ref": "#/definitions/schemaArray"
                }
            ],
            "default": {}
        },
        "maxItems": {
            "$ref": "#/definitions/positiveInteger"
        },
        "maxLength": {
            "$ref": "#/definitions/positiveInteger"
        },
        "maxProperties": {
            "$ref": "#/definitions/positiveInteger"
        },
        "maximum": {
            "type": "number"
        },
        "minItems": {
            "$ref": "#/definitions/positiveIntegerDefault0"
        },
        "minLength": {
            "$ref": "#/definitions/positiveIntegerDefault0"
        },
        "minProperties": {
            "$ref": "#/definitions/positiveIntegerDefault0"
        },
        "minimum": {
            "type": "number"
        },
        "multipleOf": {
            "exclusiveMinimum": true,
            "minimum": 0,
            "type": "number"
        },
        "not": {
            "$ref": "#"
        },
        "oneOf": {
            "$ref": "#/definitions/schemaArray"
        },
        "pattern": {
            "format": "regex",
            "type": "string"
        },
        "patternProperties": {
            "additionalProperties": {
                "$ref": "#"
            },
            "default": {},
            "type": "object"
        },
        "properties": {
            "additionalProperties": {
                "$ref": "#"
            },
            "default": {},
            "type": "object"
        },
        "required": {
            "$ref": "#/definitions/stringArray"
        },
        "title": {
            "type": "string"
        },
        "type": {
            "anyOf": [
                {
                    "$ref": "#/definitions/simpleTypes"
                },
                {
                    "items": {
                        "$ref": "#/definitions/simpleTypes"
                    },
                    "minItems": 1,
                    "type": "array",
                    "uniqueItems": true
                }
            ]
        },
        "uniqueItems": {
            "default": false,
            "type": "boolean"
        }
    },
    "type": "object"
}
"""

try:
    from jsonschema import Draft4Validator
    from jsonschema import ValidationError
except:
    #os.mkdir('./jsonschema/schema/')
    f = open("draft3.json","w")
    f.write(draft3schemafile)
    f.close()
    f = open("draft4.json","w")
    f.write(draft4schemafile)
    f.close()
    from jsonschema import Draft4Validator


class CreateDoc(object):
    def __init__(self, name, docxName=None, resourceName=None):
        self.inputname = name
        self.resourcedoc = "ResourceTemplate.docx"
        if docxName is not None:
            if os.path.isfile(docxName):
                self.resourcedoc = docxName
            else:
                print "WARNING: could not find file:", docxName
                print "using:", self.resourcedoc
        self.resourceout = name + ".docx"
        self.tab = "  "
        self.ResourceName = resourceName
        self.schema_ignorelist = ['required','$schema','type', 'definitions','description',
            'properties',":",":{","minItems","attribute","format","allOf", "$ref", "enum",
            "title", "oneOf", "anyOf","additionalProperties", "items", "default", "minitems","maxitems",
            "minimum", "maximum", "pattern", "readOnly", "minProperties", "additionalItems"]
        self.schema_types = ['boolean','array', 'object', 'enum', 'number', 'string']
    
    def listResource(self, level, resource, obj):
        #function to list the CRUDN behavior per resource
        # e.g. it adds an entry to the CRUDN table

        if obj is None:
            return

        #if level ==0:
        #text = "Resource List  of "+ resource
        #p = self.document.add_paragraph(text, style='fighead2')

        row_cells = self.table.add_row().cells
        #row_cells[0].text = resource
        row_cells[0].text = resource
        if obj.methods != None:
            for method, mobj in obj.methods.items():
                #print "Method:",method
                #PUT == Create
                if method == "put":
                    row_cells[1].text = method
                # GET = Read
                if method == "get":
                    row_cells[2].text = method
                # POST - update  (agreed on 05/02/2015)
                if method == "post":
                    row_cells[3].text = method
                # DELETE = Delete
                if method == "delete":
                    row_cells[4].text = method
                # NOTIFY = NOTIFY (does not exist)
                if method == "notify":
                    row_cells[5].text = method

        for nResName, nObj in obj.resources.items():
            self.listResource(level+1, nResName, nObj)


    def listResourcesCRUDN(self, parsetree, selectResource=None):
        # function to create the CRUDN table
        level = 0

        #text = "CRUDN behaviour of " + self.title+"."
        #p = self.document.add_paragraph(text, style='TABLEHEADER')

        # create the table
        self.table = self.document.add_table(rows=1, cols=6, style='TABLE-A')
        hdr_cells = self.table.rows[0].cells
        hdr_cells[0].text = 'Resource'
        hdr_cells[1].text = 'Create'
        hdr_cells[2].text = 'Read'
        hdr_cells[3].text = 'Update'
        hdr_cells[4].text = 'Delete'
        hdr_cells[5].text = 'Notify'

        if (selectResource is None):
            # all resources
            for resource, obj in parsetree.resources.items():
                self.listResource(level, resource, obj)
        else:
            for resource, obj in parsetree.resources.items():
                # only the one of the command line
                if resource == selectResource:
                    self.listResource(level, resource, obj)



    def listDescription(self, level, resource, obj, selectResource=None):

        if obj is None:
            return

        #if level != 0:
        if obj != None:
            if obj.description != None:
                intro_text = self.removeEOLSmart(obj.description)
                self.document.add_paragraph(intro_text)
        try:
            for nResName, nObj in obj.resources.items():
                if (selectResource is None):
                    self.listDescription(level+1, nResName, nObj, selectResource)
                else:
                    if nResName == selectResource:
                        self.listDescription(level+1, nResName, nObj, selectResource)
        except:
            pass

    def listDescriptions(self, parsetree, selectResource=None):
        level = 0

        if selectResource is None:
            for resource, obj in parsetree.resources.items():
                self.listDescription(level, resource, obj)
        else:
            for resource, obj in parsetree.resources.items():
                if selectResource == resource:
                    self.listDescription(level, resource, obj)


    def listURI(self, level, resource, obj):

        if resource != None:
            self.document.add_paragraph(resource)

        try:
            for nResName, nObj in obj.resources.items():
                self.listURI(level+1, nResName, nObj)
        except:
            pass

    def listURIs(self, parsetree, selectResource=None):
        level = 0

        if selectResource is None:
            for resource, obj in parsetree.resources.items():
                self.listURI(level, resource, obj)
        else:
            for resource, obj in parsetree.resources.items():
                if selectResource == resource:
                    self.listURI(level, resource, obj)



    def listXResource(self, level, resource, obj, selectResource=None):

        #print "listResource ", level, " ", resource
        if obj is None:
            return

        try:
            for nResName, nObj in obj.resources.items():
                self.listXResource(level+1, nResName, nObj, selectResource)
        except:
            pass


    def listXResources(self, parsetree):
        for resource, obj in parsetree.resources.items():
             self.listXResource(0, resource, obj)


    def getDisplayNameResources(self, parsetree, resourceName):
        for resource, obj in parsetree.resources.items():
             if resource == resourceName:
                #print "getDisplayNameResources:", resource, resourceName
                return obj.displayName


    def getRTLine(self, input_lines):
        # retrieve rt from the example
        my_input_lines = input_lines.replace(" ", "")
        lines = my_input_lines.splitlines()
        for line in lines:
            tokens = line.split('"')
            if len(tokens) >= 4:
                if tokens[1] == "rt":
                    #print "getRTLine: rt = ", tokens[3]
                    return tokens[3]
        #print "getRTLine",input_lines
        return None


    def getRTResources(self, parsetree, resourceName):
        # find an example in any body.

        for resource, obj in parsetree.resources.items():
             if resource == resourceName:
                for method, mobj in obj.methods.items():
                    #print type(mob
                    if mobj.responses is not None:
                        for resName, res in mobj.responses.items():
                            for sName, _body in res.body.items():
                                #print "getRTResources",sName
                                if sName == "application/json":
                                    value = self.getRTLine(_body.example)
                                    if value is not None:
                                        return value
                                    else:
                                        print "getRTResources ERROR: no RT found in:",_body.example
        return None



    def parseSchemaRequires(self, inputStringSchema):
        # find the required property list
        ignorelist = ['required','[',']', ',',': [']
        linesSchema = inputStringSchema.splitlines()
        length = len(linesSchema)
        requiredprops = []
        for x in range(0, length-1):
            # parse a line in a schema
            tokens = linesSchema[x].split('"')
            if len(tokens) > 1:
                if tokens[1] == 'required':
                   #print "parseSchemaRequires",tokens
                   for token in tokens:
                        if token == "]":
                           print "correct end of required detected"
                        if token not in ignorelist:
                           if " " not in token:
                              requiredprops.append(token)
        return requiredprops

    def parseSchemaLine(self, inputString, inputString2, inputString3, inputString4, requiredproperties):
        # parse a line in a schema
        # to get the property, type and description
        # put the found result in the attribute table
        tokens = inputString.split('"')
        tokens2 = inputString2.split('"')
        tokens3 = inputString3.split('"')
        tokens4 = inputString4.split('"')
        if len(tokens) > 1:
            if " " not in tokens[1]:
                if len(tokens) > 5:
                    if tokens[1] not in self.schema_ignorelist:
                        row_cells = self.tableAttribute.add_row().cells
                        row_cells[0].text = tokens[1]
                        if tokens[1] in requiredproperties:
                            row_cells[2].text = "yes"

                        if tokens[3] == "type":
                           row_cells[1].text = tokens[3]
                        if tokens[3] in self.schema_types:
                           #print "XXXXXXX", tokens
                           row_cells[1].text = tokens[3]
                           #row_cells[0].text = tokens[2]
                        if tokens[3] == "enum":
                           row_cells[1].text = tokens[3]
                        else:
                            # ignore descriptions of enums, for now...
                            if len(tokens) > 7:
                                # everything on the same line
                                row_cells[4].text = tokens[7]
                                if "ReadOnly" in tokens[7]:
                                    row_cells[3].text = "Read Only"
                                else:
                                    row_cells[3].text = "Read Write"
                            else:
                                # description on the next line
                                if len(tokens2) > 3:
                                    if tokens2[1] == "description":
                                        row_cells[4].text = tokens2[3]
                                        if "ReadOnly" in tokens2[3]:
                                            row_cells[3].text = "Read Only"
                                            # truncate and first letter uppercase
                                            description_text = tokens2[3][10:]
                                            #print description_text
                                            if len(description_text) > 0:
                                               if description_text[0].isupper() == False:
                                                description_text= description_text.title()
                                            # overwrite text
                                            row_cells[4].text = description_text
                                        else:
                                            row_cells[3].text = "Read Write"

                        #row_cells[2].text =
                        #print tokens[1]
                else:
                    if tokens[1] not in self.schema_ignorelist:
                      if " " not in tokens[1]:
                        if "oic." not in tokens[1] :
                            # terrible hack to remove the object class
                            count = len(tokens)
                            ignore = False
                            if count > 3:
                                if "http://" in tokens[3]:
                                    ignore = True

                            if "id" == tokens[1] and ignore == True:
                                # ignore the id for the schema...
                                pass
                            else:
                                row_cells = self.tableAttribute.add_row().cells
                                row_cells[0].text = tokens[1]
                                if tokens[1] in requiredproperties:
                                    row_cells[2].text = "yes"
                                if len(tokens2) > 3:
                                     # handling of line 2: expecting only type/enum info
                                    if tokens2[1] == "type":
                                        row_cells[1].text = tokens2[3]
                                    if tokens2[1] == "enum":
                                        row_cells[1].text = "enum"
                                if len(tokens2) == 3:
                                    # variable is an object..
                                    if tokens2[1] == "oneOf":
                                        row_cells[1].text = "object"
                                if len(tokens3) > 3:
                                    # description on line 3...
                                    if tokens3[1] == "description":
                                        row_cells[4].text = tokens3[3]
                                        if "ReadOnly" in tokens3[3]:
                                            row_cells[3].text = "Read Only"
                                            # truncate and first letter uppercase
                                            description_text = tokens3[3][10:]
                                            if len(description_text) > 0:
                                              if description_text[0].isupper() == False:
                                                description_text= description_text.title()
                                            # overwrite text
                                            row_cells[4].text = description_text
                                        else:
                                            row_cells[3].text = "Read Write"
                                if len(tokens4) > 3:
                                    # description on line 4...
                                    if len(tokens4) > 3:
                                        if tokens4[1] == "description":
                                            row_cells[4].text = tokens4[3]
                                            if "ReadOnly" in tokens4[3]:
                                                row_cells[3].text = "Read Only"
                                                # truncate and first letter uppercase
                                                description_text = tokens4[3][10:]
                                                if len(description_text) > 0:
                                                  if description_text[0].isupper() == False:
                                                    description_text= description_text.title()
                                                # overwrite text
                                                row_cells[4].text = description_text
                                            else:
                                               row_cells[3].text = "Read Write"


    def parseSchema(self, inputStringSchema):
        requiredprops = self.parseSchemaRequires(inputStringSchema)
        print "parseSchema: required properties found:",requiredprops
        linesSchema = inputStringSchema.splitlines()
        length = len(linesSchema)
        for x in range(0, length-4):
            self.parseSchemaLine(linesSchema[x],linesSchema[x+1],linesSchema[x+2],linesSchema[x+3],requiredprops)
        # make sure that the remaining lines are also processed.
        self.parseSchemaLine(linesSchema[length-3],linesSchema[length-2],linesSchema[length-1],"",requiredprops)
        self.parseSchemaLine(linesSchema[length-2],linesSchema[length-1],"","",requiredprops)

    def listAtribute(self, level, resource, obj):
        # list all attributes of an indicated resource
        if obj is None:
            print "EMPTY EMPTY"
            return

        if level != 0:
            if obj.methods != None:
                for method, mobj in obj.methods.items():
                    # default method get...
                    if method == self.table_method:
                        # print "dddd", method, self.table_method
                        for resName, res in mobj.responses.items():
                            if resName == 200:
                                for sName, body in res.body.items():
                                    if sName == "application/json":
                                        text = body.schema
                                        if len(body.schema) > 50:
                                            # we think this is the full schema..
                                            self.parseSchema(body.schema)
                                        else:
                                            # we think this is a reference.
                                            # find it and include it.
                                            filename  = self.schemaRef2Filename(body.schema)
                                            print "resolve schema reference:",body.schema, filename
                                            # read the file as a string
                                            try:
                                              #print "XXXXXXXXXXXX listAtribute reading schema file:", filename
                                              linestring = open(filename, 'r').read()
                                              # create the table with contents..
                                              self.parseSchema(linestring)
                                            except:
                                                print "could not open file:", filename
        for nResName, nObj in obj.resources.items():
            self.listAtribute(level+1, nResName, nObj)

    def listAtributes(self, parsetree, selectResource=None):

        #text = "Attributes of " + self.title+"."
        #+ resource
        #p = self.document.add_paragraph(text, style='TABLEHEADER')

        self.tableAttribute = self.document.add_table(rows=1, cols=5, style='TABLE-A')
        hdr_cells = self.tableAttribute.rows[0].cells
        hdr_cells[0].text = 'Property name'
        hdr_cells[1].text = 'Value type'
        hdr_cells[2].text = 'Mandatory'
        hdr_cells[3].text = 'Access mode'
        hdr_cells[4].text = 'Description'

        level = 1

        if selectResource == None:
            for resource, obj in parsetree.resources.items():
                self.listAtribute(level, resource, obj)
        else:
            for resource, obj in parsetree.resources.items():
                if resource == selectResource:
                    self.listAtribute(level, resource, obj)

        if self.sensor_switch == True:
            # auto generate the sensor value data..
            row_cells = self.tableAttribute.add_row().cells
            row_cells[0].text = "value"
            row_cells[1].text = "boolean"
            row_cells[2].text = "yes"
            row_cells[3].text = "Read Only"
            row_cells[4].text = "True = Sensed, False = Not Sensed."

        if self.schema_switch == True:
            # add values from external schema.
            for schema_file in self.schema_files:
                linestring = open(schema_file, 'r').read()
                # add fields in table with contents..
                self.parseSchema(linestring)


    def removeEOLSmart(self, inputString):
        # removes all EOL of the input string
        # needed for Introduction
        retstring = ""
        lines = inputString.splitlines()
        for line in lines:
            # add behind the added line an space
            retstring = retstring +line + " "
        return retstring

    def addjustificationSmart(self, depth, inputString):
        # add the spaces for an correct indentation of the generated RAML code section
        # for descriptions in the RAML definitions
        retstring = ""
        all_lines = inputString.splitlines()
        for xline in all_lines:
            lines = xline.split(". ")
            for line in lines:
                string1 = depth + line + "\n"
                if len(line) > 0:
                   retstring = retstring + string1
        return retstring

    def addjustification(self, depth, inputString):
        # add the spaces for an correct indentation of the generated RAML code section
        # needed for schema and code
        retstring = ""
        lines = inputString.splitlines()
        for line in lines:
            string1 = depth + line + "\n"
            #os.linesep
            retstring = retstring + string1
        return retstring


    def printBodies(self, depth, bodies):
        # function to loop over the bodies in an method
        if bodies is not None:
            for bName, body in bodies.items():
                self.printBody(depth, bName, body)

    def printPOSTPUTBody(self, depth, bName, body):
        # hack for parse tree in put/post
        tdepth = depth + self.tab
        ttdepth = tdepth + self.tab
        tttdepth = ttdepth + self.tab
        p = self.document.add_paragraph(depth + "body:", style='CODE-AQUA' )
        post_txt = tdepth + "application/json" + ":"
        p = self.document.add_paragraph(post_txt, style='CODE-AQUA' )

        self.printBody(tdepth, bName, body)


    def validate_raml_cop (self, schemafilename, jsonfile, jsonstring):
       import subprocess
       print "validating ",jsonfile," with ",schemafilename
       #print "validating json string ===="
       #print jsonstring
       print  "==> raml_cop: validation start:"
       mycmd = "jsonlint "+jsonfile+" -V "+schemafilename

       try:
            retcode = os.system(mycmd)
       except OSError, e:
            print >>sys.stderr, "Execution failed:", e

       print  "==> raml_cop: validation complete"

    def printBody(self, depth, bName, body):
        tdepth = depth + self.tab
        ttdepth = tdepth + self.tab
        tttdepth = ttdepth + self.tab
        writedepth = tdepth
        filename = ""

        if body.schema is None:
            return
        if body.schema != None:
            if bName is not "":
                p = self.document.add_paragraph(tdepth + "body:", style='CODE-AQUA' )
                method_txt = ttdepth + bName + ":"
                p = self.document.add_paragraph(method_txt, style='CODE-AQUA' )
                writedepth = tttdepth

            # schema :
            p = self.document.add_paragraph(writedepth + "schema", style='CODE-GREY')
            p.add_run(": |", style='CODE-GREY')
            # schema itself
            schema_text = body.schema
            if len(schema_text) < 50:
                # we think this is a reference.
                # find it and include it.
                try:
                   filename  = self.schemaRef2Filename(body.schema)
                   print "resolve schema reference:",body.schema, filename
                   # read the file as a string
                   schema_text = open(filename, 'r').read()
                except:
                   print "ERROR ==========> could not resolve schema", body.schema

            try:
                par = self.document.add_paragraph( self.addjustification(writedepth + self.tab, schema_text), style='CODE-BLACK' )
                par.alignment = WD_ALIGN_PARAGRAPH.LEFT
            except:
               print "failure in (schema):", schema_text

        if body.example != None:
            #print depth, "example: |"
            #print self.addjustification(writedepth + self.tab ,body.example)

            try:
                #print "dumping json as parse validation"
                json_data = json.loads(body.example)
                #print(json.dumps(json_data, indent=2))
                #print "end dumping json"
            except:
                print "failure in (json):", body.example


            try:
                p = self.document.add_paragraph(writedepth + "example" , style='CODE-GREY')
                p.add_run(": |", style='CODE-GREY')
                par = self.document.add_paragraph( self.addjustification(writedepth + self.tab, body.example), style='CODE-BLACK')
                par.alignment = WD_ALIGN_PARAGRAPH.LEFT
            except:
                print "failure in (body example):", body.example

            try:
                # check based on https://www.npmjs.com/package/jsonlint
                f= open("temp.json",'wb')
                f.write(body.example)
                f.close()
                #self.validate(filename,"temp.json")
            except:
                print "failure in validating (not executed)(body example):", body.example
            self.validate_raml_cop(filename,"temp.json", body.example)
            #self.printHeader(depth,body.headers)


            try:
                # validation by using package:
                #https://pypi.python.org/pypi/jsonschema
                print "xx=> validation schema (jsonschema)"
                schema_string = body.schema
                if len(body.schema) < 50:
                    # we think this is a reference.
                    # find it and include it.
                    filename  = self.schemaRef2Filename(body.schema)
                    print "resolve schema reference:", body.schema, filename
                    # read the file as a string
                    try:
                        schema_string = open(filename, 'r').read()
                    except:
                        print "error trying to open file:", filename

                v_schema = None
                v_example = None
                valiation_error = False
                try:
                    v_schema =json.loads(schema_string)
                except ValueError as ex:
                    valiation_error = True
                    print "error with loading schema:"
                    print  ex
                try:
                    v_example =json.loads(body.example)
                except ValueError as ex:
                    valiation_error = True
                    print "error with loading example:"
                    print  ex

                # Lazily report all errors in the instance
                valiation_error = False
                try:
                    v = Draft4Validator(v_schema)
                    for error in sorted(v.iter_errors(v_example), key=str):
                        valiation_error = True
                        print(error.message)
                        print(error)

                except ValidationError as e:
                    valiation_error = True
                    print "validation failed:"
                    print (e.message)

                    for error in sorted(v.iter_errors(v_example), key=str):
                        valiation_error = True
                        print(error.message)
                        print(error)


                if valiation_error is True:
                    print "validation failed, input information:"
                    print "body (json):"
                    print body.example
                    print  ""
                    print "schema (json):"
                    print  schema_string
                else:
                    print "xx=xx=> schema & json VALID"

                #validate (v_example, v_schema, cls=Draft4Validator)
            except:
                #print "jsonschema installed?"
                #print "pip install jsonschema"
                print  ""
                print "failure in body (json):"
                print body.example
                print  ""
                print "schema (json):"
                print schema_string
                print  ""
                traceback.print_exc()
                #print  ""

            print "xxx=> validation schema (jsonschema) done"


    def printHeader(self, depth, Headers):
        try:
            for hName, Header in Headers.item():
                print depth,"headername:",hName
                print depth,"headertype:",Header.type
        except:
            pass

    def printResponse(self, depth, response):
        """
        prints a response object

        :param depth: depth in the tree
        :param response: RamlResponse

        """
        tdepth = depth + self.tab
        ttdepth = tdepth + self.tab
        tttdepth = ttdepth + self.tab

        if response is None:
            return

        for resName, res in response.items():

            if resName != None:
                self.document.add_paragraph(tdepth + str(resName) +":", style='CODE-BLUE')

            if res.description is not None:
                self.printDescription(ttdepth, res.description)

            if res.schema is not None:
                p = self.document.add_paragraph(ttdepth + "schema ", style='CODE-AQUA' )
                p.add_run(": |", style='CODE-YELLOW')
                par = self.document.add_paragraph( self.addjustification(tttdepth, res.schema) )
            if res.example is not None:
                self.document.add_paragraph(ttdepth + "example", style='CODE-AQUA')
                p.add_run(": |", style='CODE-YELLOW')
                par = self.document.add_paragraph( self.addjustification(tttdepth, res.example) )

            self.printHeader(tdepth, res.headers)
            self.printBodies  (tdepth, res.body)

    def printDescription(self, depth, description_txt):
        if description_txt is not None:
            par = self.document.add_paragraph(depth + "description: |", style='CODE-YELLOW')
            adjusted_text = self.addjustificationSmart(depth + self.tab, description_txt)
            par = self.document.add_paragraph(adjusted_text, style='CODE-YELLOW')
            par.italic = True


    def list2array(self,inputlist):
        # generates an raml string representation of an python list
        string = "["
        for x in inputlist:
            comma =", "
            string=string + '"'+x+'"'+ comma
        # remove last comman (e.g. last 2 chars)
        sizeofstring = len(string)
        string = string[:-2]
        string = string + "]"
        #print "list:",string
        return string


    def list2string(self,inputlist):
        # generates an raml string representation of an python list
        string = ""
        for x in inputlist:
            string=string +x
        return string

    def printTraitQueryParam(self, depth, queryparams):
        tdepth = depth + self.tab
        ttdepth = tdepth + self.tab
        tttdepth = ttdepth + self.tab
        if queryparams is not None:
            #print "adding treat......"
            par = self.document.add_paragraph(depth + "queryParameters: ", style='CODE-AQUA')
            for query_name,qobj in queryparams.items():
                qtext = tdepth + query_name+":"
                #print "adding treat..q..", qtext
                p = self.document.add_paragraph(qtext, style='CODE-BLUE')
                for name, obj in qobj.items():
                    nametext = ""
                    if name == "enum":
                        # list as an array
                        nametext = nametext + ttdepth +name+": " + self.list2array(obj)
                    else:
                        # list as an string
                        nametext = nametext + ttdepth +name+": " + self.list2string(obj)
                    #print "adding treat..name..", nametext
                    p = self.document.add_paragraph(nametext, style='CODE-BLUE')
        #else:
        #    print "printTraitQueryParam: queryparams",queryparams

    def printQueryParam(self, depth, queryparams):
        tdepth = depth + self.tab
        ttdepth = tdepth + self.tab
        tttdepth = ttdepth + self.tab
        if queryparams is not None:
            par = self.document.add_paragraph(depth + "queryParameters: ", style='CODE-AQUA')
            for query_name,qobj in queryparams.items():
                nametext = tdepth + query_name+":"
                p = self.document.add_paragraph(nametext, style='CODE-BLUE')
                if qobj.enum is not None:
                    enumtext = nametext = ttdepth +"enum: " + self.list2string(qobj.enum)
                    p = self.document.add_paragraph(nametext, style='CODE-BLUE')
                if qobj.type is not None:
                    enumtext = nametext = ttdepth +"type: " + self.list2string(qobj.type)
                    p = self.document.add_paragraph(nametext, style='CODE-BLUE')
                if qobj.description is not None:
                    enumtext = nametext = ttdepth +"description: " + self.list2string(qobj.description)
                    p = self.document.add_paragraph(nametext, style='CODE-YELLOW')
                if qobj.required is not None:
                    if qobj.required == True:
                        enumtext = nametext = ttdepth +"required: true"
                    else:
                        enumtext = nametext = ttdepth +"required: false"
                    p = self.document.add_paragraph(nametext, style='CODE-BLUE')
                if qobj.example is not None:
                    enumtext = nametext = ttdepth +"example: " + self.list2string(qobj.example)
                    p = self.document.add_paragraph(nametext, style='CODE-GREY')


    def printIS_(self, depth, is_):
        # print the is string in the RAML definition.. this on resource level
        if is_ is not None:
            my_string = depth+"is : ["
            for is_name in is_:
                temp = "'"+is_name+"',"
                my_string = my_string + temp
            strsize = len(my_string)

            my_string = my_string[:-1]
            my_string = my_string + "]"
            p = self.document.add_paragraph(my_string,style='CODE-BLUE')

    def printResource(self, depth, resource, obj):
        tdepth = depth + self.tab
        ttdepth = tdepth + self.tab
        tttdepth = ttdepth + self.tab

        if obj is None:
            return

        resource_text = depth + resource + ":"
        #print "XXXXXXXXXXXXXXXXXXXX", resource_text
        p = self.document.add_paragraph(resource_text, style='CODE-BLUE')
        try:
            if obj.description is not None:
                self.printDescription(tdepth, obj.description)
        except:
            pass
        #try:
            #if obj.queryParameters is not None:
                #self.printQueryParam(tdepth, obj.queryParameters)
        #except:
            #pass
        try:
            if obj.is_ is not None:
                self.printIS_(tdepth, obj.is_)
        except:
            pass

        if obj.methods != None:
            for method, mobj in obj.methods.items():
                # RamlMethod
                method_txt = tdepth + method + ":"
                #print "SSSSSSSSSSS", method_txt
                p = self.document.add_paragraph(method_txt, style='CODE-AQUA')

                # description on method level
                if mobj.description is not None:
                    self.printDescription(ttdepth, mobj.description)

                # print the query parameters
                if mobj.queryParameters is not None:
                    self.printQueryParam(ttdepth, mobj.queryParameters)

                # print the body
                if mobj.body is not None:
                    self.printPOSTPUTBody(ttdepth, "", mobj.body)

                # print the response header of the method
                p = self.document.add_paragraph(ttdepth + "responses :", style='CODE-AQUA')
                # print the different responses
                self.printResponse(ttdepth, mobj.responses)

            # recurse...
            depth = depth + self.tab
            for nResName, nObj in obj.resources.items():
                self.printResource(depth, nResName, nObj)

    def printTrait(self, depth, TraitName, obj):
        tdepth = self.tab
        # one extra, due to array item indicator -
        ttdepth = "   " + self.tab
        trait_string = " - "+ TraitName + " :"
        p = self.document.add_paragraph(trait_string, style='CODE-AQUA')
        #print "printTrait: query param", obj.queryParameters
        self.printTraitQueryParam(ttdepth, obj.queryParameters)

    def printTraits(self, depth, parsetree ):
        traits = parsetree.traits
        # function to loop over the bodies in an method
        try:
            if len(traits.items()) > 0:
                p = self.document.add_paragraph("traits:", style='CODE-AQUA')
            # todo first trait needs a - to indicate it is an array...
            for traitname, obj in traits.items():
                self.printTrait(self.tab, traitname, obj)
        except:
            print "no traits found!!"
            pass


    def generateSections(self, parsetree , sectionName=None):
        # generate the individual sections

        # just plain output
        TitleName = parsetree.title
        if sectionName is not None:
            TitleName = sectionName
            displayName = self.getDisplayNameResources(parsetree, sectionName)
            self.displayName = displayName
            print "DisplayName:", displayName
            if displayName is not None:
                TitleName = displayName
        print "Title", TitleName
        self.title = TitleName

        print "RT = ",self.getRTResources(parsetree, sectionName)


        # section Resource name
        par = self.document.add_heading(TitleName, level=2)
        if self.annex_switch == True:
            par.style = 'ANNEX-heading1'
        # section introduction
        par = self.document.add_heading('Introduction', level=3)
        if self.annex_switch == True:
            par.style = 'ANNEX-heading2'
        self.listDescriptions(parsetree, selectResource=sectionName)

        # section URI
        if self.annex_switch == False:
            par = self.document.add_heading('Example URI', level=3)
        else:
            par = self.document.add_heading('Wellknown URI', level=3)
        if self.annex_switch == True:
            par.style = 'ANNEX-heading2'
        self.listURIs(parsetree, selectResource=sectionName)

        # section RT
        par = self.document.add_heading('Resource Type', level=3)
        if self.annex_switch == True:
            par.style = 'ANNEX-heading2'
        RTName = self.getRTResources(parsetree, sectionName)
        if RTName is not None:
            text = "The resource type (rt) is defined as: "+ RTName + "."
            p = self.document.add_paragraph(text)
        else:
            print "RT not found!"

        # section RAML definition
        par = self.document.add_heading('RAML Definition', level=3)
        if self.annex_switch == True:
            par.style = 'ANNEX-heading2'

        #self.document.add_section()
        self.document.add_paragraph("#%RAML 0.8", style='CODE-GREEN')
        p = self.document.add_paragraph("title: ", style='CODE-YELLOW')
        p.add_run(parsetree.title).italic = True
        p = self.document.add_paragraph("version: ", style='CODE-YELLOW')
        version_text = str(parsetree.version)
        p.add_run(version_text).italic = True


        self.printTraits("", parsetree)
        # add schema references
        #print parsetree.schema

        self.document.add_paragraph("")
        for resource, obj in parsetree.resources.items():
            if sectionName == None:
                self.printResource("", resource, obj)
            else:
                if sectionName == resource:
                    self.printResource("", resource, obj)

        if self.composite_switch == False:
            # do not add when the switch is true...
            # section property definition
            par = self.document.add_heading('Property Definition', level=3)
            if self.annex_switch == True:
                par.style = 'ANNEX-heading2'
            self.listAtributes(parsetree, selectResource=sectionName)

        # section CRUDN definition
        par = self.document.add_heading('CRUDN behavior', level=3)
        if self.annex_switch == True:
            par.style = 'ANNEX-heading2'
        self.listResourcesCRUDN(parsetree , selectResource=sectionName)

        if self.schema_switch == True:
            # section extra JSON definition
            par = self.document.add_heading('Referenced JSON schemas', level=3)
            if self.annex_switch == True:
                par.style = 'ANNEX-heading2'

            for schema_file in self.schema_files:
                par = self.document.add_heading(schema_file, level=4)
                if self.annex_switch == True:
                    par.style = 'ANNEX-heading2'

                schema_text = open(schema_file, 'r').read()

                try:
                    par = self.document.add_paragraph( self.addjustification("", schema_text), style='CODE-BLACK' )
                    par.alignment = WD_ALIGN_PARAGRAPH.LEFT
                except:
                    pass

        if self.schemaWT_switch == True:
            # section extra JSON definition
            par = self.document.add_heading('Referenced JSON schemas', level=3)
            if self.annex_switch == True:
                par.style = 'ANNEX-heading2'

            for schema_file in self.schemaWT_files:
                par = self.document.add_heading(schema_file, level=4)
                if self.annex_switch == True:
                    par.style = 'ANNEX-heading2'

                par = self.document.add_heading("Property Definition", level=5)
                if self.annex_switch == True:
                    par.style = 'ANNEX-heading2'

                schema_text = open(schema_file, 'r').read()

                self.tableAttribute = self.document.add_table(rows=1, cols=5, style='TABLE-A')

                hdr_cells = self.tableAttribute.rows[0].cells
                hdr_cells[0].text = 'Property name'
                hdr_cells[1].text = 'Value type'
                hdr_cells[2].text = 'Mandatory'
                hdr_cells[3].text = 'Access mode'
                hdr_cells[4].text = 'Description'

                # add fields in table with contents..
                self.parseSchema(schema_text)

                par = self.document.add_heading("Schema Definition", level=5)
                if self.annex_switch == True:
                    par.style = 'ANNEX-heading2'

                try:
                    par = self.document.add_paragraph( self.addjustification("", schema_text), style='CODE-BLACK' )
                    par.alignment = WD_ALIGN_PARAGRAPH.LEFT
                except:
                    pass


    def schemaRef2Filename(self, SchemaName):
        # convert the schema reference name into the actual filename to be read
        schemas = self.parsetree.schemas
        try:
          for item in schemas:
            for name, obj in item.items():
                if name == SchemaName:
                    return obj.file_name
        except:
            pass
        return "ERROR-IN-RESOLVING-SCHEMA:NO_FILE_FOUND_FOR:"+SchemaName

    def convert(self):

        try:
            parsetree = ramlparser.load(self.inputname)
        except ValidationError as e:
            print 'validation error:', e.errors
            #print "could not load file: error loading file"
            #traceback.print_exc()
            return

        # make it a member..
        self.parsetree = parsetree

        self.listXResources(parsetree)

        #print parsetree
        #output = dump(parsetree, Dumper=Dumper,default_flow_style=False)
        #output = dump(parsetree, Dumper=SafeDumper)
        #print output

        try:
            self.document = Document(docx=self.resourcedoc)
        except:
            print "could not load file: ", self.resourcedoc
            print "make sure that docx file exist in same directory as executable"
            return

        self.generateSections(parsetree, self.ResourceName)

        self.document.save(self.resourceout)

    def add_header(self, levelnr, headertitle):

        try:
            self.document = Document(docx=self.resourcedoc)
        except:
            print "could not load file: ", self.resourcedoc
            print "make sure that docx file exist in same directory as executable"



            return

        print "add_header: title:", headertitle
        paragraph = self.document.add_heading(headertitle, level=1)
        if self.annex_switch == True:
            paragraph.style = 'ANNEX-title'

        self.document.save(self.resourceout)

#
# code for the proxy
#
import os
import SimpleHTTPServer
import SocketServer
import threading
import urllib2

class ProxyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        filename = self.path.split('/')[-1]
        print "ProxyHandler: url:", self.path, " localfile:", filename
        if os.path.exists(filename):
            print "ProxyHandler: local file found:",filename
            self.copyfile(open(filename), self.wfile)
        else:
            filenamejson = filename + ".json"
            print "ProxyHandler: local file NOT found:", filename, " trying: ", filenamejson
            if os.path.exists(filenamejson):
                print "ProxyHandler: local file found:",filenamejson
                self.copyfile(open(filenamejson), self.wfile)
            else:
                print "ProxyHandler: trying url:",self.path
                proxy_handler = urllib2.ProxyHandler({})
                opener = urllib2.build_opener(proxy_handler)
                try:
                    req = urllib2.Request(self.path)
                    self.copyfile(opener.open(req), self.wfile)
                except:
                    print "ProxyHandler: file not found:", self.path

def proxy():
    PORT = 4321
    httpd = SocketServer.TCPServer(("", PORT), ProxyHandler)
    print "HTTPPRoxy: serving at port", PORT
    proxythread = threading.Thread(target=httpd.serve_forever)
    proxythread.setDaemon(True)
    proxythread.start()
    os.environ['http_proxy'] = 'http://localhost:%d/' % PORT
    return


if __name__ == '__main__':

    resourcedoc = "ResourceTemplate.docx"
    # set the execution path of the tool
    if hasattr(sys, 'frozen'):
        my_dir = os.path.dirname(sys.executable)
    else:
        my_dir = os.path.dirname(sys.argv[0])


    # version information
    my_version = ""
    try:
        from version import VERSION
        my_version = VERSION
    except:
        pass

    print "==================================="
    print "version: ", my_version


    #annex_switch = False

    # argument parsing
    parser = argparse.ArgumentParser(description='Process RAML files.')
    parser.add_argument('-docx','--docx', help='word template file')
    parser.add_argument('-raml','--raml', help='raml input file')
    parser.add_argument('-heading1','--heading1', help='creates an heading 1 to the document (and exit)')
    #parser.add_option('-showResources','--showResources', help='shows the resources in an RAML file')
    parser.add_argument('-resource','--resource', help='resource to be processed')

    parser.add_argument('-annex','--annex', help='uses a annex heading instead of normal heading (--annex true)')
    parser.add_argument('-put','--put', help='uses put command as property table input instead of get (--put true)')
    parser.add_argument('-composite','--composite', help='treats the resource as an composite resource, e.g. no property definition table (--composite true)')
    parser.add_argument('-sensor','--sensor', help='treats the resource as an sensor resource, e.g. add the value "value" to the property table (--sensor true)')
    parser.add_argument('-schema','--schema', nargs = '*', help='additional (referenced) schema used in the resource (--schema "schema file1" "schema file2" )')
    parser.add_argument('-schemaWT','--schemaWT', nargs = '*', help='additional (referenced) schema (section With Table) used in the resource (--schema "schema file1" "schema file2" )')

    args = vars(parser.parse_args())

    resourceName = args['resource']
    docxName = args['docx']
    ramlName = args['raml']
    header0 = args['heading1']
    annex_switch = args['annex']
    put_switch = args['put']
    composite_switch = args['composite']
    sensor_switch = args['sensor']
    schema_file = args['schema']
    schemaWT_file = args['schemaWT']

    #annex_switch = True

    if annex_switch is None:
        annex_switch = False
    else:
        annex_switch = True

    if put_switch is None:
        put_switch = False
        table_method = 'get'
    else:
        put_switch = True
        table_method = 'put'

    if composite_switch is None:
        composite_switch = False
    else:
        composite_switch = True

    if sensor_switch is None:
        sensor_switch = False
    else:
        sensor_switch = True

    if schema_file is None:
        # schema_file to be included in class
        schema_switch = False
    else:
        schema_switch = True


    if schemaWT_file is None:
        # schema_file to be included in class
        schemaWT_switch = False
    else:
        schemaWT_switch = True

    if docxName is None:
        docxName = resourcedoc


    print "==================================="
    print "using raml file              :", ramlName
    print "using docx file              :", docxName
    print "using resource               :", resourceName
    print "using header0                :", header0
    print "using annex                  :", annex_switch
    print "using put for property table :", put_switch
    print "using composite              :", composite_switch
    print "using sensor                 :", sensor_switch
    print "schema switch                :", schema_switch
    print "schema (WT) switch           :", schemaWT_switch
    if schema_switch == True:
      print "schema file                  :", schema_file
    if schemaWT_switch == True:
      print "schema (WT) file             :", schemaWT_file

    print "styles:"
    print " heading: Heading 1 or ANNEX-heading1"
    print " table style: TABLE-A"
    print " table header style: TABLEHEADER"
    print " color (code) style: CODE-AQUA"
    print "                   : CODE-YELLOW"
    print "                   : CODE-GREY"
    print "                   : CODE-BLACK"
    print "                   : CODE-BLUE"
    print "                   : CODE-GREEN"

    print "documentation section handling:"
    print " new lines are inserted in generated examples when"
    print " .<blank><EOL> are encountered"
    print " : is an reserved character and can not be used"
    print "==================================="


    temp = sys.stdout
    #sys.stdout = sys.stderr
    sys.stderr = sys.stdout

    proxy();

    if my_dir:
        os.chdir(my_dir)

    if len(sys.argv) == 1:
        parser.print_help()
        processor = None
    else:
        #try:
        #    import ramlfications
        #    print
        #    api = ramlfications.parse(ramlName)
        #except:
        #    traceback.print_exc()
        #    sys.exit()
        processor = CreateDoc(ramlName, docxName=docxName, resourceName=resourceName)


    if processor != None:
       processor.annex_switch = annex_switch
       processor.composite_switch = composite_switch
       processor.sensor_switch = sensor_switch
       processor.table_method = table_method
       processor.sensor_switch = sensor_switch
       processor.schema_switch= schema_switch
       processor.schemaWT_switch= schemaWT_switch
       if schema_switch == True:
          processor.schema_files = schema_file
       if schemaWT_switch == True:
          processor.schemaWT_files = schemaWT_file
       if header0 is not None:
          processor.add_header(0,header0)
          sys.exit()

    if processor != None:
        processor.convert()
