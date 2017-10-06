#!/bin/bash

PYTHON_EXE=C:\\python27\\python.exe
RAML2DOC=../src/raml2doc.py

OUTPUT_DIR=./out
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
    compare_file $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT $REF_DIR/$TEST_CASE/$TEST_CASE$EXT
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


# array in schema
#TEST_CASE="testcase_15"
#my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_9_array/ -resource ArrayResURI -raml ../test/in/test_9_array/array-resource.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx 


# ? in url
TEST_CASE="testcase_16"
my_test -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_7_queryparaminuri/ -resource AirFlowControlResURI?if=oic.if.ll -raml ../test/in/test_7_queryparaminuri/airflowControl.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx 


}

function tests_derived {

# option -derived
TEST_CASE="test_derived_1"
my_test  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_5_derived_data_modeling/ -resource AudioVolumeResURI -raml ../test/in/test_5_derived_data_modeling/AudioVolume.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx -derived ASA

# option -derived
TEST_CASE="test_derived_2"
my_test  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_5b_derived_no_example/ -resource CurrentAirQualityResURI -raml ../test/in/test_5b_derived_no_example/AirQuality.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx -derived ASA


}

function test_resolve_reference {
# option -swagger
TEST_CASE="test_schema_1"
mkdir -p $OUTPUT_DIR_DOCS/$TEST_CASE

node node-resolver.js ./in/test_1/oic.r.switch.binary.json    > $OUTPUT_DIR_DOCS/$TEST_CASE/generated-schema.json

node node-resolver.js ./in/test_7_compound/oic.r.airflowControl-Batch.json  > $OUTPUT_DIR_DOCS/$TEST_CASE/generated-oic.r.airflowControl-Batch.json
}


function tests_swagger {

# option -swagger
TEST_CASE="test_swagger_1"
mkdir -p $OUTPUT_DIR_DOCS/$TEST_CASE
my_test_in_dir  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_1/ -resource BinarySwitchResURI -raml ../test/in/test_1/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx -swagger $OUTPUT_DIR_DOCS/$TEST_CASE/$TEST_CASE.swagger.json
compare_to_reference_file_in_dir $TEST_CASE.swagger.json $TEST_CASE

# option -swagger
TEST_CASE="test_swagger_2"
mkdir -p $OUTPUT_DIR_DOCS/$TEST_CASE
my_test_in_dir  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_2_schema_dir/schemas -resource BinarySwitchResURI -raml ../test/in/test_2_schema_dir/binarySwitch.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx -swagger $OUTPUT_DIR_DOCS/$TEST_CASE/$TEST_CASE.swagger.json
compare_to_reference_file_in_dir $TEST_CASE.swagger.json $TEST_CASE

# option -swagger
TEST_CASE="test_swagger_3"
mkdir -p $OUTPUT_DIR_DOCS/$TEST_CASE
my_test_in_dir  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_6_compound/ -resource AirFlowControlResURI -raml ../test/in/test_6_compound/airFlowControl.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx -swagger $OUTPUT_DIR_DOCS/$TEST_CASE/$TEST_CASE.swagger.json
compare_to_reference_file_in_dir $TEST_CASE.swagger.json $TEST_CASE

# option -swagger
TEST_CASE="test_swagger_4"
mkdir -p $OUTPUT_DIR_DOCS/$TEST_CASE
my_test_in_dir  -docx ../input/ResourceTemplate.docx -schemadir ../test/in/test_7_compound/ -resource AirFlowControlResURI -raml ../test/in/test_7_compound/airFlowControl.raml -outdocx $OUTPUT_DIR_DOCS/$TEST_CASE.docx -swagger $OUTPUT_DIR_DOCS/$TEST_CASE/$TEST_CASE.swagger.json
compare_to_reference_file_in_dir $TEST_CASE.swagger.json $TEST_CASE

}

tests  
tests_derived
tests_swagger
test_resolve_reference
