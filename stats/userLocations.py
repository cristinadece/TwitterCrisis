import sys
from util import TweetTextTokenizer

__author__ = 'cris'




def getUserLocation():
    return

if __name__ == '__main__':


    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <tweetDirectory>  <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]

    tweets = TweetTextTokenizer.getTweetAsDictionary(tweetDir)

