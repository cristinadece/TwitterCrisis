#!/bin/bash

CORES=6
#INPUT_DIR=/home/muntean/english-tweets-09
INPUT_DIR=/data/muntean/tweets
OUTPUT_DIR=/home/muntean/output-sem-user-loc
COMMAND="python ../processing/userLocations.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/${OUTPUT_NAME}.output
done
sem --wait
exit 0
