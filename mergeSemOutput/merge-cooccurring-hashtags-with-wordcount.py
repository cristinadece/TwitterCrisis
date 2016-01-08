import codecs
import json
import sys
from collections import defaultdict, OrderedDict
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging

__author__ = 'muntean'

'''


Usage:
python merge-cooccurring-hashtags-with-wordcount.py ../../output-sem-coocc-hashtags-09/ ../../hashtags-wc.tsv ../../merged-hashtags-coocurence-with-wordcount.tsv

'''

def loadWC(wordcountFile):
    hashtagWCFreq = defaultdict(int)
    input = codecs.open(wordcountFile, "r", "utf-8")
    for line in input:
        hashtagCount = line.split('\t')
        hashtagWCFreq[hashtagCount[0]] += int(hashtagCount[1])
    return hashtagWCFreq

# each line is smth like this:
# #migrants       7       Neutral:6 Pro:1   #refugees,#refugeeswelcome
# we load a dict <hashtag, list[corresponding strings form different files]> without parsing the values
def loadHashtagDict(path):
    hashtagDict = defaultdict(list)
    if os.path.isdir(path):
        for fname in os.listdir(path):
            inputFile = codecs.open(os.path.join(path, fname), 'r', 'utf8')
            for line in inputFile:
                items = line.replace('\n', '').split('\t', 1)
                hashtag = items[0]
                hashtagData = items[1]
                hashtagDict[hashtag].append(hashtagData)
    else:
        print "This is not a directory!"

    return hashtagDict

def mergeAndPrintHashtagsStats(hashtagDict, wordcountDict, outputFile):
    output = codecs.open(outputFile, "w", "utf-8")
    coocTypes = defaultdict(int)  # create this one time, then clear after each record

    for hashtag, hashtagData in hashtagDict.iteritems():
        if len(hashtagData) > 1:

            freqTotal = 0
            coocSeeds = set()

            for item in hashtagData:
                totalCoocFreq, freqByCateg, seedList = item.split('\t')
                freqTotal += int(totalCoocFreq)
                coocSeeds.update(seedList.split(','))
                typeFreq = freqByCateg.split(' ')
                for entry in typeFreq:
                    miniFreqs = entry.split(':')
                    coocTypes[miniFreqs[0]] += int(miniFreqs[1])

            freqs = ' '.join('{}:{}'.format(key, val) for key, val in coocTypes.items())
            coocs = ','.join(coocSeeds)

            output.write('{}\t{}\t{}\t{}\t{}\n'.format(hashtag, freqTotal, freqs, coocs, wordcountDict[hashtag]))
            coocTypes.clear()
        else:
            output.write('{}\t{}\t{}\n'.format(hashtag, hashtagData[0], wordcountDict[hashtag]))
    output.close()


if __name__ == '__main__':
    logger = logging.getLogger("merge-cooccurring-hashtags-with-wordcount.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started counting')

    if len(sys.argv) != 4:
        print "You need to pass the following 3 params: <inputDIR> <hashtags-wordcount> <outputFileForHashtagCount>"
        sys.exit(-1)
    inputDir = sys.argv[1]
    wordcountFile = sys.argv[2]
    outputFile = sys.argv[3]

    # load wordcount
    wcDict = loadWC(wordcountFile)
    print "Loaded Wordcount"

    # merging hashtags from multiple files in a dict
    hashtagsDict = loadHashtagDict(inputDir)
    print "Num of hashtags: ", len(hashtagsDict)

    # count global frequencies and print to file
    mergeAndPrintHashtagsStats(hashtagsDict, wcDict, outputFile)

    logger.info('Finished counting and writing to file')

