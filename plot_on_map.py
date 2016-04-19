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
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import enrich_relevant_tweet
import stats_enriched_tweets
from util import locations



def dumpData(filename, data):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for item in data:
            writer.writerow(item)


def getCapitalCoords(country):
    pass


def getCoords(city, city_dict):
    cityEntry = city_dict[city]
    try:
        u = cityEntry[2]
    except:
        print cityEntry, city
    return [cityEntry[2], cityEntry[3]]


def plot_cities_on_maps_cvs(inputFile, outputUser, outputMention, euroCities, cities):
    i = 0
    tweetIterator = enrich_relevant_tweet.tweetIter(inputFile)
    with open(outputUser, 'wb') as user_f, open(outputMention, 'wb') as tweet_f:
        i += 1
        user_writer = csv.writer(user_f)
        tweet_writer = csv.writer(tweet_f)
        for tweet in tweetIterator:
            day = tweet["day"]
            # print day

            if stats_enriched_tweets.hasUserCityAndUserSentiment(tweet):
                # write user loc + user senti
                user_sentiment = tweet["sentiment_user"]
                user_loc = tweet["final_location"]
                if user_loc in euroCities.keys():
                    [lon, lat] = getCoords(user_loc, euroCities)
                    user_writer.writerow([day, user_sentiment, user_loc.encode("utf-8"), lat, lon])
                else:
                    print user_loc

            if stats_enriched_tweets.hasMentionLocationAndTweetSentiment(tweet):
                # write tweet location mention + tweet senti
                tweet_sentiment = tweet["sentiment_tweet"]
                location_mentions = tweet["text_location_mentions"]
                for loc in location_mentions:
                    [lon, lat] = getCoords(loc, cities)
                    tweet_writer.writerow([day, tweet_sentiment, loc.encode("utf-8"), lat, lon])


def plot_countries_on_maps_cvs(inputFile, outputUser, outputMention, euroCountries, countries, ccDict):
    i = 0
    tweetIterator = enrich_relevant_tweet.tweetIter(inputFile)
    with open(outputUser, 'wb') as user_f, open(outputMention, 'wb') as tweet_f:
        i += 1
        user_writer = csv.writer(user_f)
        tweet_writer = csv.writer(tweet_f)
        for tweet in tweetIterator:
            day = tweet["day"]
            # print day

            if stats_enriched_tweets.hasUserCountryAndUserSentiment(tweet):
                # write user loc + user senti
                user_sentiment = tweet["sentiment_user"]
                user_loc = tweet["final_location_c"]
                if user_loc in ccDict.keys():
                    # [lon, lat] = getCoords(user_loc, euroCities)
                    user_writer.writerow([day, user_sentiment, ccDict[user_loc].encode("utf-8")]) #, lat, lon])
                else:
                    print user_loc

            if stats_enriched_tweets.hasMentionCountryAndTweetSentiment(tweet):
                # write tweet location mention + tweet senti
                tweet_sentiment = tweet["sentiment_tweet"]
                if tweet_sentiment == "pro_ref":
                    senti = 1
                else:
                    senti = 0
                location_mentions = tweet["text_location_mentions_c"]
                for loc in location_mentions:
                    # [lon, lat] = getCoords(loc, cities)
                    tweet_writer.writerow([day, senti, loc.encode("utf-8")]) #, lat, lon])



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
    ccDict = locations.Countries.countryCodeDict(countries)


    ### dump csv for plots in carto db
    #plot_cities_on_maps_cvs(inputFile, outputUser, outputMention, euroCities, cities)

    plot_countries_on_maps_cvs(inputFile, outputUser, outputMention, euroCountries, countries, ccDict)

if __name__ == '__main__':
    main()