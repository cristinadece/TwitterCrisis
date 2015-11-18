#!/bin/bash

CORES=16
INPUT_DIR=/data/muntean/tweets
OUTPUT_DIR=/home/muntean/output-sem-wordcount
COMMAND="time python ../stats/computeWordCount.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/${OUTPUT_NAME}.output
done
sem --wait
exit 0
