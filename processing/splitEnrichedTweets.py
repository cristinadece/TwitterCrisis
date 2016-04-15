#!/usr/bin/env python
'''
geo-events-foursquare : splitEnrichedTweets
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 4/15/16
-----------------------------


'''
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import stats_enriched_tweets

def main():
    # take params
    if len(sys.argv) != 4:
        print "You need to pass the following 3 params: <enriched-tweets> <userRelated> <locationMentionsRelated>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputUser = sys.argv[2]
    outputMention = sys.argv[3]

    #
    i = 0
    tweetIterator = stats_enriched_tweets.tweetIter(inputFile)
    with open(outputUser, 'wb') as user_f, open(outputMention, 'wb') as tweet_f:
        i += 1
        for tweet in tweetIterator:
            if stats_enriched_tweets.hasUserLocationAndUserSentiment(tweet):
                user_f.write(json.dumps(tweet) + "\n")
            if stats_enriched_tweets.hasMentionLocationAndTweetSentiment(tweet):
                tweet_f.write(json.dumps(tweet) + "\n")


if __name__ == '__main__':
    main()