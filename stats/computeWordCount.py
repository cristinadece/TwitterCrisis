import codecs

__author__ = 'cris'

import sys
from collections import defaultdict
import operator
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet
from util import ngrams
import logging

'''
We read JSON files from directory, get the text, tokenize it and compute WordCount

'''

def wordcountPlain(tweets, outputfile, onlyHashtags=False, ngram=1):
    wordcount = defaultdict(int)
    output = codecs.open(outputfile, "w", "utf-8")
    i=0
    for tweet in tweets:
        i+=1
        if i%10000==0:
            print 'processing tweets: ', i
        tokenList = [t for t in tweet if (len(t) > 2 and (not ngrams.is_url_or_mention(t)))]
        if ngram>1:
            for ng in range(1,ngram):
                tokenList = tokenList + [ntoken for ntoken in ngrams.window_no_twitter_elems(tweet, ng+1)]

        for token in tokenList: # len(token) > 2
            if onlyHashtags:
                if token.startswith('#'):
                    wordcount[token] += 1
                else:
                    continue
            else:
                wordcount[token] += 1
    print "Total words" , len(wordcount)
    sorted_wc = sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)
    for k,v in sorted_wc:
        # todo json load, dump
        output.write(u'{}\t{}\n'.format(k,v)) #.encode('utf-8',errors='ignore'))
    output.close()

if __name__ == '__main__':
    logger = logging.getLogger("computerWordCount.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started counting')

    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <tweetDirectory> <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]

    tweetsAsTokens = Tweet.getTweetAsTweetTextTokens(tweetDir)

    wordcountPlain(tweetsAsTokens, output, False, 2)

    logger.info('Finished counting and writing to file')
