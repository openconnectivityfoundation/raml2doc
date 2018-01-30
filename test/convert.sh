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
RESOLVER=../src/resolve_json_schema.py
#
# swagger2doc, uses python 3
# https://github.com/openconnectivityfoundation/swagger2doc
# same level in directory structure as raml2doc
PYTHON3_EXE=C:\\python35\\python.exe
SWAG2DOC=../../swagger2doc/src/swagger2doc.py
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
echo " HELLO convert.sh"
echo "================="
echo "IN_DIR=$1"
echo "OUTPUT_DIR=$2"
echo "extra arguments: $3"
echo "extra arguments: $4"
echo "================="


SCHEMA_DIR=""
if [ -d $IN_DIR/schemas ]
then
echo "schema dir exist"
SCHEMA_DIR="/schemas"
fi


OUTPUT_DIR_DOCS=../test/$OUTPUT_DIR/.
REF_DIR=./ref
EXT=.txt


function compare_output {
    diff -w $OUTPUT_DIR/$TEST_CASE$EXT $REF_DIR/$TEST_CASE$EXT
    echo "testcase difference: $TEST_CASE $?"
    #echo "blah"
}

function compare_to_reference_file {
    diff -w $OUTPUT_DIR/$1 $REF_DIR/$1
    echo "output $1 difference: $TEST_CASE $?"
    #echo "blah"
}


function compare_to_reference_file_in_dir {
    diff -w $OUTPUT_DIR/$1 $REF_DIR/$2/$1
    echo "output $1 difference: $TEST_CASE $?"
    #echo "blah"
}

function compare_file {
    echo "comparing ($TEST_CASE): " $1 $2
    diff -wb $1 $2
    #echo "blah"
}


function my_test {
    $PYTHON_EXE $RAML2DOC $* > $OUTPUT_DIR/$TEST_CASE$EXT 2>&1
    compare_output
}

function my_test_in_dir {
    mkdir -p $OUTPUT_DIR/$TEST_CASE
    $PYTHON_EXE $RAML2DOC $* >> $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    #compare_file $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT $REF_DIR/$TEST_CASE/$TEST_CASE$EXT
}


function add_to_doc {
    $PYTHON3_EXE $SWAG2DOC $*
    #compare_file $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT $REF_DIR/$TEST_CASE/$TEST_CASE$EXT
}

containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

crop_string_ends() {
    STR="$1"
    NEWSTR=""
    COUNT=0
    while read -n 1 CHAR
    do
        COUNT=$(($COUNT+1))
        if [ $COUNT -eq 1 ] || [ $COUNT -eq ${#STR} ]
        then
            continue
        fi
        NEWSTR="$NEWSTR"$CHAR
    done <<<"$STR"
    echo $NEWSTR
}




TEST_CASE="testcase_1"
outfile="outfile.txt"

echo "" > $outfile
cp ../input/ResourceTemplate.docx $outfile.docx

mkdir  $OUTPUT_DIR
mkdir  $OUTPUT_DIR/copy-resolved
cp $IN_DIR/* $OUTPUT_DIR/copy-resolved/.
mkdir  $OUTPUT_DIR/copy-resolved/examples
mkdir  $OUTPUT_DIR/copy-resolved/schemas
cp $IN_DIR/examples/* $OUTPUT_DIR/copy-resolved/examples/.
cp $IN_DIR/schemas/* $OUTPUT_DIR/copy-resolved/schemas/.

#
# these schema's should be kept intact since they will be referenced by other schemas.. e.g. the #defintion part needs to be there.
#
ignorelist=(dummy oic.core-schema.json oic.types-schema.json oic.collection.linkslist-schema.json oic.collection-schema.json oic.oic-link-schema.json oic.baseResoure.json oic.core.json oic.core-schema.json oic.oic-link-schema.json oic.baseResource.json oic.basecorecomposite.json )
notflatten=(dummy oic.r.airqualitycollection.json oic.r.airqualitycollection-ll.json oic.r.consumablecollection.json oic.r.consumablecollection-ll.json oic.r.heatingzonecollection-ll.json oic.r.heatingzonecollection.json oic.rd.publish-schema.json)

# old node.js based...
#for file in $IN_DIR$SCHEMA_DIR/*.json
#do
#    if [[ $file != *".swagger.json" ]]; then
#        echo "converting $file to $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)"
#        mybasename=$(basename $file)
#        containsElement $mybasename ${ignorelist[@]}
#        retvalue=$?
#        if [[ $retvalue == 0 ]]; then 
#            echo "ignoring $(basename $file)"
#            cp $file $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)
#        else    
#            node node-resolver.js $file    >  $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)
#            if [[ -s $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file) ]]; then
#                echo "generated."
#            else
#                echo "empty file, deleting."
#                rm -f $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)
#            fi
#        fi 
#    fi
#done


for file in $IN_DIR$SCHEMA_DIR/*.json
do
    if [[ $file != *".swagger.json" ]]; then
        echo "converting/resolving $file to $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)"
        mybasename=$(basename $file)
        containsElement $mybasename ${ignorelist[@]}
        retvalue=$?
        
        containsElement $mybasename ${notflatten[@]}
        notflatten=$?
        
        resolve_arg=" --resolveInternal true"
        if [[ $notflatten == 0 ]]; then 
            resolve_arg=" "
        fi
        
        if [[ $retvalue == 0 ]]; then 
            echo "ignoring $(basename $file)"
            cp $file $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)
        else    
            $PYTHON3_EXE $RESOLVER -schema  $file -out  $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)  $resolve_arg
            if [[ -s $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file) ]]; then
                echo "generated."
            else
                echo "empty file, deleting."
                rm -f $OUTPUT_DIR/copy-resolved$SCHEMA_DIR/$(basename $file)
            fi
        fi 
    fi
done

 echo "=================="
 echo "Resolving done.."
 echo "=================="

IN_DIR=$OUTPUT_DIR/copy-resolved

for file in $IN_DIR/*.raml
do
    if [[ -f $file ]]; then
        echo ""
        echo "======================"
        echo "processing file: $file"
        filename="${file##*/}"
        basename="${filename%.*}"
        #copy stuff ....
        TEST_CASE=$basename
        mkdir -p $OUTPUT_DIR/$TEST_CASE
        
        rm -f $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT
        string_all=`grep ResURI: $file`
        string_1=`grep ResURI? $file`
        string_2=`grep InterfaceURI: $file`
        string_3=`grep ^/oic/ $file`
        string_4=`grep URI: $file`
        string_5=`grep /example/ $file`
        string_all="$string_all $string_1 $string_2 $string_3 $string_4  $string_5"
        echo " url to be processed: $string_all"
        for string in $string_all
        do
            URI=`crop_string_ends $string`
            VAR_URI=$(echo $URI | sed 's#/#_#g' | sed 's#?#_#g')
            echo " processing $URI ($URI_VAR) from $file"
            my_test_in_dir  -docx ../input/ResourceTemplate.docx -schemadir $IN_DIR$SCHEMA_DIR -resource $URI -raml $file -outdocx $OUTPUT_DIR/$TEST_CASE_$VAR_URI.docx -swagger $OUTPUT_DIR/$TEST_CASE/$TEST_CASE_$VAR_URI.swagger.json
            echo $OUTPUT_DIR/$TEST_CASE/$TEST_CASE_$VAR_URI.swagger.json >> $outfile
            mydir=`pwd`
            pushd `pwd`
            cd $OUTPUT_DIR/$TEST_CASE
            echo " running swagger validator at $OUTPUT_DIR/$TEST_CASE on $TEST_CASE_$URI.swagger.json"
            output_swagger_validation=`wb-swagger validate $TEST_CASE_$VAR_URI.swagger.json`
            echo $output_swagger_validation >> $mydir/$outfile 2>&1
            echo $output_swagger_validation
            popd
            echo " running swagger2doc on $OUTPUT_DIR/$TEST_CASE/$TEST_CASE_$URI.swagger.json "
            add_to_doc -docx $outfile.docx -swagger $OUTPUT_DIR/$TEST_CASE/$TEST_CASE_$VAR_URI.swagger.json -resource $URI -word_out $OUTPUT_DIR_DOCS/$TEST_CASE/$TEST_CASE.docx $3 $4
            cp $OUTPUT_DIR_DOCS/$TEST_CASE/$TEST_CASE.docx $outfile.docx
            #-docx ../input/ResourceTemplate.docx -resource BinarySwitchResURI -swagger ../test/in/test_swagger_1/test_swagger_1.swagger.json -word_out $OUTPUT_DIR_DOCS/$TEST_CASE/$TEST_CASE.docx
        done


    fi
done

read -p "Press any key to continue"
