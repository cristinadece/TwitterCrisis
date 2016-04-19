#!/usr/bin/env python
'''
geo-events-foursquare : enrich_relevant_tweet
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 4/6/16
-----------------------------


'''
import codecs
import json
import logging
import sys
import operator
from util import locations
from processing import locationsInTweets


def tweetIter(inputfile):
    """
    Read simplified relevant tweet
    """
    for line in codecs.open(inputfile, "r", "utf-8"):
        try:
            tweet = json.loads(line)
        except:
            print "Couldn't parse tweet: ", line[:200]
        yield tweet


def addUserExLocation(tweet, euroCities, euroCountries):
    """
    user_ex_location: LIST - location of the user (extracted from user manual input field)
    user_ex_location_c: STRING -  country code (if more than one leave it empty)
    :param tweet:
    :param euroCities:
    :param euroCountries:
    :return:
    """
    potentialCities, potentialCountries, us = locationsInTweets.getUserLocation(tweet["user_location"], euroCities, euroCountries)
    country_codes = set()

    # init or covers other cases
    tweet["user_ex_location"] = []
    tweet["user_ex_location_c"] = None

    if not us:
        tweet["user_ex_location"] = list(potentialCities)

        if len(potentialCountries) == 0:
            # infer form cities
            for city in potentialCities:
                country_codes.add(euroCities[city][4]) ## add country code, could be more than 1

        if len(potentialCountries) == 1:
            potentialCountry = next(iter(potentialCountries))
            country_codes.add(euroCountries[potentialCountry][4])

        if len(potentialCountries) > 1 or len(country_codes) > 1:
            tweet["user_ex_location_c"] = None
            tweet["user_ex_location"] = []
        elif len(country_codes) == 1:
            tweet["user_ex_location_c"] = next(iter(country_codes))

    return tweet


def addFinalLocation(tweet, euroCities):
    """

    :param tweet:
    :param euroCities:
    :return:
    """
    flag = None

    # 1. check for city; if we find country simply return
    if "gps_ex_location" in tweet:
        tweet["final_location"] = tweet["gps_ex_location"]
        if "gps_ex_location_c" in tweet:
            tweet["final_location_c"] = tweet["gps_ex_location_c"]
            return tweet
        flag = "gps_city"
    elif "place_ex_location" in tweet:
        tweet["final_location"] = tweet["place_ex_location"]
        if "place_ex_location_c" in tweet:
            tweet["final_location_c"] = tweet["place_ex_location_c"]
            return tweet
        flag = "place_city"
    elif tweet["user_ex_location"]:
        if len(tweet["user_ex_location"]) > 1:
            # same country different cities
            locOrderedByPop = dict()
            for loc in tweet["user_ex_location"]:
                population = euroCities[loc][5]
                locOrderedByPop[loc] = population
            sorted_x = sorted(locOrderedByPop.items(), key=operator.itemgetter(1))
            # print "Ambiguous location", tweet["user_ex_location"], sorted_x[0][0]
            tweet["final_location"] = sorted_x[0][0]
        else:
            tweet["final_location"] = tweet["user_ex_location"][0]
        if tweet["user_ex_location_c"]:
            tweet["final_location_c"] = tweet["user_ex_location_c"]
            return tweet
        flag = "user_city"

    if flag is not None:
        print "We have city but no country", tweet
    else:
        # 2. check for country (no city, flag should be None)
        if tweet["user_ex_location_c"]:
            tweet["final_location_c"] = tweet["user_ex_location_c"]
            flag = "user_country"
        elif "gps_ex_location_c" in tweet:
            tweet["final_location_c"] = tweet["gps_ex_location_c"]
            flag = "gps_country"
        elif "place_ex_location_c" in tweet:
            tweet["final_location_c"] = tweet["place_ex_location_c"]
            flag = "place_country"

    if flag in ["user_country", "gps_country", "place_country"]:
        tweet["final_location"] = None

    if flag is None:
        tweet["final_location"] = None
        tweet["final_location_c"] = None

    return tweet


def addFinalLocationAdapted(tweet, euroCities):
    """

    :param tweet:
    :param euroCities:
    :return:
    """

    # country
    if "gps_ex_location_c" in tweet:
        tweet["final_location_c"] = tweet["gps_ex_location_c"]
    elif "place_ex_location_c" in tweet:
        tweet["final_location_c"] = tweet["place_ex_location_c"]
    elif tweet["user_ex_location_c"]:
        tweet["final_location_c"] = tweet["user_ex_location_c"]
    else:
        tweet["final_location_c"] = None  # these should be actually removed

    # city
    if "gps_ex_location" in tweet:
        tweet["final_location"] = tweet["gps_ex_location"]
    elif "place_ex_location" in tweet:
        tweet["final_location"] = tweet["place_ex_location"]
    elif tweet["user_ex_location"]:
        if len(tweet["user_ex_location"]) > 1:
            # same country different cities
            locOrderedByPop = dict()
            for loc in tweet["user_ex_location"]:
                population = euroCities[loc][5]
                locOrderedByPop[loc] = population
            sorted_x = sorted(locOrderedByPop.items(), key=operator.itemgetter(1))
            #print "Ambiguous location", tweet["user_ex_location"], sorted_x[0][0]
            tweet["final_location"] = sorted_x[0][0]
        else:
            tweet["final_location"] = tweet["user_ex_location"][0]
    else:
        tweet["final_location"] = None  # these should be actually removed

    return tweet


def addTweetTextLocations(tweet, cityDict, countryDict, ccDict):
    """
    Enriching schema with tweet text locations:
    - text_location_mentions: LIST - all cities mentioned in the text of the tweet
    - text_location_mentions_c: LIST - all countries mentioned in the text of the tweets AND all countries to which
    the mentioned cities belong to

    :param tweet:
    :param cityDict:
    :param countryDict:
    :return:
    """
    # countrycode 2 country map

    citiesInTweetText, countriesInTweetText = locationsInTweets.getLocationFromTweetText(tweet, cityDict, countryDict)
    for city in citiesInTweetText:
        countryCode = cityDict[city][4]
        # print cityDict[city]
        countryName = ccDict[countryCode]
        countriesInTweetText.add(countryName)

    tweet["text_location_mentions"] = list(citiesInTweetText)
    tweet["text_location_mentions_c"] = list(countriesInTweetText)  # todo add also country code?
    return tweet


def main():
    logger = logging.getLogger("enrichRelevantTweets.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 3:
        print "You need to pass the following 2 params: <relevantTweets> <enrichedTweets>"
        sys.exit(-1)
    inputRelevant = sys.argv[1]
    outputEnriched = codecs.open(sys.argv[2], "w", "utf-8")


    # load cities and countries
    countries = locations.Countries.loadFromFile()
    euroCountries = locations.Countries.filterEuropeanCountries(countries)
    cities = locations.Cities.loadFromFile()
    euroCities = locations.Cities.filterEuropeanCities(cities)
    # citiesAscii = locations.Cities.loadFromFile(ascii=True)
    # euroCitiesAscii = locations.Cities.filterEuropeanCities(citiesAscii)
    ccDict = locations.Countries.countryCodeDict(countries)

    # start iterating tweets
    tweetsAsDict = tweetIter(inputRelevant)
    i = 0
    for tweet in tweetsAsDict:
        i += 1
        enrichedTweet1 = addUserExLocation(tweet, euroCities, euroCountries)
        # print repr(enrichedTweet["user_location"])
        # print enrichedTweet["user_ex_location"], enrichedTweet["user_ex_location_c"]

        # enrichedTweet2 = addFinalLocationAdapted(enrichedTweet1, euroCities)
        enrichedTweet2 = addFinalLocation(enrichedTweet1, euroCities)
        # print enrichedTweet["final_location"], enrichedTweet["final_location_c"]

        enrichedTweet = addTweetTextLocations(enrichedTweet2, cities, countries, ccDict)
        # print repr(enrichedTweet["text"])
        # print enrichedTweet["text_location_mentions"], enrichedTweet["text_location_mentions_c"]
        # print

        # if "paris. " in tweet["user_location"]:
        #     enrichedTweet = addUserExLocation(tweet, euroCities, euroCountries)
        #     print repr(enrichedTweet["user_location"])
        #     print enrichedTweet["user_ex_location"], enrichedTweet["user_ex_location_c"]

        outputEnriched.write(json.dumps(enrichedTweet) + "\n")
        # print enrichedTweet
        # if i % 40 == 0:
        #     break


    outputEnriched.close()

if __name__ == '__main__':
    main()