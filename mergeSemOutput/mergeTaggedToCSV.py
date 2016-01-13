import codecs
import json
from collections import defaultdict
import logging
import os
import sys
from itertools import izip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import ngrams

__author__ = 'muntean'

'''
This is needed for merging the tagged tweets
'''

def formatCSVLine(jsonDict):
    id_str = jsonDict["id_str"]
    text = jsonDict["text"].replace(",", " ")
    sensitive = jsonDict["sensitive"]
    tag = jsonDict["tag"]
    csv_line = ",".join([id_str, text, sensitive, tag]) + "\n"
    return csv_line


if __name__ == '__main__':
    logger = logging.getLogger("mergeTaggedToCSV.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started merging')

    if len(sys.argv) != 3:
        print "You need to pass the following 2 params: <inputDIR> <outputFileCVS>"
        sys.exit(-1)
    inputDir = sys.argv[1]
    outputFile = sys.argv[2]
    output = codecs.open(outputFile, "w", "utf-8")

    if os.path.isdir(inputDir):
        for fname in os.listdir(inputDir):
            if "tagged-english-tweets" in fname:
                day = fname.split("-")[3].split(".")[0]
                irrelevantFilename = "taggedNonRelevant-english-tweets-" + day + ".sample.output"
                with open(fname) as textfile1, open(irrelevantFilename) as textfile2:
                    for x, y in izip(textfile1, textfile2):
                        line1 = json.loads(x.strip())
                        line2 = json.loads(y.strip())
                        output.write(formatCSVLine(line1))
                        output.write(formatCSVLine(line2))
    else:
        print "This is not a directory!"

    output.close()
    logger.info('Finished merging')



