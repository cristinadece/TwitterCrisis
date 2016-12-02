#!/bin/bash

CORES=16
INPUT_DIR=/data/muntean/brexit-filtered
OUTPUT_DIR=/data/muntean/brexit-enriched
COMMAND="time python enrich_relevant_tweet.py"

for LINE in `ls $INPUT_DIR/*.output`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/enriched-brexit-in${OUTPUT_NAME}.output
done
sem --wait
exit 0