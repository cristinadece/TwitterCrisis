__author__ = 'muntean'

import sys
from collections import defaultdict, OrderedDict
import operator
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet
from util import ngrams
import logging

'''
We read USER with hashtags file, count hashtags, write to file.
We do this in order to discover new significant PRO, ANTI and NEUTRAL hashtags.

'''

def countHashtagsFromList(filename):
    hashtagFreq = defaultdict(int)
    for line in open(filename, 'r'):
        hashtagList = line.split('\t')[1]
        print hashtagList
        # convert it to real list

        for hashtag in hashtagList:
            print hashtag
            hashtagFreq[hashtag] += 1

    return OrderedDict(sorted(hashtagFreq.items(), key=lambda t: t[1]), reverse=True)

if __name__ == '__main__':
    logger = logging.getLogger("computerHashtags.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started counting')

    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <inputFile> <outputFileForHashtagCount>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    sortedHashtags = countHashtagsFromList(inputFile)
    print len(sortedHashtags), sortedHashtags
    for k,v in sortedHashtags:
        outputFile.write('{}\t{}\n'.format(k,v).encode('utf-8'))
    outputFile.close()

    logger.info('Finished counting and writing to file')

