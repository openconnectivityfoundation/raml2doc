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
                
def load_json_schema(filename, dir):
    """
    load the JSON schema file
    :param filename: filename (with extension)
    :param dir: path to the file
    :return: json dict
    """
    full_path = os.path.join(dir,filename)
    if os.path.isfile(full_path) is False:
        print ("json file does not exist:", full_path)

    linestring = open(full_path, 'r').read()
    json_dict =json.loads(linestring)
    clean_dict(json_dict)

    return json_dict   
   
   
   
   
   
   
class FlattenSchema(object):
    def __init__(self, input_file, output_file):
        """
        initialize the class


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
        if iteration == 0:
            print ("fix_references_dict: fixing references")
        for key, value in mydict.items():
            if isinstance(value, list):
                #print ("list_value", value)
                self.fix_references_list(value, defintionlist, propertylist, defupdate=defupdate)
            elif isinstance(value, dict):
                self.fix_references_dict(value, defintionlist, propertylist, iteration=1, defupdate=defupdate)
            else:
                if str(key) in ["$ref"]:
                    #print ("fix_references_dict: $ref value:", value)
                    if value.startswith("#/definitions/") == False:
                        # external reference.. 
                        print ("fix_references_dict: $ref value:", value)
                        filename = value.split('#')[0]
                        reference = value.split('#/definitions/')[1]
                        print ("fix_references_dict: fixing $ref file:", filename)
                        
                        print ("fix_references_dict: reference:", reference)
                        new_reference = "#/definitions/"+reference

                        mydict[key] = new_reference
                        if defupdate == True:
                            # add reference to the defintionlist
                            file_dict = load_json_schema(filename, self.basedir)
                            propkey = find_key(file_dict, reference)
                            if propkey is not None:
                                defintionlist[reference] = propkey
                        
                   

    def fix_references_list(self, l, defintionlist, propertylist, defupdate=True):
        for index, item in enumerate(l):
            if isinstance(item, dict):
                self.fix_references_dict(item, defintionlist, propertylist,iteration=1, defupdate=defupdate)
            elif isinstance(item, list):
                self.fix_references_list(item, defintionlist, propertylist,defupdate=defupdate)
            else:
                pass


    def remove_external_references(self, json_dict, definitionlist, propertylist, recursion= " "):
        print (recursion + "remove_external_references")
        self.fix_references_dict(json_dict, definitionlist, propertylist)
        # fix the references in the definition list
        # the following code adds the missing definitions in the defintionlist
        new_dict_deepcopy = deepcopy(definitionlist)
        self.fix_references_dict(new_dict_deepcopy, definitionlist, propertylist)
        # now change the reference value only
        self.fix_references_dict(definitionlist, definitionlist, propertylist, defupdate=False)
        
      
    
    def processAllOf(self, mydict, propertieslist, recursion=" "):
        if isinstance(mydict, dict) :
            props = mydict.get("properties")
            allOf = mydict.get("allOf")
            if props is not None:
                for propname, prop in props.items():
                    propertieslist[propname] = prop
            if allOf is not None:
                for item in allOf:
                    # this should be an dict.
                    propitem = item.get("properties")
                    if propitem is not None:
                        for propname, prop in propitem.items():
                            propertieslist[propname] = prop
      
        
          
    
    def process(self):
        print (self.input_file)
        json_dict = load_json_schema(self.input_file, "")
        #fix_references_dict(json_dict)
        required = json_dict.get("required")
        definition = json_dict.get("definitions")
        allOf_data = json_dict.get("allOf")
        propertiesdict = json_dict.get("properties")
        definitiondict = {}
                
        self.remove_external_references(json_dict, definitiondict, propertiesdict)
        
        for entry, entryobject in definition.items():
            definitiondict[entry] = entryobject
  
        #if allOf is not None:
        #   self.processAllOf(allOf_data, definitiondict, propertiesdict)
   
        print ("\n\n") 
        print ("allOf      :", allOf_data)        
        print ("properties :", propertiesdict)
        print ("required   :", required)
        print ("\n\n") 
                
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
            self.write_stringln('"properties" : ')
            # the created property dict
            self.increase_indent()
            object_string = json.dumps(propertiesdict, sort_keys=True, indent=2, separators=(',', ': '))
            adjusted = self.add_justification_smart(self.indent, object_string)
            self.write_stringln(adjusted)
            self.decrease_indent()
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
        
        self.closefile()
        
        
        import jsonref
        #json_dump = json.load(open(self.output_temp))
        json_file = open(self.output_temp,"r")
        json_str = json_file.read()
        #print (json_str)
        
        resolved_json = jsonref.loads(json_str)
        resolved_string = json.dumps(resolved_json, sort_keys=True, indent=2, separators=(',', ': '))
        
        json_dict =json.loads(resolved_string)
        
        # remove the definitions, they are resolved!!
        definitions = json_dict.get("definitions")
        if definitions is not None:
            json_dict.pop('definitions')
            
        #resolved_string = json.dumps(json_dict, sort_keys=True, indent=2, separators=(',', ': '))
        #print (resolved_string)
       
        # remove first level of oneOff
        properties = {}
        self.processAllOf(json_dict, properties);
        json_dict["properties"] = properties
        allOf = json_dict.get("allOf")
        if allOf is not None:
            json_dict.pop('allOf')

        resolved_string = json.dumps(json_dict, sort_keys=True, indent=2, separators=(',', ': '))
        print (resolved_string)
       
        f = open(self.output_file, "w")
        f.write(resolved_string)
        f.close();
        
       
        
        
        prop_string = json.dumps(properties, sort_keys=True, indent=2, separators=(',', ': '))
        print (prop_string)
        
        
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
        
        print ("verify json temp syntax :")
        input_string_schema = open(self.output_temp, 'r').read()
        json_dict =json.loads(input_string_schema)
        
        print ("verify json syntax :")
        input_string_schema = open(self.output_file, 'r').read()
        json_dict =json.loads(input_string_schema)
        
        
        
   
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
    #try:
    #    from version import VERSION#
    #
    #       my_version = VERSION
    #except:
    #    pass

    print ("===================================")
    print ("resolve_json_schema")
    print ("version: ", my_version)

    # argument parsing
    parser = argparse.ArgumentParser(description='Flatten JSON schemas')
    parser.add_argument('-schema', '--schema', help='input file schema')
    parser.add_argument('-out', '--out', help='output file schema')
    args = vars(parser.parse_args())

    infile = args['schema']
    outfile = args['out']
    
    print ("===========================")
    print ("using current directory   :", my_dir)
    print ("using schema file         :", infile)
    print ("using outfile file        :", outfile)
    

    if my_dir:
        os.chdir(my_dir)

    if len(sys.argv) == 1:
        parser.print_help()
        processor = None
    else:
        processor = FlattenSchema(infile, outfile)

    if processor is not None:
        processor.process()
   
    