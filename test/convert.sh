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
#    ou

PYTHON_EXE=C:\\python27\\python.exe
RAML2DOC=../src/raml2doc.py



#IN_DIR=../../../../../Wouter2/IoTDataModels
#OUTPUT_DIR=../../out

IN_DIR=$1
OUTPUT_DIR=$2


OUTPUT_DIR_DOCS=../test/$OUTPUT_DIR
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
    $PYTHON_EXE $RAML2DOC $* > $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    #compare_file $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT $REF_DIR/$TEST_CASE/$TEST_CASE$EXT
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
 
for file in $IN_DIR/*.raml
do
    if [[ -f $file ]]; then
        echo $file
        filename="${file##*/}"
        basename="${filename%.*}"
        #copy stuff ....
        TEST_CASE=$basename
        mkdir -p $OUTPUT_DIR/$TEST_CASE
        string=`grep ResURI: $file`
        echo $string
        URI=`crop_string_ends $string`
        #URI=`echo $string | tail -c +2 | head -c -1`
        echo $URI
        my_test_in_dir  -docx ../input/ResourceTemplate.docx -schemadir $IN_DIR -resource $URI -raml $file -outdocx $OUTPUT_DIR/$TEST_CASE.docx -swagger $OUTPUT_DIR/$TEST_CASE/$TEST_CASE.swagger.json
        echo $OUTPUT_DIR/$TEST_CASE/$TEST_CASE.swagger.json >> $outfile 
        mydir=`pwd`
        pushd `pwd`
        cd $OUTPUT_DIR/$TEST_CASE
        wb-swagger validate $TEST_CASE.swagger.json >> $mydir/$outfile 2>&1 
        popd


    fi
done
 
