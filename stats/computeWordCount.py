__author__ = 'cris'

import sys
from TweetTextTokenizer import TweetTextTokenizer
from collections import defaultdict
import operator
from util import ngrams

'''
We read JSON files from directory, get the text, tokenize it and compute WordCount

'''

def wordcountPlain(tweets, outputfile, onlyHashtags=False, ngram=1):
    wordcount = defaultdict(int)
    output = open(outputfile, 'w')
    i=0
    for tweet in tweets:
        i+=1
        if i%10000==0:
            print 'processing tweets: ', i
        tokenList = [t for t in tweet if len(t) > 2]
        if ngram>1:
            for ng in range(1,ngram):
                tokenList = tokenList + [ntoken for ntoken in ngrams.window(tweet, ng+1)]

        for token in tokenList: # len(token) > 2
            if onlyHashtags and token.startswith('#'):
                    wordcount[token] += 1
            else:
                wordcount[token] += 1
    print "Total words" , len(wordcount)
    sorted_wc = sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)
    for k,v in sorted_wc:
        output.write(u'{}\t{}\n'.format(k,v).encode('utf-8'))
    output.close()

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <tweetDirectory>  <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]
    tweetsAsTokens = TweetTextTokenizer(tweetDir)

    wordcountPlain(tweetsAsTokens, output, True, 1)


