import codecs
import json
import logging
import os
import sys
from collections import Counter
# from geopy.geocoders import Nominatim
# https://github.com/geopy/geopy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import locations

"""
{"tweet_place_country": null, "user_id": "62815642", "screen_name": "TrucksHorsesDog", "tweet_place_city": null,
"tweet_place_country_code": null, "text": "RT @LeahR77: #PlannedInfanticide &amp; The Mammogram MYTH
\ud83d\udc4c\n#DefundPP #PPSellsDeadBabies #PJNET #TCOT http://t.co/m90wG0zpwn", "created_at": "Tue Aug 04 23:59:51 +0000 2015",
"hashtags": [{"indices": [13, 32], "text": "PlannedInfanticide"}, {"indices": [60, 69], "text": "DefundPP"}, {"indices": [70, 88],
"text": "PPSellsDeadBabies"}, {"indices": [89, 95], "text": "PJNET"}, {"indices": [96, 101], "text": "TCOT"}],
"user_location": "A R I Z O N A", "place": null, "id_str": "628717013452468224", "tokenized_text": ["@leahr77",
"#plannedinfanticide", "mammogram", "myth", "\ud83d\udc4c", "#defundpp", "#ppsellsdeadbabies", "#pjnet", "#tcot",
"http://t.co/m90wg0zpwn"], "tweet_coords": null}
"""

# Usage: searchWithGeopy("Paris")
# def searchWithGeopy(query):
#     geolocator = Nominatim()
#     location = geolocator.geocode(query)
#     print location.raw
#
#     # we need title
#
#     # we need coords
#     print((location.latitude, location.longitude))


def getFilterredTweetsAsDict(path):
    if os.path.isdir(path):
         for fname in os.listdir(path):
            for line in codecs.open(os.path.join(path, fname), "r", "utf-8"):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]
                yield tweet
    else:
        print "Opening file: ", path
        for line in codecs.open(path, "r", "utf-8"):
            try:
                tweet = json.loads(line)
            except:
                print "Couldn't parse tweet: ", line[:200]
            yield tweet


def getLocationFromTweetText(tweet, cityDict, countryDict):
    cityList = list()
    countryList = list()
    for token in tweet["tokenized_text"]:  # todo: bigrams, trigrams, check if hashtag is a place by removing hash
            if token.lower() in cityDict.keys():  # The dict has keys in lowercase
                cityList.append(token.lower())
            if token.lower() in countryDict.keys():
                countryList.append(token.lower())
    return cityList, countryList  # these need to be added to a bigger list for all tweets


def countLocationsInTweetText(locationList, locationDict):  #todo this nees to be fixed for countries
    # output = codecs.open(outputFile, "w", "utf-8")
    orderredLocations = Counter(locationList).most_common()
    for loc in orderredLocations:
        lat = locationDict[loc[0]][3]
        lon = locationDict[loc[0]][2]
        try:
            s = loc[0] + "," + str(lon) + "," + str(lat) + "," + str(loc[1]) + "\n"
        except:
            print "error happens here: ", inputFile, loc, locationDict[loc]
    #     output.write(s)
    # output.close()


def getUserLocation(tweet):
    """
    THis field is an empty string
    :param tweet:
    :return:
    """
    if tweet["user_location"]:
        print tweet["user_location"]
        # tokenize by , / " " unigrams, bigrams, trigrams to lower!
    else:
        print "the field is empty"

def getPlace(tweet):
    """
    The idea here is that if a tweet has a place it has a country and maybe even a city - in the json schema
    :param tweet:
    :return: null or the object(dict)
    """
    return tweet["place"]


def getCoords(tweet):
    """
    Returns the coords of the tweet. We should check if they are in the europe BB
    :param tweet:
    :return:
    """
    return tweet["tweet_coords"]


if __name__ == '__main__':
    logger = logging.getLogger("locationsInTweets.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 3:
        print "You need to pass the following param: <inputFile> <output>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    # load cities and countries
    countries = locations.Countries.loadFromFile()
    euroCountries = locations.Countries.filterEuropeanCountries(countries)

    cities = locations.Cities.loadFromFile()
    euroCities = locations.Cities.filterEuropeanCities(cities)

    citiesAscii = locations.Cities.loadFromFile(ascii=True)
    euroCitiesAscii = locations.Cities.filterEuropeanCities(citiesAscii)


    i = 0

    filterredTweets = getFilterredTweetsAsDict(inputFile)
    for tweet in filterredTweets:
        i += 1
        print tweet
        getUserLocation(tweet)

        if i % 10 == 0:
            break





