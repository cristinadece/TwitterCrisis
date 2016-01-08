import codecs
import json
import logging
import os
import sys
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet


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
def filterRelevance(allHtList, tweet):
    tweetDict = dict()
    tweetText = tweet["text"]
    tweetTextTokens = Tweet.tokenizeTweetText(tweetText)
    # if any(r in tweetText for r in allHtList):
    if any(token in allHtList for token in tweetTextTokens):
        tweetDict["id_str"] = tweet["id_str"]
        tweetDict["text"] = tweetText
        tweetDict["tokenized_text"] = tweetTextTokens
        tweetDict["created_at"] = tweet["created_at"]
        tweetDict["place"] = tweet["place"]
        tweetDict["hashtags"] = tweet["entities"]["hashtags"]
        tweetDict["user_id"] = tweet["user"]["id_str"]
        tweetDict["screen_name"] = tweet["user"]["screen_name"]
    return tweetDict


# andrea
# fields:
def filterHashtagType(htDict, tweet):
    tweetDict = dict()
    tweetText = tweet["text"]
    tweetTextTokens = Tweet.tokenizeTweetText(tweetText)
    # if any(r in tweetText for r in allHtList):
    tags = []
    for token in tweetTextTokens:
        if token in htDict["Anti"]:
            tags.append("Anti")
        if token in htDict["Pro"]:
            tags.append("Pro")
        if token in htDict["Neutral"]:
            tags.append("Neutral")

    tag_set = set(tags)
    tweetDict["text"] = tweetText
    tweetDict["tokenized_text"] = tweetTextTokens
    tweetDict["hashtags"] = Tweet.getHashtags(tweetText)
    tweetDict["sensitive"] = tweet["possibly_sensitive"]

    if len(tag_set) == 1:  # this means it is not ambiguous
        tweetDict["tag"] = tags[0]
        return [1, tweetDict]

    if len(tags) == 0:  # this means it is irrelevant
        tweetDict["tag"] = "irrelevant"
        return [0, tweetDict]

    if len(tag_set) == 2 and "Neutral" in tag_set:  # this means it's ambiguous
        print tag_set, tweetDict
        if "Pro" in tag_set:
            tweetDict["tag"] = "NeutralPro"
            return [2, tweetDict]
        elif "Anti" in tag_set:
            tweetDict["tag"] = "NeutralAnti"
            return [2, tweetDict]

    return [3, tweetDict]

def dumpDictValuesToFile(dict, file):
    line = json.dumps(dict) + "\n"
    file.write(line)


if __name__ == '__main__':
    logger = logging.getLogger("filterRelevantTweets.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 5:
        print "You need to pass the following 4 params: <jsonTweetsFile> <filteredTweetsFile> <taggedTweetsFile> <taggedTweetsNonRelevantFile>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputRelevant = codecs.open(sys.argv[2], "w", "utf-8")
    outputTagged = codecs.open(sys.argv[3], "w", "utf-8")
    outputTaggedNonRelevant = codecs.open(sys.argv[4], "w", "utf-8")

    htDict = loadHashtags()
    print htDict
    tweetsAsDict = Tweet.getTweetAsDictionary(inputFile)

    i = 0
    for tweet in tweetsAsDict:
        relevantTweetDict = filterRelevance(htDict["All"], tweet)
        if bool(relevantTweetDict):  # the dict is not empty
            dumpDictValuesToFile(relevantTweetDict, outputRelevant)
        taggedTweetDict = filterHashtagType(htDict, tweet)
        if taggedTweetDict[0] == 1 or taggedTweetDict[0] == 2:
            dumpDictValuesToFile(taggedTweetDict[1], outputTagged)
        elif taggedTweetDict[0] == 0:
            dumpDictValuesToFile(taggedTweetDict[1], outputTaggedNonRelevant)
        else:
            i += 1


    print "Ambiguous hashtags", i
    outputRelevant.close()
    outputTagged.close()
    outputTaggedNonRelevant.close()
