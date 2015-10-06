#!/usr/bin/env python
import gzip
import json
import os
from tokenizer import twokenize

stopwords=open('../resources/stop-word-list.txt', 'r').read().decode('utf-8').split('\r\n')

__author__ = 'cris'

class TweetTextTokenizer:
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in gzip.open(os.path.join(self.dirname, fname)):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]

                tweetText = tweet['text']
                tokenizedTweettext = [t for t in twokenize.tokenize(tweetText.lower()) if t not in stopwords]
                yield tokenizedTweettext

    def getTweetAsDictionary(self):
         for fname in os.listdir(self.dirname):
            for line in gzip.open(os.path.join(self.dirname, fname)):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]
                yield tweet




if __name__ == '__main__':
    #print stopwords

    tweetsAsTokens = TweetTextTokenizer("../../../english-tweets")
    for i in tweetsAsTokens:
        print i
        break

    j=0
    for i in tweetsAsTokens.getTweetAsDictionary():
        j+=1
        print i['user']['id_str']
        print i['user']['location']


        print i['place'] # https://dev.twitter.com/overview/api/places
            # "name":"Washington",
            # "place_type":"city",


        print i['coordinates']
        # "coordinates":
        #     {
        #         "coordinates":
        #         [
        #             -75.14310264,
        #             40.05701649
        #         ],
        #         "type":"Point"
        #     }

        if j%10==0:
            break


