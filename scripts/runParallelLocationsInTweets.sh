#!/bin/bash

CORES=16
INPUT_DIR=/home/muntean/relevant-tweets
OUTPUT_DIR=/home/muntean/locations-in-tweets-per-day
COMMAND="time python ../stats/locationsInTweets.py"

for LINE in `ls $INPUT_DIR/*.output`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/locations-in-${OUTPUT_NAME}.csv
done
sem --wait
exit 0
