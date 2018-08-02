#############################
#
#    copyright 2018 Open Interconnect Consortium, Inc. All rights reserved.
#    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#    1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#    2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE OPEN INTERCONNECT CONSORTIUM, INC. "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE OR WARRANTIES OF NON-INFRINGEMENT,
#    ARE DISCLAIMED. IN NO EVENT SHALL THE OPEN INTERCONNECT CONSORTIUM, INC. OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#############################


#
# generic imports
#
import re
import os
import sys
import traceback
import argparse
from os import listdir
from os.path import isfile, join
import json
from copy import deepcopy

import jsonref
import wget
   

def list_to_array(input_list):
    """
    generates an raml string representation of an python list
    :param input_list: python array
    :return: string as raml string representation. example = "[ 'blah', 'blah2' ]"
    """
    my_string = "["
    if input_list is not None:
        for x in input_list:
            comma = ", "
            my_string = my_string + '"' + x + '"' + comma
        # remove last comma (e.g. last 2 chars)
        my_string = my_string[:-2]
    my_string += "]"
    return my_string   
   
def clean_list(l):
    for index, item in enumerate(l):
        if isinstance(item, dict):
            clean_dict(item)
        elif isinstance(item, list):
            clean_list(item)
        elif isinstance(item, str):
            l[index] = item.replace("\n","").replace("\r","")
        else:
            pass
            
def clean_dict(d):
    for key, value in d.items():
        if isinstance(value, list):
            clean_list(value)
        elif isinstance(value, dict):
            clean_dict(value)
        elif isinstance(value, str):
            newvalue = value.replace("\n","").replace("\r","")
            d[key] = newvalue
        else:
            pass
   
def find_key(rec_dict, target, depth=0):
    """
    find key "target" in recursive dict
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    try:
        #print (depth,target, rec_dict)
        if isinstance(rec_dict, dict):
            for key,value in rec_dict.items():
                if key == target:
                    return rec_dict[key]
            for key,value in rec_dict.items():
                r = find_key(value, target, depth+1)
                if r is not None:
                        return r
        #else:
        #    print ("no dict:", rec_dict)
    except:
        traceback.print_exc()


def find_key_link(rec_dict, target, depth=0):
    """
    find the first key recursively
    also traverse lists (arrays, oneOf,..) but only returns the first occurrence
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    if isinstance(rec_dict, dict):
        # direct key
        for key,value in rec_dict.items():
            if key == target:
                return rec_dict[key]
        # key is in array
        rvalues = []
        found = False
        for key,value in rec_dict.items():
            if key in ["oneOf", "allOf", "anyOf"]:
                for val in value:
                    #print ("xxx", depth, key, val)
                    if val == target:
                        return val
                    if isinstance(val, dict):
                        r = find_key_link(val, target, depth+1)
                        if r is not None:
                            found = True
                            # TODO: this should return an array, now it only returns the last found item
                            rvalues = r
        if found:
            return rvalues
        # key is an dict
        for key,value in rec_dict.items():
            r = find_key_link(value, target, depth+1)
            if r is not None:
                return r #[list(r.items())]
                
                
def basename(p):
    """Returns the final component of a pathname"""
    i = p.rfind('/') + 1
    return p[i:]
    
def load_json_schema(filename, dir):
    """
    load the JSON schema file
    :param filename: filename (with extension)
    :param dir: path to the file
    :return: json dict
    """

    fname = filename
    if filename.startswith("http://openconnectivityfoundation.github.io"):
        fname = basename(filename)
        fullpath = os.path.join(dir,fname)
        print ("load_json_schema downloading url ", filename, " to ", fullpath)
        wget.download(filename,fullpath)
        
    full_path = os.path.join(dir,fname)
    if os.path.isfile(full_path) is False:
        print ("load_json_schema: json file does not exist:", full_path)
    linestring = open(full_path, 'r').read()
        
    json_dict =json.loads(linestring)
    clean_dict(json_dict)

    return json_dict   
   
   
class FlattenSchema(object):
    def __init__(self, input_file, output_file):
        """
        initialize the Flatten/Resolve schema class.


        """
        self.tab = "  "
        self.indent =""
        self.input_file = input_file
        self.output_temp = output_file+"temp"
        self.output_file = output_file = output_file
        #self.dir = schema_dir
        self.schema_ignorelist = ['required', '$schema', 'type', 'definitions', 'description',
                                  'properties', ":", ":{", "minItems", "attribute", "format", "allOf", "$ref", "enum",
                                  "title", "oneOf", "anyOf", "additionalProperties", "items", "default", "minitems",
                                  "maxitems",
                                  "minimum", "maximum", "pattern", "readOnly", "minProperties", "additionalItems"]
        self.schema_types = ['boolean', 'array', 'object', 'enum', 'number', 'string']
    
        self.basedir = os.path.dirname(os.path.abspath(input_file))
        print ("basedir =", self.basedir)
    

    def fix_references_dict(self, mydict, defintionlist, propertylist, iteration=0, defupdate=True):
        """
        fix the external reference, e.g. make them internal
        dict part... see also the list part
        :param mydict: dict (json schema) to work on
        :param defintionlist: definition list to add the internal definitions to
        :param propertylist: properties list to add the properties too, e.g. no $ref used 
        :param iteration: recursion counter
        :param defupdate: update the definition, default is yes, 
        """

        #print ("fix_references_dict: fixing references")
        for key, value in mydict.items():
            if isinstance(value, list):
                self.fix_references_list(value, defintionlist, propertylist, defupdate=defupdate)
            elif isinstance(value, dict):
                self.fix_references_dict(value, defintionlist, propertylist, iteration=1, defupdate=defupdate)
            else:
                if str(key) in ["$ref"]:
                    print (" fix_references_dict: reference found:", defupdate, key, value)
                    if value.startswith("#/definitions/") == False:
                        # external reference.. 
                        print ("  fix_references_dict: $ref value:", value)
                        filename = value.split('#')[0]
                        print ("  fix_references_dict: fixing $ref file:", filename)
                        whole_file = True
                        reference = filename
                        try:
                            reference = value.split('#/definitions/')[1]
                            print ("  fix_references_dict: reference found:", reference)
                            whole_file = False
                        except:
                            print ("  fix_references_dict: reference NOT found (filename):", reference)
                            pass
                        new_reference = "#/definitions/"+reference
                        print ("  fix_references_dict: new reference:", new_reference)
                        mydict[key] = new_reference
                        
                        if defupdate == True:
                            # add reference to the defintionlist
                            file_dict = load_json_schema(filename, self.basedir)
                            if whole_file == False:
                                propkey = find_key(file_dict, reference)
                                if propkey is not None:
                                    print ("  fix_references_dict: adding definition (reference):", reference)
                                    defintionlist[reference] = propkey
                                else:
                                    lastkey = reference.split("/")[-1]
                                    print ("  fix_references_dict: reference only key :", reference, lastkey)
                                    propkey = find_key(file_dict, lastkey)
                                    if propkey is not None:
                                        print ("  fix_references_dict: adding definition (reference):", reference)
                                        defintionlist[lastkey] = propkey
                                
                                
                                    print ("  ERROR could not reference ", reference, " in file", filename )
                            else:
                                print ("  fix_references_dict: adding definition (file):", reference)
                                defintionlist[reference] = file_dict
                    else:
                        print ("  fix_references_dict: no need to update:", value)
                        
                   

    def fix_references_list(self, l, defintionlist, propertylist, defupdate=True):
        """
        fix the external reference, e.g. make them internal
        list part... see also the dict part
        :param l: list (json schema) to work on
        :param defintionlist: definition list to add the internal definitions to
        :param propertylist: properties list to add the properties too, e.g. no $ref used 
        :param defupdate: update the definition, default is yes, 
        """
        for index, item in enumerate(l):
            if isinstance(item, dict):
                self.fix_references_dict(item, defintionlist, propertylist,iteration=1, defupdate=defupdate)
            elif isinstance(item, list):
                self.fix_references_list(item, defintionlist, propertylist,defupdate=defupdate)
            else:
                pass


    def remove_external_references(self, json_dict, definitionlist, propertylist, recursion= " "):
        """
        remove the external references
        2 step approach, first create the definition part from the external references
        then fix the external reference in the just added definition part itself
        :param json_dict: dict (json schema) to work on
        :param defintionlist: definition list to add the internal definitions to
        :param propertylist: properties list to add the properties too, e.g. no $ref used 
        :param recursion: recursing indication
        """
        print ("remove_external_references")
        self.fix_references_dict(json_dict, definitionlist, propertylist)
        # fix the references in the definition list
        # the following code adds the missing definitions in the defintionlist
        
        print ("=>remove_external_references 2rd pass: update the definition list")
        new_dict_deepcopy = deepcopy(definitionlist)
        self.fix_references_dict(new_dict_deepcopy, definitionlist, propertylist)
        # now change the reference value only
        print ("=>remove_external_references 3rd pass: update the references")
        new_dict_deepcopy = deepcopy(definitionlist)
        self.fix_references_dict(new_dict_deepcopy, definitionlist, propertylist)
        print ("=>remove_external_references 4th pass: the references")
        new_dict_deepcopy = deepcopy(definitionlist)
        self.fix_references_dict(new_dict_deepcopy, definitionlist, propertylist)
        
        # now change the reference value only
        print ("=>remove_external_references 5th pass: update the references")
        self.fix_references_dict(definitionlist, definitionlist, propertylist, defupdate=False)
        
      
    def get_reference_from_ref(self, value):

        print ("get_reference_from_ref", value)
        if value.startswith("#/definitions/"):
            reference = value [len("#/definitions/"):]
            print ("get_reference_from_ref", reference)
            return reference
            
        filename = value.split('#')[0]
        print (" get_reference_from_ref file:", filename)
        whole_file = True
        reference = filename
        try:
            reference = value.split('#/definitions/')[1]
            print ("  get_reference_from_ref: reference found:", reference)
        except:
            print ("  get_reference_from_ref: reference NOT found (filename):", reference)
            pass
        return reference
        #ew_reference = "#/definitions/"+reference
        #print ("  fix_references_dict: new reference:", new_reference)
        #mydict[key] = new_reference
                
    
    def processAllOf(self, mydict, propertieslist, requiredlist, recursion=" "):
        """
        code to remove the allOff construct by flatten it.
        this is a bit of fiddling around with dicts/lists
        the allOff is an list, all other things are dicts.
        this goes down 3 levels (as currently used in oneIOTA definitions)
        :param mydict: dict (json schema) to work on
        :param propertylist: properties list to add the properties too, e.g. no $ref used 
        :param recursion: recursing indication
        """
        
        anyOf = None
        if isinstance(mydict, dict) :
            props = mydict.get("properties")
            allOf = mydict.get("allOf")
            anyOf = mydict.get("anyOf")
            if props is not None:
                for propname, prop in props.items():
                    print (recursion+"processAllOf : properties adding,", propname)
                    propertieslist[propname] = prop
            if allOf is not None:
                for item in allOf:
                    # this should be an dict.
                    propitem = item.get("properties")
                    allOfitem = mydict.get("allOf")
                    anyOfitem = item.get("anyOf")
                    if anyOfitem is not None:
                        anyOf = anyOfitem
                    typeitem = item.get("type")
                    refitem = item.get("$ref")
                    if propitem is not None:
                        # add all items of the property list of the object
                        for propname, prop in propitem.items():
                            print (recursion+"processAllOf : allOf adding", propname)
                            propertieslist[propname] = prop
                    elif refitem is not None:
                        # add all items of the property list of the object
                        reference = self.get_reference_from_ref(refitem)
                        print("processAllOf: handling reference:", reference)
                        proplist_properties = find_key_link(mydict, reference)
                        required_ref = proplist_properties.get("required")
                        proplist = proplist_properties.get("properties")
                        itemlist = proplist_properties.get("items")
                        anyOfitem = proplist_properties.get("anyOf")
                        print (" required:", required_ref)
                        if required_ref is not None:
                            for x in required_ref:
                                requiredlist.append(x)
                        if anyOfitem is not None:
                            anyOf = anyOfitem
                        
                        if proplist is not None:
                            # add the properties from the properties tag
                            for propname, prop in proplist.items():
                                print (recursion+"processAllOf : $ref adding", propname)
                                propertieslist[propname] = prop
                        elif itemlist is not None:
                            # it is an array
                            for item_name, item_object in proplist_properties.items():
                                if item_name in ["type", "items", "minItems", "description", "maxItems", "uniqueItems"] :
                                    # e.g all keywords of an array
                                    propertieslist[item_name] = item_object
                        else:
                            print (recursion+"processAllOf : ERROR could not find reference of $ref ", reference)
                    elif allOfitem is not None:
                        print (recursion+"handling allOf", item, allOfitem)
                        # the object starts with oneOf
                        for item_2 in allOfitem:
                            if isinstance(item_2, dict):
                                for item3name, item3object in item_2.items():
                                    # add the reference
                                    if item3name in ["$ref"]:
                                        propertieslist[item3name] = item3object
                                    elif item3name in ["properties"]:
                                        # add the properties
                                        for item4name, item4object in item3object.items():
                                            print (recursion+"processAllOf 3: adding", item4name)
                                            propertieslist[item4name] = item4object
                                    elif item3name in ["allOf"]:
                                        if isinstance(item3object, list):
                                            for itemlistobject in item3object:
                                                if isinstance(itemlistobject, dict):
                                                    for item4name, item4object in itemlistobject.items():
                                                        if item4name in ["properties"]:
                                                            for item5name, item5object in item4object.items():
                                                                print (recursion+"processAllOf dict props5: adding", item5name)
                                                                propertieslist[item5name] = item5object
                                                        else:
                                                            print (recursion+"processAllOf ERROR: not handled (lv3): ", item4name, item4object)
                                                elif isinstance(itemlistobject, list):
                                                    for listitem in itemlistobject:
                                                        for item4name, item4object in listitem.items():
                                                            if item4name in ["properties"]:
                                                                for item5name, item5object in item4object.items():
                                                                    print (recursion+"processAllOf list props5: adding", item5name)
                                                                    propertieslist[item5name] = item5object
                                                            else:
                                                                print (recursion+"processAllOf ERROR: not handled (lv4): ", item4name, item4object)
                                                    
                                    elif item3name in ["type", "items", "minItems", "description", "maxItems", "uniqueItems"] :
                                        # e.g all keywords of an array
                                        propertieslist[item3name] = item3object
                                    else:
                                        print ("processAllOf ERROR: not handled: ", item3name)
        print ("processAllOf return: ", anyOf)                                
        return anyOf                                       
    
    def get_required_from_definition(self, json_dict, defintion_name):
        name = defintion_name [len("#/definitions/"):]
        print ("get_required_from_definition: name:", name)
        definitions = json_dict.get("definitions")
        if definitions == None:
            return None
        schema_props = definitions.get(name)
        print (schema_props)
    
    def process(self, resolve_internal=True):
        print (self.input_file)
        json_dict = load_json_schema(self.input_file, "")
        #fix_references_dict(json_dict)
        required = json_dict.get("required")
        definition = json_dict.get("definitions")
        allOf_data = json_dict.get("allOf")
        type_data = json_dict.get("type")
        propertiesdict = json_dict.get("properties")
        definitiondict = {}
                
        self.remove_external_references(json_dict, definitiondict, propertiesdict)
        
        if definition is not None:
            for entry, entryobject in definition.items():
                definitiondict[entry] = entryobject
                
        print ("\n") 
        print ("allOf      :", allOf_data)        
        print ("properties :", propertiesdict)
        print ("required   :", required)
        print ("\n") 
                
        # start writing the output file       
        self.openfile()
        
        # add schema
        schema_name= json_dict.get("$schema")
        if schema_name is not None:
            self.write_stringln('"$schema": "'+schema_name+ '",')
        
        # add description
        description_title= json_dict.get("description")
        if description_title is not None:
            self.write_stringln('"description": "'+description_title+ '",')
        
        # add title
        title= json_dict.get("title")
        if title is not None:
            self.write_stringln('"title": "'+title+ ' (auto merged)",')
               
        # add the definition tag
        self.write_stringln('"definitions" : ')
        # the created property dict
        self.increase_indent()
        object_string = json.dumps(definitiondict, sort_keys=True, indent=2, separators=(',', ': '))
        object_string += ","
        adjusted = self.add_justification_smart(self.indent, object_string)
        self.write_stringln(adjusted )
        self.decrease_indent()
               
               
        if allOf_data is None:
            # add the properties tag
            
            # the created property dict
            if propertiesdict is not None:
                if propertiesdict.get("type") is not None:
                    # remove type
                    propertiesdict.pop("type", None)
                    
                self.increase_indent()    
                self.write_stringln('"properties" : ')
                object_string = json.dumps(propertiesdict, sort_keys=True, indent=2, separators=(',', ': '))
                adjusted = self.add_justification_smart(self.indent, object_string)
                self.write_stringln(adjusted)
                self.decrease_indent()
            else:
                # write the top level but not definition, required, etc..
                print ("process writing top level")
                first = True
                for topname, topobject in json_dict.items():
                    if topname in ["$schema", "description", "id", "definitions", "properties"]:
                        pass
                    else:
                        object_string = json.dumps(topobject, sort_keys=True, indent=2, separators=(',', ': '))
                        adjusted = self.add_justification_smart(self.indent, object_string)
                        if first == True:
                            self.write_stringln('"'+topname+'" : ')
                            self.write_stringln(adjusted)
                        else:
                            self.write_stringln(',"'+topname+'" : ')
                            self.write_stringln(adjusted)
                        first = False
        else:
            self.write_stringln('"allOf" : ') 
            self.increase_indent()
            object_string = json.dumps(allOf_data, sort_keys=True, indent=2, separators=(',', ': '))
            adjusted = self.add_justification_smart(self.indent, object_string)
            self.write_stringln(adjusted)
            self.decrease_indent()            
        
        # add the required tag if it exist...
        if required is not None:
            self.write_stringln(',')
            self.write_stringln('"required":'+list_to_array(required))
        else:
            required = []
        
        self.closefile()
        # ###################################
        # read the contents of the temp file
        # ###################################
        json_dict = load_json_schema(self.output_temp, "")
        
        oneOf_data = json_dict.get("oneOf")
        anyOf_data = json_dict.get("anyOf")  # on the top level
        
        if resolve_internal == True:
            # resolve the internal references.
            # e.g. replace the json_dict with the resolved dict
            import jsonref
            json_str = json.dumps(json_dict, sort_keys=True, indent=2, separators=(',', ': '))
            resolved_json = jsonref.loads(json_str)
            resolved_string = json.dumps(resolved_json, sort_keys=True, indent=2, separators=(',', ': '))
            json_dict =json.loads(resolved_string)
        
            #print ("process : resolved string:",resolved_string)
        
        oneOf_data = json_dict.get("oneOf")
        anyOf_data = json_dict.get("anyOf")  # on the top level
        
        
        if resolve_internal == True:
            # remove the definitions, they are resolved!!
            definitions = json_dict.get("definitions")
            if definitions is not None:
                json_dict.pop('definitions')
                   
        # remove first level of oneOff
        properties = {}
        anyOf_data = self.processAllOf(json_dict, properties, required)
        
        if properties.get("items") is  None:
            # this is an object... so add the properties layer
            properties.pop("type", None)
            if properties.get("$ref") is not None:
                # resolve the $ref at the top level of schema
                value = properties.get("$ref")
                #if value.startswith("#/definitions/"):
                reference = value [len("#/definitions/"):]
                #reference = value.split("#/definitions/", 1)[0]
                print ("reference on top level:", value, reference)
                proplist = find_key_link(definitiondict, reference)
                if proplist.get("items") is not None:
                    # top level is an array
                    for prop, propitem in proplist.items():
                        json_dict["prop"] = propitem
                else:
                    json_dict["properties"] = proplist.get("properties")
            else:
                # normal dict... just copy
                json_dict["properties"] = properties
        else:
            # this is an array (without a name) so it should not have the properties layer, e.g. add all the items one by one..
            for propname, propobject in properties.items():
                json_dict[propname] = propobject
        
        # remove the allOf tag, we have handled it
        allOf = json_dict.get("allOf")
        if allOf is not None:
            json_dict.pop('allOf')
        propdict = json_dict.get("properties")
        if propdict is not None:
            if len(propdict) == 0:
                json_dict.pop('properties')

        if oneOf_data is not None:
            json_dict["oneOf"] = oneOf_data
            
        if anyOf_data is not None:
            json_dict["anyOf"] = anyOf_data
            
        if type_data is not None:
            json_dict["type"] = type_data
        
        req = json_dict.get("required")
        if req is None:
            if len(required) > 0:
                json_dict["required"] = required
        
        resolved_string = json.dumps(json_dict, sort_keys=True, indent=2, separators=(',', ': '))
       
        f = open(self.output_file, "w")
        f.write(resolved_string)
        f.close();
        
        prop_string = json.dumps(properties, sort_keys=True, indent=2, separators=(',', ': '))
        #print (prop_string)
        self.verify()
    
    def increase_indent(self):
        """
        increase indentation for output
        """
        self.indent += self.tab

    def decrease_indent(self):
        """
        decrease indentation for output
        """
        length = len(self.tab)
        total_lenght = len(self.indent)
        self.indent = self.indent[:total_lenght-length]

    def write_stringln(self, string):
        """
        write the string to file with end of line
        :param string: string to be written to file with end of line
        """
        self.f.write(self.indent + string + "\n")

    def write_string_raw(self, string):
        """
        write the string to file, no changes to string
        :param string: string to be written to file
        """
        self.f.write(string)

    def write_string(self, string):
        """
        write the string to file, with indentation
        :param string: string to be written to file, with indentation
        """
        self.f.write(self.indent + string)
    
    
    def openfile(self):
        """
        open file as swagger file
        :param version: version of the API (e.g. not the swagger version
        :param title: title of the API
        """
        self.f = open(self.output_temp, "w")
        self.indent = ""

        self.write_stringln("{")
        self.increase_indent()        
            
    
    def closefile(self):
        """
        close the file
        e.g. end the json object with an closing }
        """
        
        self.decrease_indent()
        self.write_string_raw("}\n")
        self.f.close();

    def verify(self):
        """
        verify the generated swagger file.
        easy verification: only check is that it is an valid json file
        """
        
        print ("verify json syntax on temp file:",self.output_temp)
        try:
            input_string_schema = open(self.output_temp, 'r').read()
            json_dict =json.loads(input_string_schema)
        except:
            traceback.print_exc()
        
        print ("verify json syntax on output file:",self.output_file)
        try:
            input_string_schema = open(self.output_file, 'r').read()
            json_dict =json.loads(input_string_schema)
        except:
            traceback.print_exc()
        
        print ("verify done...")
        
        
        
   
    def read_file(self, filename):
        """
        read the file as a string

        :param filename: file to read
        :return:
        """
        try:
            linestring = open(filename, 'r').read()
            # create the table with contents..
            return linestring
        except:
            pass
        try:
            full_path = os.path.join(self.dir, filename)
            linestring = open(full_path, 'r').read()
            # create the table with contents..
            return linestring
        except:
            pass

        try:
            base = os.path.basename(filename)
            full_path = os.path.join(self.dir, base)
            linestring = open(full_path, 'r').read()
            # create the table with contents..
            return linestring
        except:
            pass

        print ("read_file: could not open file:", filename, full_path)


    def add_justification_smart(self, depth, input_string, no_dot_split=True):
        """
        add the spaces for an correct indentation of the generated RAML code section
        for descriptions in the RAML definitions
        :param depth: character depth
        :param input_string: string to be adjusted
        :return:  adjusted string
        """
        ret_string = ""
        all_lines = input_string.splitlines()
        for x_line in all_lines:
            if no_dot_split is False:
                lines = x_line.split(". ")
                for line in lines:
                    string1 = depth + line + "\n"
                    if len(line) > 0:
                        ret_string = ret_string + string1
            else:
                string1 = depth + x_line + "\n"
                ret_string = ret_string + string1
        return ret_string
        
        
        
if __name__ == '__main__':
    # set the execution path of the tool
    if hasattr(sys, 'frozen'):
        my_dir = os.path.dirname(sys.executable)
    else:
        my_dir = os.path.dirname(sys.argv[0])
        
     

    # version information
    my_version = "1.0"
    program_name="resolve_json_schema"
    #try:
    #    from version import VERSION#
    #
    #       my_version = VERSION
    #except:
    #    pass

    print ("===================================")
    print (program_name)
    print ("version: ", my_version)

    # argument parsing
    parser = argparse.ArgumentParser(description='Resolve and Flatten JSON schemas')
    parser.add_argument('-schema', '--schema', help='input file schema')
    parser.add_argument('-out', '--out', help='output file schema')
    parser.add_argument('-resolveInternal', '--resolveInternal', help='resolve internal references (e.g. avoid blow up of recursion),  (--resolveInternal true)')
    args = vars(parser.parse_args())

    infile = args['schema']
    outfile = args['out']
    resolve_internal_switch = args['resolveInternal']

    if resolve_internal_switch is None:
        resolve_internal_switch = False
    else:
        resolve_internal_switch = True
        
    print ("===================================")
    print ("using current directory   :", my_dir)
    print ("using schema file         :", infile)
    print ("using outfile file        :", outfile)
    print ("using resolveInternal     :", resolve_internal_switch)    
    print ("===================================")
    

    if my_dir:
        os.chdir(my_dir)

    if len(sys.argv) == 1:
        parser.print_help()
        processor = None
    else:
        processor = FlattenSchema(infile, outfile)

    if processor is not None:
        processor.process(resolve_internal=resolve_internal_switch)
        
    
    print ("===========DONE==============",program_name)    
   
    