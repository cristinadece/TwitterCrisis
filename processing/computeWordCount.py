import codecs
import json
import sys
from collections import defaultdict
import operator
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet
from util import ngrams
import logging


__author__ = 'cris'


'''
We read JSON files from directory, get the text, tokenize it and compute WordCount

'''

def printJson(sorted_wc, outputfile):
    output = open(outputfile, "w")
    for item in sorted_wc:
        output.write(json.dumps(item) + '\n')
    output.close()


def printTSV(sorted_wc, outputfile):
    output = codecs.open(outputfile, "w", "utf-8")
    for k, v in sorted_wc:
        output.write(u'{}\t{}\n'.format(k, v))  #.encode('utf-8',errors='ignore'))
    output.close()

def printUTF8(sorted_wc, outputfile):
    output = codecs.open(outputfile, "w", "utf-8")
    for k, v in sorted_wc:
        output.write('{}\t{}\n'.format(json.dumps(k).replace('"', ''), v))  #.encode('utf-8',errors='ignore'))
    output.close()

def wordcountPlain(tweets, onlyHashtags=False, ngram=1):
    wordcount = defaultdict(int)

    i = 0
    for tweet in tweets:
        i += 1
        if i % 10000 == 0:
            print 'processing tweets: ', i
        tokenList = [t for t in tweet if (len(t) > 2 and (not ngrams.is_url_or_mention(t)))]
        if ngram > 1:
            for ng in range(1, ngram):
                tokenList = tokenList + [ntoken for ntoken in ngrams.window_no_twitter_elems(tweet, ng + 1)]

        for token in tokenList:  # len(token) > 2
            if onlyHashtags:
                if token.startswith('#'):
                    wordcount[token] += 1
                else:
                    continue
            else:
                wordcount[token] += 1
    print "Total words", len(wordcount)
    sorted_wc = sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_wc

if __name__ == '__main__':
    logger = logging.getLogger("computerWordCount.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started counting')

    if len(sys.argv) != 3:
        print "You need to pass the following 2 params: <tweetDirectory> <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]

    tweetsAsTokens = Tweet.getTweetAsTweetTextTokensNoGZ(tweetDir)

    sorted_wordcount = wordcountPlain(tweetsAsTokens, False, 2)
    # printTSV(sorted_wordcount, output)
    # printJson(sorted_wordcount, output)
    printUTF8(sorted_wordcount, output)

    logger.info('Finished counting and writing to file')
