import codecs
from collections import defaultdict
import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import ngrams

__author__ = 'muntean'

'''
This is needed for merging the wordcount
'''

def buildWordcountDict(path, ifHashtagsOnly):
    wordcountDict = defaultdict()
    if os.path.isdir(path):
        for fname in os.listdir(path):
            inputFile = codecs.open(os.path.join(path, fname), 'r', 'utf8')
            for line in inputFile:
                data = line.split("\t")
                word = data[0]
                count = int(data[1])
                if ifHashtagsOnly:
                    if ngrams.is_hashtag(word):
                        wordcountDict[word] +=count
                else:
                    wordcountDict[word] +=count
    else:
        print "This is not a directory!"

    return wordcountDict

def writeOutputPlain(wordcountDict, outputFile):
    output = codecs.open(outputFile, "w", "utf-8")
    for k,v in wordcountDict.iteritems():
        output.write(k + "\t" + v + "\n")
    output.close()

if __name__ == '__main__':
    logger = logging.getLogger("merge-wordcount.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started counting')

    if len(sys.argv) != 4:
        print "You need to pass the following 3 params: <inputDIR> <outputFileForWordCount> <1 for hashtags only, 0 for everything>"
        sys.exit(-1)
    inputDir = sys.argv[1]
    outputFile = sys.argv[2]
    ifHashtagsOnly = sys.argv[3]

    # build user dict with hashtag set
    userLocationDict = buildWordcountDict(inputDir)

    # print to file
    writeOutputPlain(userLocationDict, outputFile)

    logger.info('Finished counting and writing to file')

