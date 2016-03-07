import codecs
import json
import logging
import os
import sys
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tokenizer import twokenize
from twitter.Tweet import Tweet
from util import worldLocations

'''
This is for geotagged raw JSON tweets
'''

def userLocationInBB(tweet, wl):
    """

    :param tweet:
    :param wl:
    :return:
    """
    user_loc = tweet['user']['location']
    if user_loc==None:
        return None
    else:
        potential_cities = [t.capitalize() for t in twokenize.tokenize(user_loc)]
        for city in potential_cities:
            if city in wl.keys():
                return city
            else:
                return None


def loadHashtags():
    """

    :return:
    """
    htDict = defaultdict(list)
    with open("../resources/kw.txt") as f:
        for line in f:
            htType = line.split(":")[0]
            hashtagsString = line.split(":")[1].replace("\n", "")
            hashtags = hashtagsString.replace("\'", "").replace(" ", "").split(",")
            htDict[htType].extend(hashtags)
            htDict["All"].extend(hashtags)

    return htDict


# mauro
# lowercase, tokenization from util - keep everything coherent
# fields: user_id, screen_name, text, data, id tweet, entities: dict{coord, location, user, hashtags}
def filterRelevanceinBB(allHtList, tweet, wl):
    """

    :param allHtList:
    :param tweet:
    :param wl:
    :return:
    """
    tweetDict = dict()
    tweetText = tweet["text"]
    tweetTextTokens = Tweet.tokenizeTweetText(tweetText)
    # if any(r in tweetText for r in allHtList):
    user_location = userLocationInBB(tweet, wl)
    if any(token in allHtList for token in tweetTextTokens) and user_location!=None:
        tweetDict["id_str"] = tweet["id_str"]
        tweetDict["text"] = tweetText
        tweetDict["tokenized_text"] = tweetTextTokens
        tweetDict["created_at"] = tweet["created_at"]
        tweetDict["place"] = tweet["place"]
        tweetDict["hashtags"] = tweet["entities"]["hashtags"]
        tweetDict["user_id"] = tweet["user"]["id_str"]
        tweetDict["screen_name"] = tweet["user"]["screen_name"]
        tweetDict["user_location"] = user_location
        if tweet["coordinates"] is not None:
            tweet_coords = tweet['coordinates']['coordinates']  # returns a list [longitude, latitude]
        else:
            tweet_coords = None
        tweetDict["tweet_coords"] = tweet_coords
    return tweetDict


def dumpDictValuesToFile(dict, file):
    """

    :param dict:
    :param file:
    :return:
    """
    line = json.dumps(dict) + "\n"
    file.write(line)


if __name__ == '__main__':
    logger = logging.getLogger("filterRelevantTweets.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 3:
        print "You need to pass the following 2 params: <jsonTweetsFile> <filteredTweetsFile> "
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputRelevant = codecs.open(sys.argv[2], "w", "utf-8")

    wl = worldLocations.Locations.loadFromFile()
    print "Loaded city dict", len(wl)

    htDict = loadHashtags()
    # print htDict
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)

    i = 0
    for tweet in tweetsAsDict:
        relevantTweetDict = filterRelevanceinBB(htDict["All"], tweet)
        if bool(relevantTweetDict):  # the dict is not empty
            dumpDictValuesToFile(relevantTweetDict, outputRelevant)


    outputRelevant.close()

