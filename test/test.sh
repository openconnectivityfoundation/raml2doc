#!/bin/bash

PYTHON_EXE=C:\\python27\\python.exe
RAML2DOC=../src/raml2doc.py

OUTPUT_DIR=./out
OUTPUT_DIR_DOCS=../test/$OUTPUT_DIR
REF_DIR=./ref
EXT=.txt

function compare_output {
    diff -w $OUTPUT_DIR/$TEST_CASE$EXT $REF_DIR/$TEST_CASE$EXT
    echo "$TEST_CASE $?"
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


TEST_CASE="testcase_1"

function tests {

# option -h
TEST_CASE="testcase_1"
my_test -h

# default docx 
TEST_CASE="testcase_2"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml

# option -outdcx
TEST_CASE="testcase_3"
my_test  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx
#compare_file $OUTPUT_DIR/$TEST_CASE.docx $REF_DIR/$TEST_CASE.docx 

# option --annex
TEST_CASE="testcase_4"
my_test  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml --annex true -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx

# option -schemadir subdirectory for schemas
TEST_CASE="testcase_5"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_2_schema_dir/schemas -resource BinarySwitchResURI -raml ../test/in/test_2_schema_dir/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx

# error in validation of payload against schema
TEST_CASE="testcase_6"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_3_error -resource BinarySwitchResURI -raml ../test/in/test_3_error/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx

# option --sensor
TEST_CASE="testcase_7"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --sensor true

# option -- heading
TEST_CASE="testcase_8"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --heading1 "my_new_heading"

# option -- heading and --annex
TEST_CASE="testcase_9"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --heading1 "my_new_heading"  --annex true

# option -- put
TEST_CASE="testcase_10"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_4_put/ -resource BinarySwitchResURI -raml ../test/in/test_4_put/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --put true

# option --schema - one file
TEST_CASE="testcase_11"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --schema ../test/in/test_1/oic.core.json

# option --schema - two files
TEST_CASE="testcase_12"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --schema ../test/in/test_1/oic.core.json ../test/in/test_1/oic.baseResource.json

# option --schemaWT - one file
TEST_CASE="testcase_13"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --schemaWT ../test/in/test_1/oic.core.json

# option --schemaWT - two files
TEST_CASE="testcase_14"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx --schemaWT ../test/in/test_1/oic.core.json ../test/in/test_1/oic.baseResource.json

}

function tests_derived {

# option -outdcx
TEST_CASE="test_derived_1"
my_test  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_5_derived_data_modeling/ -resource AudioVolumeResURI -raml ../test/in/test_5_derived_data_modeling/AudioVolume.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx -derived ASA

}


tests  
tests_derived
