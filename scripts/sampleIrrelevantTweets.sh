#!/bin/bash

INPUT_DIR=/home/muntean/output-sem-filter
OUTPUT_DIR=/home/muntean/output-sem-filter

for LINE in `ls $INPUT_DIR/tagged-english-tweets-*.output`
do
        OUTPUT_NAME=`basename $LINE | cut -d'.' -f1 | cut -d'-' -f4`
        NUM_LINES=`wc -l $LINE | cut -d' ' -f1`
        # sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/${OUTPUT_NAME}.output
        echo $OUTPUT_NAME, $NUM_LINES
        shuf -n $NUM_LINES taggedNonRelevant-english-tweets-$OUTPUT_NAME.output > taggedNonRelevant-english-tweets-$OUTPUT_NAME.sample.output
done

exit 0