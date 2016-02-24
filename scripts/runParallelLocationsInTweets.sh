#!/bin/bash

CORES=16
INPUT_DIR=/home/muntean/relevant-tweets
OUTPUT_DIR=/home/muntean/output-sem-filter
COMMAND="time python ../stats/locationsInTweets.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/locations-in-tweets-${OUTPUT_NAME}.csv
done
sem --wait
exit 0