#!/bin/bash
# script to convert an directory of RAML files to swagger2.0
# usage:
# convert.sh <input dir>  <output dir>
#
# the directories should be relative path with respect to this file
# the execution should take place from the test directory (all references are relative to this directory)
#
# output:
#    each raml file will have its own output directory. e.g. raml filename without extension.
#

#
# pre requisites:
# - wb-swagger tool chain (see https://github.com/WAvdBeek/wb-swagger-tools )
#
# raml2doc, uses python2.7
# e.g. retrieved from https://github.com/openconnectivityfoundation/raml2doc
#
# swagger2doc uses python 3
# should be installed on the same folder level as raml2doc
#
# run the install_node_packages.sh once
# this installs the node packages that are needed to run node-resolver
#

PYTHON_EXE=C:\\python27\\python.exe
RAML2DOC=../src/raml2doc.py
#
# swagger2doc, uses python 3
# https://github.com/openconnectivityfoundation/swagger2doc
# same level in directory structure as raml2doc
PYTHON3_EXE=C:\\python35\\python.exe
JSONRESOLVER=../src/resolve_json_schema.py
if [ -f $PYTHON3_EXE ]
then
	echo "$file found."
else
	#echo "$file not found."
    PYTHON3_EXE=python3
fi

#SCHEMA_DIR="/schemas"
IN_DIR=$1
OUTPUT_DIR=$2
# swagger2doc extra arguments are $3
echo "extra arguments: $3"
echo "extra arguments: $4"

SCHEMA_DIR=""
if [ -d $IN_DIR/schemas ]
then
echo "schema dir exist"
SCHEMA_DIR="/schemas"
fi


OUTPUT_DIR_DOCS=../test/$OUTPUT_DIR/.
REF_DIR=./ref
EXT=.txt

function my_test {
    $PYTHON3_EXE $JSONRESOLVER $*
}


#my_test -schema ../test/test_schemas/oic.r.sensor.acceleration.json  -out ../test/out/test.json
my_test -schema ../test/test_schema_collection/oic.collection-schema.json  -out ../test/out/test-col.json

