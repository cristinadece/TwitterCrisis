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
from plots import plot_distributions

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


def hasMentionLocationAndTweetSentiment(tweet):
    return ("sentiment_tweet" in tweet) and (tweet["text_location_mentions"] or tweet["text_location_mentions_c"])


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


def plotTweetsPerCountry(tweetsPerCountryDict):
    """

    :param tweetsPerCountry: is a dictionary of key=country and values=list of tweets ids
    :return:
    """
    tweetsPerCountry = [[len(y), x] for x, y in tweetsPerCountryDict.items() if x is not None]
    print "user countries: ", len(tweetsPerCountry)
    values = list(zip(*tweetsPerCountry)[0])
    labels = list(zip(*tweetsPerCountry)[1])
    # distributions.plotBarMinimal(values)
    plot_distributions.plotBarWithLables(values, labels, "Number of tweets per country")


def plotSentimentPerCountry(tweetsPerCountry, tweetIndex):
    """

    :param tweetsPerCountry: is a dictionary of key=country and values=list of tweets ids
    :return:
    """
    againstCount = 0
    proCount = 0
    countrySentimDict = dict()
    for country, tweetList in tweetsPerCountry.iteritems():
        for tweet_id in tweetList:
            tweet = tweetIndex[tweet_id]
            if "sentiment_user" in tweet:
                if tweet["sentiment_user"] == 0:
                    againstCount += 1
                else:
                    proCount += 1
        countrySentimDict[country] = [againstCount, proCount]
        againstCount = 0
        proCount = 0
    print "len country sentim dict", len(countrySentimDict)
    sortedCountrySentimDict = sorted(countrySentimDict.items(), key=lambda x: x[1][0] + x[1][1], reverse=True)

    ### if i remove the and in the parethesis the plot is fit exactly , without the space on the right
    data = [[x,y,z] for x, [y,z] in sortedCountrySentimDict if x is not None and (z is not 0 or y is not 0)]
    labels = list(zip(*data)[0])
    against = list(zip(*data)[1])
    pro = list(zip(*data)[2])

    plot_distributions.plotBarWithLables2Distrib(against, pro, labels, "User Sentiment per Country")


def plotTweetsPerDay(tweetsPerDayDict):
    tweetsPerDay = [[len(y), x] for x, y in tweetsPerDayDict.items() if x is not None]
    print "Tweets per day", len(tweetsPerDay)
    values = list(zip(*tweetsPerDay)[0])
    labels = list(zip(*tweetsPerDay)[1])
    # distributions.plotBarMinimal(values)
    plot_distributions.plotBarWithLables(values, labels, "Number of tweets per day", rotation=70)


def plotSentimentPerDay(tweetsPerDay, tweetIndex):
    againstCount = 0
    proCount = 0
    countrySentimDict = dict()
    for day, tweetList in tweetsPerDay.iteritems():
        for tweet_id in tweetList:
            tweet = tweetIndex[tweet_id]
            if "sentiment_user" in tweet:
                if tweet["sentiment_user"] == 0:
                    againstCount += 1
                else:
                    proCount += 1
        countrySentimDict[day] = [againstCount, proCount]
        againstCount = 0
        proCount = 0
    print "Country sentiment dict", len(countrySentimDict)

    countrySentimDictOrdered = sorted(countrySentimDict.iteritems(), key=lambda x:x[0])

    ### if i remove the and in the parethesis the plot is fit exactly , without the space on the right
    data = [[x, y, z] for x, [y, z] in countrySentimDictOrdered if x is not None]  # and (z is not 0 or y is not 0)]
    labels = list(zip(*data)[0])
    against = list(zip(*data)[1])
    pro = list(zip(*data)[2])

    plot_distributions.plotBarWithLables2Distrib(against, pro, labels, "User Sentiment per Day", rot=70)


def main():

    # countSimple("/Users/muntean/refugees-with-final.json")

    ti = createTweetIndex("/Users/muntean/refugees-with-final.json")
    di = createDailyTweetsMask(ti)
    ci = createUserCountryTweetsMask(ti)
    print "Finished indexing tweets and creating masks"

    # plotTweetsPerCountry(ci)
    # plotTweetsPerDay(di)
    plotSentimentPerCountry(ci, ti)
    # plotSentimentPerDay(di, ti)



if __name__ == '__main__':
    main()