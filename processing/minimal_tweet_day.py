"""
TwitterCrisis

@autor: cristina muntean
@date: 06/12/16
"""


import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import stats_enriched_tweets


def main():
    # take params
    if len(sys.argv) != 3:
        print "You need to pass the following 3 params: <enriched-tweets> <minimal print>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputUser = sys.argv[2]


    #
    i = 0
    tweetIterator = stats_enriched_tweets.tweetIter(inputFile)
    with open(outputUser, 'w') as output_file:
        i += 1
        for tweet in tweetIterator:
            clean_tweet_text = tweet["text"].replace("\t", "")
            ht = ",".join(tweet["ht"])
            day = tweet["day"]
            line = "\t".join([clean_tweet_text, ht, day])
            output_file.write(line + "\n")


if __name__ == '__main__':
    main()
