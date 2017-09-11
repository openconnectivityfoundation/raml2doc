#!/bin/bash
#
# copying all generated swagger files to top level directory.
#


copy_from=$1
#copy_from=$OUTPUT_DIR

for mydir in $copy_from/*
do
    if [[ -d $mydir ]]; then
        if [[ $mydir != "copy-resolved" ]]; then
            for file in $mydir/*.swagger.json
            do
                echo "$file"
                cp  "$file" $copy_from/.
            
            done
        fi
    fi 
done