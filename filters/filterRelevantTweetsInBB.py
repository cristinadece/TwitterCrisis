import codecs
import json
import logging
import os
import sys
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet

'''
This is for geotagged raw JSON tweets
'''

eurasiaBB = [tuple([-24.08203125, 14.0939571778]), tuple([70.13671875, 66.9988437919])]

def inBB(lon, lat, boundingbox=eurasiaBB):
    """
    Checks if a coordinate [longitude, latitude] is within a Bounding Box
    :param lon:
    :param lat:
    :param boundingbox:
    :return:
    """
    lonMin = boundingbox[0][0]
    lonMax = boundingbox[1][0]
    latMin = boundingbox[0][1]
    latMax = boundingbox[1][1]
    return lonMin < lon < lonMax and latMin < lat < latMax


def isBBinBB(tweet_bb, boundingbox=eurasiaBB):
    # [[33.9105011, -4.7672356], [33.9105011, 4.631608], [41.8998666, 4.631608], [41.8998666, -4.7672356]] - kenya
    lonMin = tweet_bb[0][0]
    lonMax = tweet_bb[2][0]
    latMin = tweet_bb[0][1]
    latMax = tweet_bb[2][1]
    return inBB(lonMin, latMin, boundingbox) and inBB(lonMax, latMax, boundingbox)


def isValidLocation(tweet):
    tweet_place_bb = tweet["place"]["bounding_box"]["coordinates"][0]  # list of coordinates [longitude, latitude]
    return isBBinBB(tweet_place_bb)


def getLocationData(tweet):
    """
    These can always have None values; e.g no coordinates, no city, no user location
    :param tweet:
    :return:
    """
    if tweet["coordinates"] is not None:
        tweet_coords = tweet['coordinates']['coordinates']  # returns a list [longitude, latitude]
    else:
        tweet_coords = None

    if tweet["place"] is not None:
        if tweet["place"]["place_type"] == "city":
            tweet_place_city = tweet["place"]["name"]  # if place type == city
            tweet_place_country = tweet["place"]["country"]
            tweet_place_country_code = tweet["place"]["country_code"]
        else:
            tweet_place_city = None
            tweet_place_country = tweet["place"]["country"]
            tweet_place_country_code = tweet["place"]["country_code"]
    else:
        tweet_place_city = None
        tweet_place_country = None
        tweet_place_country_code = None

    user_location = tweet['user']['location']

    return tweet_coords, tweet_place_city, tweet_place_country, tweet_place_country_code, user_location


def loadHashtags():
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
def filterRelevanceinBB(allHtList, tweet):
    tweetDict = dict()
    tweetText = tweet["text"]
    tweetTextTokens = Tweet.tokenizeTweetText(tweetText)
    # if any(r in tweetText for r in allHtList):
    if any(token in allHtList for token in tweetTextTokens):
        if isValidLocation(tweet):
            tweetDict["id_str"] = tweet["id_str"]
            tweetDict["text"] = tweetText
            tweetDict["tokenized_text"] = tweetTextTokens
            tweetDict["created_at"] = tweet["created_at"]
            tweetDict["place"] = tweet["place"]
            tweetDict["hashtags"] = tweet["entities"]["hashtags"]
            tweetDict["user_id"] = tweet["user"]["id_str"]
            tweetDict["screen_name"] = tweet["user"]["screen_name"]
            tweet_coords, tweet_place_city, tweet_place_country, tweet_place_country_code, user_location = getLocationData(tweet)
            tweetDict["tweet_coords"] = tweet_coords
            tweetDict["tweet_place_city"] = tweet_place_city
            tweetDict["tweet_place_country"] = tweet_place_country
            tweetDict["tweet_place_country_code"] = tweet_place_country_code
            tweetDict["user_location"] = user_location

    return tweetDict


# mauro
# lowercase, tokenization from util - keep everything coherent
# fields: user_id, screen_name, text, data, id tweet, entities: dict{coord, location, user, hashtags}
def filterRelevanceNoBB(allHtList, tweet):
    tweetDict = dict()
    tweetText = tweet["text"]
    tweetTextTokens = Tweet.tokenizeTweetText(tweetText)
    # if any(r in tweetText for r in allHtList):
    if any(token in allHtList for token in tweetTextTokens):
        tweetDict["id_str"] = tweet["id_str"]
        tweetDict["text"] = tweetText
        tweetDict["tokenized_text"] = tweetTextTokens
        tweetDict["hashtags"] = tweet["entities"]["hashtags"]

        tweetDict["created_at"] = tweet["created_at"]

        tweetDict["user_id"] = tweet["user"]["id_str"]
        tweetDict["screen_name"] = tweet["user"]["screen_name"]

        tweet_coords, tweet_place_city, tweet_place_country, tweet_place_country_code, user_location = getLocationData(tweet)
        tweetDict["user_location"] = user_location

        tweetDict["place"] = tweet["place"]
        tweetDict["tweet_coords"] = tweet_coords
        tweetDict["tweet_place_city"] = tweet_place_city
        tweetDict["tweet_place_country"] = tweet_place_country
        tweetDict["tweet_place_country_code"] = tweet_place_country_code

    return tweetDict


def dumpDictValuesToFile(dict, file):
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


    htDict = loadHashtags()
    # print htDict
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)

    i = 0
    for tweet in tweetsAsDict:
        relevantTweetDict = filterRelevanceNoBB(htDict["All"], tweet)
        if bool(relevantTweetDict):  # the dict is not empty
            dumpDictValuesToFile(relevantTweetDict, outputRelevant)
    outputRelevant.close()

