#!/usr/bin/env python
'''
geo-events-foursquare : stats_enriched_tweets
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 4/13/16
-----------------------------


'''
import codecs
import json
from collections import defaultdict


def tweetIter(inputfile):
    """
    Iterates a JSON file containing enriches tweets
    :param inputfile: the file to iterate over
    :return:
    """
    for line in codecs.open(inputfile, "r", "utf-8"):
        try:
            tweet = json.loads(line)
        except:
            print "Couldn't parse tweet: ", line[:200]
        yield tweet


def hasUserLocationAndMentionLocation(tweet):
    """
    Checks if a tweet has both a location and mentions a locations in the text
    :param tweet: tweet as dict
    :return: True/False if it has both
    """
    return (tweet["final_location"] or tweet["final_location_c"]) and (tweet["text_location_mentions"] or tweet["text_location_mentions_c"])


def hasUserLocationAndUserSentiment(tweet):
    # is the sentiment of the tweet or the sentiment of a user?
    """
    Check if user location has a sentiment
    :param tweet:
    :return:
    """
    return ("sentiment_user" in tweet) and (tweet["final_location"] or tweet["final_location_c"])


def hasUserCountryAndUserSentiment(tweet):
    # is the sentiment of the tweet or the sentiment of a user?
    """
    Check if user location has a sentiment
    :param tweet:
    :return:
    """
    return ("sentiment_user" in tweet) and (tweet["final_location_c"])


def hasUserCityAndUserSentiment(tweet):
    # is the sentiment of the tweet or the sentiment of a user?
    """
    Check if user location has a sentiment
    :param tweet:
    :return:
    """
    return ("sentiment_user" in tweet) and (tweet["final_location"])


def hasMentionLocationAndTweetSentiment(tweet):
    return ("sentiment_tweet" in tweet) and (tweet["text_location_mentions"] or tweet["text_location_mentions_c"])


def hasMentionCountryAndTweetSentiment(tweet):
    return ("sentiment_tweet" in tweet) and (tweet["text_location_mentions_c"])


def hasMentionCityAndTweetSentiment(tweet):
    return ("sentiment_tweet" in tweet) and (tweet["text_location_mentions"])


def hasTweetSentimentAndUserSentiment(tweet):
    """

    :param tweet:
    :return:
    """
    return ("sentiment_user" in tweet) and ("sentiment_tweet" in tweet)


def countSimple(filename):
    '''
    We count the number of occurrences for each element

    sentiment_tweet: STRING 'pro_ref' : pro refugees, 'against_ref' : against refugees
                        (the tweet contains polarized hashtags)
    sentiment_user: BOOLEAN  1 : pro refugees, 0 : against refugees
                        (the user is polarized by analyzing the tweets he/she wrote so far)

    We return a dictionary of locations and frequencies per type : mention or user loc,  mention or user loc - country
    '''

    tweetsAsDict = tweetIter(filename)

    # user sentiment count
    countUserPro = 0
    countUserAgainst = 0

    # tweet sentiment count
    countTweetPro = 0
    countTweetAgainst = 0

    # user location - from final
    userLocDict = defaultdict(int)
    userLocCountryDict = defaultdict(int)
    countFinalLoc = 0
    countFinalLocCountry = 0

    # location mention
    locationMention = defaultdict(int)
    locationCountryMention = defaultdict(int)
    countLocMention = 0
    countLocMention_c = 0

    # both location and location mention
    countUserLocAndLocMention = 0

    countMentionLocationAndTweetSentiment = 0
    countUserLocationAndUserSentiment = 0

    i = 0
    for tweet in tweetsAsDict:
        i += 1

        if "sentiment_user" in tweet:
            if tweet["sentiment_user"] == 1:
                countUserPro += 1
            else:
                countUserAgainst += 1

        if "sentiment_tweet" in tweet:
            if tweet["sentiment_tweet"] == 'pro_ref':
                countTweetPro += 1
            else:
                countTweetAgainst += 1

        if tweet["final_location"]:
            countFinalLoc += 1
            userLocDict[tweet["final_location"]] += 1

        if tweet["final_location_c"]:
            countFinalLocCountry += 1
            userLocCountryDict[tweet["final_location_c"]] += 1

        if tweet["text_location_mentions"]:
            if len(tweet["text_location_mentions"]) > 1:
                for loc in tweet["text_location_mentions"]:
                    countLocMention += 1
                    locationMention[loc] += 1
            else:
                countLocMention += 1
                locationMention[tweet["text_location_mentions"][0]] += 1

        if tweet["text_location_mentions_c"]:
            if len(tweet["text_location_mentions_c"]) > 1:
                for loc_c in tweet["text_location_mentions_c"]:
                    countLocMention_c += 1
                    locationCountryMention[loc_c] += 1
            else:
                countLocMention_c += 1
                locationCountryMention[tweet["text_location_mentions_c"][0]] += 1

        if hasUserLocationAndMentionLocation(tweet):
            countUserLocAndLocMention += 1

        if hasUserLocationAndUserSentiment(tweet):
            countUserLocationAndUserSentiment += 1

        if hasMentionLocationAndTweetSentiment(tweet):
            countMentionLocationAndTweetSentiment += 1

    # if i%10000 ==0 :
    #         break

    print "Tweets with User pro: ", countUserPro, "Tweets with User against: ", countUserAgainst
    print "Tweets pro: ", countTweetPro, "Tweets against: ", countTweetAgainst
    print "Final loc: ", countFinalLoc, "Final loc country: ", countFinalLocCountry
    print "Loc mention: ", countLocMention, "Loc mention country: ", countLocMention_c
    print "With Loc and loc mention: ", countUserLocAndLocMention
    print "UserLocationAndUserSentiment: ", countUserLocationAndUserSentiment
    print "MentionLocationAndTweetSentiment: ", countMentionLocationAndTweetSentiment

    return [userLocDict, userLocCountryDict, locationMention, locationCountryMention]


def createTweetIndex(filename):
    """
    This is an index for tweets based on id_str, unfortunately
    :param filename:
    :return:
    """
    tweetIndex = dict()
    tweetsAsDict = tweetIter(filename)
    i = 0
    for tweet in tweetsAsDict:
        i += 1
        tweetIndex[long(tweet["id_str"])] = tweet
        if i % 100000 == 0:
            print i
            # break
    return tweetIndex


def createDailyTweetsMask(tweetIndex):
    """
    This is and index day - [list of tweet_ids], which in conjunction with the tweet index help fast retrieval of tweets
    :param tweetIndex:
    :return:
    """
    dailyTweetsDict = defaultdict(list)
    for tweet in tweetIndex.itervalues():
        dailyTweetsDict[tweet["day"]].append(long(tweet["id_str"]))
    return dailyTweetsDict


def createUserCountryTweetsMask(tweetIndex):
    """
    This is and index day - [list of tweet_ids], which in conjunction with the tweet index help fast retrieval of tweets
    :param tweetIndex:
    :return:
    """
    dailyTweetsDict = defaultdict(list)
    for tweet in tweetIndex.itervalues():
        dailyTweetsDict[tweet["final_location_c"]].append(long(tweet["id_str"]))
    return dailyTweetsDict


def createDayIndex(filename):
    """
    This is an individual structure which indexes days with dictionary representation on tweets!
    :param filename:
    :return:
    """
    dayIndex = dict()
    tweetsAsDict = tweetIter(filename)
    i = 0
    for tweet in tweetsAsDict:
        i += 1
        dayIndex[tweet["day"]] = tweet
        # if i % 30000 == 0:
        #     break
    return dayIndex


def buildCountrySentiIndexMention(filename):
    """
    The structure is a dictionary < location : dictionary <date, [list of sentiments - repeating e.g. 0,1,1,0,1 ...]> >
    :param filename:
    :param location_field_name:
    :return:
    """
    countryIndex = defaultdict(lambda : defaultdict(list))
    tweetsAsDict = tweetIter(filename)
    i = 0
    for tweet in tweetsAsDict:
        i += 1
        if tweet["text_location_mentions_c"] and "sentiment_tweet" in tweet:
            countries = tweet["text_location_mentions_c"]
            day = tweet["day"]
            sentiment = tweet["sentiment_tweet"]
            if sentiment == "pro_ref":
                senti = 1
            else:
                senti = 0
            for country in countries:
                countryIndex[country][day].append(senti)

    return countryIndex


def buildCountrySentiIndexUser(filename):
    """
    The structure is a dictionary < location : dictionary <date, [list of sentiments - repeating e.g. 0,1,1,0,1 ...]> >
    :param filename:
    :param location_field_name:
    :return:
    """
    countryIndex = defaultdict(lambda : defaultdict(list))
    tweetsAsDict = tweetIter(filename)
    i = 0
    for tweet in tweetsAsDict:
        i += 1
        if tweet["final_location_c"] and "sentiment_user" in tweet:
            country = tweet["final_location_c"]  # this is a string not a list
            day = tweet["day"]
            sentiment = tweet["sentiment_user"]

            countryIndex[country][day].append(sentiment)  # this is already 0 o 1

        # if i % 30000 == 0:
        #     # print i
        #     break
    return countryIndex



def buildMixCountryMentionUserSenti(filename):
    """
    The structure is a dictionary < location : dictionary <date, [list of sentiments - repeating e.g. 0,1,1,0,1 ...]> >
    :param filename:
    :param location_field_name:
    :return:
    """
    countryIndex = defaultdict(lambda: defaultdict(set))
    user_class = defaultdict()
    tweetsAsDict = tweetIter(filename)
    i = 0
    for tweet in tweetsAsDict:
        i += 1
        if tweet["text_location_mentions_c"] and "sentiment_user" in tweet:
            countries = tweet["text_location_mentions_c"]  # this is a string not a list
            day = tweet["day"]
            sentiment = tweet["sentiment_user"]
            user_id = tweet["user_id"]
            user_class[user_id] = sentiment  # pos, neg users
            for country in countries:
                countryIndex[country][day].add(user_id)  # this is the user_id

        # if i % 30000 == 0:
        #     # print i
        #     break
    print "finished step 1"

    new_countryIndex = defaultdict(lambda: defaultdict(list))
    for country, dayDict in countryIndex.iteritems():
        for day, uniq_users in dayDict.iteritems():
            unique_user_senti_list = list()
            for user in uniq_users:
                unique_user_senti_list.append(user_class[user])
            new_countryIndex[country][day].extend(unique_user_senti_list)

    print "finished step 2"

    return new_countryIndex



def main():

    # countSimple("/Users/muntean/refugees-output/Final2/refugees_all.json")
    # loc_mentions = buildCountrySentiIndexMention("/Users/muntean/refugees-output/refugees-with-final-new.json")
    # user_loc = buildCountrySentiIndexUser("/Users/muntean/refugees-output/refugees-with-final-new.json")
    mix = buildMixCountryMentionUserSenti("/Users/muntean/refugees-output/Final2/refugees_all.json")
    print mix["serbia"]

if __name__ == '__main__':
    main()