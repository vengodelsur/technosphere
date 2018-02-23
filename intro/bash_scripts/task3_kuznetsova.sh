#!/bin/bash
TIME1=$(date +%s%N)

cd data_for_cool_science
FILES=$(ls -s | sort -nr | head -3 | cut -d' ' -f 2)
awk -F '\t' '$1=="bad" {print $0}' $FILES | cut -f 2 | tr "[:upper:]" "[:lower:]" | tr "," "\n" | sort | uniq | wc -l

TIME2=$(date +%s%N)
TIME=$(echo $TIME2 - $TIME1 | bc)
echo $TIME "nanoseconds"

