import codecs
import json
import logging
import os
import sys
from collections import defaultdict, Counter
# from geopy.geocoders import Nominatim
# https://github.com/geopy/geopy


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import locations
from util import ngrams
from tokenizer import twokenize


"""
Need to see: how many have:
    - geotagging
    - coordinates
    - user location


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


# def countLocationsInTweetText(locationList, locationDict, country=False):
#     """
#
#     :param locationList:
#     :param locationDict:
#     :param country:
#     :return:
#     """
#     # output = codecs.open(outputFile, "w", "utf-8")
#     orderredLocations = Counter(locationList).most_common()
#     for loc in orderredLocations:
#         lat = locationDict[loc[0]][3]
#         lon = locationDict[loc[0]][2]
#         try:
#             s = loc[0] + "," + str(lon) + "," + str(lat) + "," + str(loc[1]) + "\n"
#         except:
#             print "error happens here: ", inputFile, loc, locationDict[loc]
#     #     output.write(s)
#     # output.close()

def getLocationsFromToken(token, cityDict, countryDict):
    city = ""
    country = ""
    if cityDict[token]:
        city = token
    if countryDict[token]:
        country = token
    return city, country


def getUserLocation(tweet, cityDict, countryDict, outputFile):
    """
    THis field is an empty string
    :param tweet:
    :return:
    """

    potentialCities = list()
    potentialCountries = list()

    outputFile.write("=========================\n")

    locationField = tweet["user_location"].lower()
    outputFile.write(locationField + "\n")

    # 1. check if user loc is word or country - unigrams - to lower
    city, country = getLocationsFromToken(locationField, cityDict, countryDict)
    if city or country:
        outputFile.write("1 " + city + "|" + country + "\n")
        potentialCities.append(city)
        potentialCountries.append(countries)
        return potentialCities, potentialCountries
    # 2. split by ,
    elif "," in locationField:
        locArray = locationField.split(",")
        for token in locArray:
            city, country = getLocationsFromToken(token, cityDict, countryDict)
            if city or country:
                outputFile.write("2 " + city + "|" + country + "\n")
                potentialCities.append(city)
                potentialCountries.append(countries)
        return potentialCities, potentialCountries
    # 3. split by /
    elif "/" in locationField:
        locArray = locationField.split(",")
        for token in locArray:
            city, country = getLocationsFromToken(token, cityDict, countryDict)
            if city or country:
                outputFile.write("3 " + city + "|" + country + "\n")
                potentialCities.append(city)
                potentialCountries.append(countries)
        return potentialCities, potentialCountries

    # 4. split by " "
    # if " " in locationField:
    #     locArray = locationField.split(",")
    #     for token in locArray:
    #         city, country = getLocationsFromToken(token, cityDict, countryDict)
    #         outputFile.write("4 " + city + "|" + country + "\n")

    # 5. tokenize with util and get bigram and trigrams - to lower
    # bi
    else:
        tokenList = twokenize.tokenize(locationField.lower())
        tokens = ngrams.window_no_twitter_elems(tokenList,2)
        for token in tokens:
            city, country = getLocationsFromToken(token, cityDict, countryDict)
            if city or country:
                outputFile.write("5a " + city + "|" + country + "\n")
                potentialCities.append(city)
                potentialCountries.append(countries)

        tokens = ngrams.window_no_twitter_elems(tokenList,3)
        for token in tokens:
            city, country = getLocationsFromToken(token, cityDict, countryDict)
        if city or country:
            outputFile.write("5b " + city + "|" + country + "\n")
            potentialCities.append(city)
            potentialCountries.append(countries)
        return potentialCities, potentialCountries

    c = set(potentialCities)
    if "" in c:
        c.remove("")
    C = set(potentialCountries)
    if "" in C:
        C.remove("")
    return c, C


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
    # countries = defaultdict(tuple)
    # euroCountries = defaultdict(tuple)

    cities = locations.Cities.loadFromFile()
    euroCities = locations.Cities.filterEuropeanCities(cities)
    print euroCities["washington"]
    print cities["raqqa"]
    print euroCountries["turkey"], countries["turkey"]  # only in countries!

    citiesAscii = locations.Cities.loadFromFile(ascii=True)
    euroCitiesAscii = locations.Cities.filterEuropeanCities(citiesAscii)


    tweetId = 0
    placeTweets = list()
    geotaggedTweets = list()
    userLocationTweets = list()

    outputFile = codecs.open("userLocationParsing.txt", "w", encoding="utf-8")

    filterredTweets = getFilterredTweetsAsDict(inputFile)
    for tweet in filterredTweets:
        tweetId += 1
        if getPlace(tweet) is not None:
            placeTweets.append(tweetId)
        if getCoords(tweet) is not None:
            geotaggedTweets.append(tweetId)
        if tweet["user_location"]:
            userLocationTweets.append(tweetId)
            potentialCities, potentialCountries = getUserLocation(tweet, euroCities, euroCountries, outputFile)


        # if tweetId % 100 == 0:
        #     break
    outputFile.close()

    print "Tweets with place", len(placeTweets) #, placeTweets
    print "Tweets with GEO", len(geotaggedTweets) #, geotaggedTweets
    print "Tweets with user location", len(userLocationTweets) #, userLocationTweets

    # intersections - it could happen then same tweet has place, geo and user location
    # for tweets with place or geo - the user location become last resource
    print "Tweets with place and geo", len(set(placeTweets).intersection(set(geotaggedTweets)))
    print "Tweets with place and user loc", len(set(placeTweets).intersection(set(userLocationTweets)))
    print "Tweets with geo and user loc", len(set(geotaggedTweets).intersection(set(userLocationTweets)))


