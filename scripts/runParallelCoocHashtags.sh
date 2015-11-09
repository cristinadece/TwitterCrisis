#!/usr/bin/env bash


CORES=27
#INPUT_DIR=/home/muntean/english-tweets-09
INPUT_DIR=/data/tweets
OUTPUT_DIR=/home/muntean/output-sem-coocc-hashtags-09
COMMAND="time python ../stats/cooccuringHashtags.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/user-type-${OUTPUT_NAME}.output $OUTPUT_DIR/${OUTPUT_NAME}-PRO-hashtags.output $OUTPUT_DIR/${OUTPUT_NAME}-ANTI-hashtags.output $OUTPUT_DIR/${OUTPUT_NAME}-NEUTRAL-hashtags.output
done
sem --wait
exit 0
