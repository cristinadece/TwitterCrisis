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

we count the number of tweets and the number of users
'''

romeBB = [tuple([12.341707, 41.769596]), tuple([12.626724, 42.01002])]
stadioOlimpico = [tuple([12.449897, 41.926534]), tuple([12.461527, 41.936048])]
circoMassimo = [tuple([12.481765, 41.883170]), tuple([12.489329, 41.888593])]
piazzaSanPietro = [tuple([12.455789, 41.901337]), tuple([12.458503, 41.903429])]
piazzaSanGiovanni = [tuple([12.505771, 41.885228]), tuple([12.508807, 41.887391])]

def inBB(lon, lat, boundingbox=romeBB):
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


def isBBinBB(tweet_bb, boundingbox=romeBB):
    # [[33.9105011, -4.7672356], [33.9105011, 4.631608], [41.8998666, 4.631608], [41.8998666, -4.7672356]] - kenya
    lonMin = tweet_bb[0][0]
    lonMax = tweet_bb[2][0]
    latMin = tweet_bb[0][1]
    latMax = tweet_bb[2][1]
    return inBB(lonMin, latMin, boundingbox) and inBB(lonMax, latMax, boundingbox)


def isValidLocation(tweet):
    tweet_place_bb = tweet["place"]["bounding_box"]["coordinates"][0]  # list of coordinates [longitude, latitude]
    return isBBinBB(tweet_place_bb)


# def getLocationData(tweet):
#     """
#     These can always have None values; e.g no coordinates, no city, no user location
#     :param tweet:
#     :return:
#     """
#     if tweet["coordinates"] is not None:
#         tweet_coords = tweet['coordinates']['coordinates']  # returns a list [longitude, latitude]
#     else:
#         tweet_coords = None
#
#     if tweet["place"] is not None:
#         if tweet["place"]["place_type"] == "city":
#             tweet_place_city = tweet["place"]["name"]  # if place type == city
#             tweet_place_country = tweet["place"]["country"]
#             tweet_place_country_code = tweet["place"]["country_code"]
#             tweet_place_bb = tweet["place"]["bounding_box"]["coordinates"]
#         else:
#             tweet_place_city = None
#             tweet_place_country = tweet["place"]["country"]
#             tweet_place_country_code = tweet["place"]["country_code"]
#             tweet_place_bb = tweet["place"]["bounding_box"]["coordinates"]
#     else:
#         tweet_place_city = None
#         tweet_place_country = None
#         tweet_place_country_code = None
#
#     #user_location = tweet['user']['location']
#
#     return tweet_coords, tweet_place_city, tweet_place_country, tweet_place_country_code

def dumpDictValuesToFile(tweet, file):
    line = json.dumps(tweet) + "\n"
    file.write(line)

if __name__ == '__main__':
    logger = logging.getLogger("filterRelevantTweets_Rome.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 3:
        print "You need to pass the following 2 params: <jsonTweetsFile> <filteredTweetsFile> "
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputRelevant = codecs.open(sys.argv[2], "w", "utf-8")

    stadioOlimpicoDict = defaultdict(list)
    circoMassimoDict = defaultdict(list)
    piazzaSanGiovanniDict = defaultdict(list)
    piazzaSanPietroDict = defaultdict(list)


    # print htDict
    tweetsAsDict = Tweet.getTweetAsDictionaryNoGZ(inputFile)
    currentFilename = ""

    i = 0
    for tweet, fname in tweetsAsDict:
        if fname not in currentFilename:
            print currentFilename
            if currentFilename is not "":
                print "Stadio Olimpico"
                print "Num tweets: ", len(stadioOlimpicoDict["tweets"])
                print "Num users - uniq", len(set(stadioOlimpicoDict["users"]))
                print "----------------"
                print "Circo Massimo"
                print "Num tweets: ", len(circoMassimoDict["tweets"])
                print "Num users - uniq", len(set(circoMassimoDict["users"]))
                print "----------------"
                print "Piazza San Giovanni"
                print "Num tweets: ", len(piazzaSanGiovanniDict["tweets"])
                print "Num users - uniq", len(set(piazzaSanGiovanniDict["users"]))
                print "----------------"
                print "Piazza San Pietro"
                print "Num tweets: ", len(piazzaSanPietroDict["tweets"])
                print "Num users - uniq", len(set(piazzaSanPietroDict["users"]))
                print "----------------"
                print
            currentFilename = fname
            stadioOlimpicoDict.clear()
            circoMassimoDict.clear()
            piazzaSanGiovanniDict.clear()
            piazzaSanPietroDict.clear()

        if tweet["coordinates"] is not None:
            tweet_coords = tweet['coordinates']['coordinates']  # returns a list [longitude, latitude]
            if (inBB(tweet_coords[0],tweet_coords[1])):
                dumpDictValuesToFile(tweet, outputRelevant)
                i += 1
            if (inBB(tweet_coords[0],tweet_coords[1],stadioOlimpico)):
                stadioOlimpicoDict["tweets"].append(tweet["id_str"])
                stadioOlimpicoDict["users"].append(tweet["user"]["id_str"])
            if (inBB(tweet_coords[0],tweet_coords[1],circoMassimo)):
                print tweet["text"]
                circoMassimoDict["tweets"].append(tweet["id_str"])
                circoMassimoDict["users"].append(tweet["user"]["id_str"])
            if (inBB(tweet_coords[0],tweet_coords[1],piazzaSanGiovanni)):
                piazzaSanGiovanniDict["tweets"].append(tweet["id_str"])
                piazzaSanGiovanniDict["users"].append(tweet["user"]["id_str"])
            if (inBB(tweet_coords[0],tweet_coords[1],piazzaSanPietro)):
                piazzaSanPietroDict["tweets"].append(tweet["id_str"])
                piazzaSanPietroDict["users"].append(tweet["user"]["id_str"])

        else:
            tweet_coords = None

    print "All tweets in Rome in July", i
            
    outputRelevant.close()

    # print inputFile
    # print "Stadio Olimpico"
    # print "Num tweets: ", len(stadioOlimpicoDict["tweets"])
    # print "Num users - uniq", len(set(stadioOlimpicoDict["users"]))
    # print "----------------"
    # print "Circo Massimo"
    # print "Num tweets: ", len(circoMassimoDict["tweets"])
    # print "Num users - uniq", len(set(circoMassimoDict["users"]))
    # print "----------------"
    # print "Piazza San Giovanni"
    # print "Num tweets: ", len(piazzaSanGiovanniDict["tweets"])
    # print "Num users - uniq", len(set(piazzaSanGiovanniDict["users"]))
    # print "----------------"
    # print "Piazza San Pietro"
    # print "Num tweets: ", len(piazzaSanPietroDict["tweets"])
    # print "Num users - uniq", len(set(piazzaSanPietroDict["users"]))
    # print "----------------"
    # print