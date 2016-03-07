#!/bin/bash

CORES=16
INPUT_DIR=/data/muntean/georef-tweets/
OUTPUT_DIR=/home/muntean/locations-in-tweets-in-BB
COMMAND="time python ../filters/filterRelevantTweetsInBB.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/filterred-in-BB-in${OUTPUT_NAME}.output
done
sem --wait
exit 0