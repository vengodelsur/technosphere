#!/bin/bash
TIME1=$(date +%s%N)

FILES=$(find . -type f -name "*.tsv" -size +10M)
for file in $FILES; do
    (cd $(dirname $file) && zip $(basename $file.zip) $(basename $file) -q)
done

TIME2=$(date +%s%N)
TIME=$(echo $TIME2 - $TIME1 | bc)
echo $TIME "nanoseconds"
