#!/usr/bin/env python
'''
geo-events-foursquare : plot_on_map
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 4/15/16
-----------------------------


'''
import csv
import os
import sys
import numpy as np
from mpltools import style
import enrich_relevant_tweet
import stats_enriched_tweets
from util import locations
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def dumpData(filename, data):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for item in data:
            writer.writerow(item)


def getCapitalCoords(country):
    pass


def getCoords(city, city_dict):
    cityEntry = city_dict[city]
    return [cityEntry[2], cityEntry[3]]


def main():
    # take params
    if len(sys.argv) != 4:
        print "You need to pass the following 3 params: <enriched-tweets> <outputUser> <outputMention>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputUser = sys.argv[2]
    outputMention = sys.argv[3]



    # load cities and countries
    countries = locations.Countries.loadFromFile()
    euroCountries = locations.Countries.filterEuropeanCountries(countries)
    cities = locations.Cities.loadFromFile()
    euroCities = locations.Cities.filterEuropeanCities(cities)
    citiesAscii = locations.Cities.loadFromFile(ascii=True)
    euroCitiesAscii = locations.Cities.filterEuropeanCities(citiesAscii)
    ccDict = enrich_relevant_tweet.countryCodeDict(countries)

    #
    i = 0
    tweetIterator = enrich_relevant_tweet.tweetIter("/Users/muntean/refugees-with-final.json")
    with open(outputUser, 'wb') as user_f, open(outputUser, 'wb') as tweet_f:
        i += 1
        user_writer = csv.writer(user_f)
        tweet_writer = csv.writer(tweet_f)
        for tweet in tweetIterator:
            # todo check id tweet has user location and only then plot!

            day = tweet["day"]

            if stats_enriched_tweets.hasUserLocationAndUserSentiment(tweet):
                # write user loc + user senti
                user_loc = tweet["final_location"]
                [lon, lat] = getCoords(user_loc)
                # user_country = tweet["final_location_c"]
                user_sentiment = tweet["sentiment_user"]
                user_writer.write([day, user_sentiment, user_loc, lat, lon])

            if stats_enriched_tweets.hasMentionLocationAndTweetSentiment(tweet):
                # write tweet location mention + tweet senti
                location_mention = tweet["text_location_mentions"]
                [lon, lat] = getCoords(location_mention)
                # country_mention  = tweet["text_location_mentions_c"]
                tweet_sentiment = tweet["sentiment_tweet"]
                tweet_writer.write([day, tweet_sentiment, location_mention, lat, lon])

            if i % 10000 == 0:
                break

if __name__ == '__main__':
    main()