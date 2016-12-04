#!/bin/bash

CORES=17
INPUT_DIR=/home/muntean/brexit-rojo/
OUTPUT_DIR=/home/muntean/brexit-filtered
COMMAND="time python ../filters/filterRelevantTweetsInBB.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/filtered-no-BB-in${OUTPUT_NAME}.output
done
sem --wait
exit 0