#!/bin/bash
TIME1=$(date +%s%N)

START=$(date -d "10/31/2017 10:00:00" "+%s")

cat logs*.txt | awk -F '\t' -v date1="$START" '$1>=date1 && $3 == "GET" {print $0}' | cut -f 2 | sort | uniq -c | sort -nr | head -10

TIME2=$(date +%s%N)
TIME=$(echo $TIME2 - $TIME1 | bc)
echo $TIME "nanoseconds"
