#!/bin/bash

CORES=16
INPUT_DIR=/data/muntean/tweets
OUTPUT_DIR=/home/muntean/output-sem-coocc-hashtags-by-users
COMMAND="time python ../processing/cooccurringHashtagsByUsers.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/user-type-${OUTPUT_NAME}.output $OUTPUT_DIR/${OUTPUT_NAME}-PRO-hashtags.output $OUTPUT_DIR/${OUTPUT_NAME}-ANTI-hashtags.output $OUTPUT_DIR/${OUTPUT_NAME}-NEUTRAL-hashtags.output
done
sem --wait
exit 0
