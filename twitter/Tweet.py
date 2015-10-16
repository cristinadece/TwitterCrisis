#!/usr/bin/env python
import gzip
import json
import os
from tokenizer import twokenize

#stopwords=open('../resources/stop-word-list.txt', 'r').read().decode('utf-8').split('\r\n')

dir = os.path.dirname(__file__)
stopwordsFile = os.path.join(dir, '../resources/stop-word-list.txt')
stopwords = open(stopwordsFile, 'r').read().decode('utf-8').split('\r\n')

__author__ = 'cris'

class Tweet:

    @staticmethod
    def tokenizeTweetText(tweetText):
        return [t for t in twokenize.tokenize(tweetText.lower()) if t not in stopwords]

    @staticmethod
    def getTweetAsTweetTextTokens(path): #todo this is the same as __iter__ , iter should be replaced by this

        if os.path.isdir(path):
            for fname in os.listdir(path):
                for line in gzip.open(os.path.join(path, fname)):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]

                    tweetText = tweet['text']
                    tokenList = Tweet.tokenizeTweetText(tweetText)
                    yield tokenList
        else: #this means it is a file
            for line in gzip.open(path):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]

                    tweetText = tweet['text']
                    tokenList = Tweet.tokenizeTweetText(tweetText)
                    yield tokenList



    @staticmethod
    def getTweetAsDictionary(path):
        if os.path.isdir(path):
             for fname in os.listdir(path):
                for line in gzip.open(os.path.join(path, fname)):
                    try:
                        tweet = json.loads(line)
                    except:
                        print "Couldn't parse tweet: ", line[:200]
                    yield tweet
        else:
            for line in gzip.open(path):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]
                yield tweet

if __name__ == '__main__':
    #print stopwords


    tweetsAsTokens = Tweet.getTweetAsTweetTextTokens("../../../english-tweets")
    for i in tweetsAsTokens:
        print i
        break

    j=0
    for i in Tweet.getTweetAsDictionary("../../../english-tweets/sample/90-tweets.json.gz"):
        j+=1
        print j
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


