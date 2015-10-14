__author__ = 'cris'

import sys

from gensim import corpora

from twitter.Tweet import Tweet


def tfidsWithGensim(tweets):

     # create dictionary (index of each element)
    print "creating dict"
    dictionary = corpora.Dictionary(tweetsAsTokens)
    print "dict created"
    print dictionary
    print dictionary.get(30)
    dictionary.save('/tmp/tweets.dict') # store the dictionary, for future reference
    print "We create a dictionary, an index of all unique values: %s"%type(dictionary)

    # compile corpus (vectors number of times each elements appears)
    raw_corpus = [dictionary.doc2bow(t) for t in tweetsAsTokens]
    print "Then convert convert tokenized documents to vectors: %s"% type(raw_corpus)
    print raw_corpus[:10]
    corpora.MmCorpus.serialize('/tmp/tweets.mm', raw_corpus) # store to disk
    print "Save the vectorized corpus as a .mm file"
    print


if __name__ == '__main__':
    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <tweetDirectory>  <outputFileForTFTDF>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]
    tweetsAsTokens = Tweet(tweetDir)

    tfidsWithGensim(tweetsAsTokens)

