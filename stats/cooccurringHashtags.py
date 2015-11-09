import codecs
from collections import defaultdict, Counter
import json
import logging
import sys
import os
import itertools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import ngrams
from twitter.Tweet import Tweet


__author__ = 'cris'

'''
This script computes cooccuring hashtags (from relevant users) with few preselected
Run it:
<python cooccurringHashtagsByUsers.py ../../../../english-tweets ../../../../users-by-type.json
../../../../cooc-hashtags-Pro.json ../../../../cooc-hashtags-Anti.json ../../../../cooc-hashtags-Neutral.json>

Parallel version:
./runParallelCooccurringHashtags.sh

'''

neutral_refugee = ['#refugeescrisis', '#syrianrefugees', '#refugees']
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad']


def tagHashtagsOnCooccurrencePerType(tweetsAsDictionary):
    anti_hashtagsDict = defaultdict(int)
    pro_hashtagsDict = defaultdict(int)
    neutral_hashtagsDict = defaultdict(int)


    for tweet in tweetsAsDictionary:
        tweetText = tweet['text'].lower()
        tweetTokens = Tweet.tokenizeTweetText(tweetText)
        hashtags = set([x for x in tweetTokens if x.startswith('#')])

        if len(hashtags) != 0:
            if not hashtags.isdisjoint(anti_refugee):
                for tag in hashtags:
                    if tag not in anti_refugee:
                        anti_hashtagsDict[tag] += 1
            if not hashtags.isdisjoint(pro_refugee):
                for tag in hashtags:
                    if tag not in pro_refugee:
                        pro_hashtagsDict[tag] += 1
            if not hashtags.isdisjoint(neutral_refugee):
                for tag in hashtags:
                    if tag not in neutral_refugee:
                        neutral_hashtagsDict[tag] += 1

    return [anti_hashtagsDict, pro_hashtagsDict, neutral_hashtagsDict]

'''
the summing up may not addup to whole freq in case of duplicates of seeds in same tweet
e.g. i don't know #refugees #refugees #italy
'''
def tagHashtagsOnCooccurrence(tweetsAsDictionary):
    coocurences = defaultdict(list)  # keys are hashtags, values are lists of seed hashtags
    seeds = set(itertools.chain(pro_refugee, anti_refugee, neutral_refugee))

    i = 0
    for tweet in tweetsAsDictionary:
        i += 1
        if i % 10000 == 0:
            print 'processing tweets: ', i
        tweetText = tweet['text'].lower()
        tweetTokens = Tweet.tokenizeTweetText(tweetText)
        hashtags = set([x for x in tweetTokens if x.startswith('#')])

        if len(hashtags) > 1 :  #this means they co-occur, at least 2 hashtags
            seeds_in_hashtags = hashtags.intersection(seeds)  #seeds in tweet ; this return unique - not counting repetitions inside tweets
            if len(seeds_in_hashtags) != 0:
                other_hashtags = hashtags.difference(seeds_in_hashtags)
                for tag in other_hashtags:
                    coocurences[tag].extend(list(seeds_in_hashtags))

    return coocurences



def writeCoocurrencesInOutput(coocurences, outputFile):
    output = codecs.open(outputFile, "w", "utf-8")
    for hashtag, cooccurenceList in coocurences.iteritems():
        countCoocs = Counter(cooccurenceList)
        coocTypes = defaultdict(int)

        for k,v in countCoocs.iteritems():
            if k in anti_refugee:
                coocTypes["Anti"] += v
            if k in pro_refugee:
                coocTypes["Pro"] += v
            if k in neutral_refugee:
                coocTypes["Neutral"] += v

        freqs = ' '.join('{}:{}'.format(key, val) for key, val in coocTypes.items())
        coocs = ','.join(countCoocs.keys())
        output.write('{}\t{}\t{}\n'.format(hashtag, freqs, coocs))
    output.close()


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Need to pass the following params: <tweetDirectory> <outputCoocFile> "
        sys.exit(-1)
    tweetDir = sys.argv[1]
    outputFile = sys.argv[2]


    logger = logging.getLogger("cooccurringHashtags.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Computing hashtag cooccurences')

    tweetsAsDictionary = Tweet.getTweetAsDictionary(tweetDir)
    coocDicts = tagHashtagsOnCooccurrence(tweetsAsDictionary)
    writeCoocurrencesInOutput(coocDicts, outputFile)

    logger.info("Finished writing to file")
