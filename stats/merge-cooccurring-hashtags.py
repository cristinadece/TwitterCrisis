import codecs
import sys
from collections import defaultdict, OrderedDict
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging

__author__ = 'muntean'

'''
We read USER with hashtags file, count hashtags, write to file.
We do this in order to discover new significant PRO, ANTI and NEUTRAL hashtags.

* the case here is special because for the same user we might have to lists, so we put them together and create a set
so as to remove duplicate!

Usage:
python merge-cooccurring-hashtags.py ../../output-sem-coocc-hashtags-v1/ ANTI ../../output-sem-coocc-hashtags-v1/top-ANTI-hashtags.tsv

'''

# We need to read UTF8
def buildUserHashtagsDict(path, type):
    userHashDict = defaultdict(set)
    if os.path.isdir(path):
        for fname in os.listdir(path):
            if type in fname:  # if we want ANTI hashtags we search for outputs referring only to this
                inputFile = codecs.open(os.path.join(path, fname), 'r', 'utf8')
                for line in inputFile:
                    items = line.replace('\n', '').split('\t')
                    user = items[0]
                    hashtags = set(items[1].split(','))
                    userHashDict[user].update(hashtags)
    else:
        print "This is not a directory!"

    return userHashDict

def countHashtagsFromList(userHashDict):
    hashtagFreq = defaultdict(int)
    for hashtagSet in userHashDict.itervalues():
        for hashtag in hashtagSet:
            hashtagFreq[hashtag] += 1

    return OrderedDict(sorted(hashtagFreq.items(), key=lambda t: t[1], reverse=True))

def writeOutputPlain(sortedHashtags, outputFile):
    output = codecs.open(outputFile, "w", "utf-8")
    for k,v in sortedHashtags.iteritems():
        s = k + '\t' + str(v) + '\n'
        output.write(s)
    output.close()

if __name__ == '__main__':
    logger = logging.getLogger("merge-cooccurring-hashtags.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started counting')

    if len(sys.argv) != 4:
        print "You need to pass the following 3 params: <inputDIR> <ANTI/PRO/NEUTRAL> <outputFileForHashtagCount>"
        sys.exit(-1)
    inputDir = sys.argv[1]
    type = sys.argv[2]
    outputFile = sys.argv[3]

    # build user dict with hashtag set
    userHashtagsDict = buildUserHashtagsDict(inputDir, type)

    # top hashtags per user Type <ANTI/PRO/NEUTRAL>
    sortedHashtags = countHashtagsFromList(userHashtagsDict)

    # print to file
    writeOutputPlain(sortedHashtags, outputFile)

    logger.info('Finished counting and writing to file')

