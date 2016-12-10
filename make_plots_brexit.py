#!/usr/bin/env python
'''
geo-events-foursquare : make_plots
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 4/18/16
-----------------------------

'''
import datetime

import stats_enriched_tweets
from plots import plot_templates
from stats_enriched_tweets import createTweetIndex, createDailyTweetsMask, createUserCountryTweetsMask

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
    plot_templates.plotBarWithLables(values, labels, "Number of tweets per country")


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

    plot_templates.plotBarWithLables2Distrib(against, pro, labels, "User Sentiment per Country")


def plotTweetsPerDay(tweetsPerDayDict):
    tweetsPerDay = [[len(y), x] for x, y in tweetsPerDayDict.items() if x is not None]
    print "Tweets per day", len(tweetsPerDay)
    values = list(zip(*tweetsPerDay)[0])
    labels = list(zip(*tweetsPerDay)[1])
    # distributions.plotBarMinimal(values)
    plot_templates.plotBarWithLables(values, labels, "Number of tweets per day", rotation=70)


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

    plot_templates.plotBarWithLables2Distrib(against, pro, labels, "User Sentiment per Day", rot=70)


def plotCountrySentimentPerDay(dailySentiDict, countryName):
    labels = list()
    against = list()
    pro = list()

    dailySentiDictSorted = sorted(dailySentiDict.iteritems(), key=lambda x: x[0])  # order by date
    for record in dailySentiDictSorted:
        day = record[0]
        sentiList = record[1]
        labels.append(day)
        count_pro = sentiList.count(1)
        pro.append(count_pro)
        count_anti = sentiList.count(0)
        against.append(count_anti)

    plot_templates.plotBarWithLables2Distrib(against, pro, labels, countryName.capitalize() + " sentiment per Day", rot=70)



def main():
    print datetime.datetime.now()

    filename_pre = "/Users/cris/all-brexit-with-sent_pre-lines.json"
    filename_post = "/Users/cris/all-brexit-with-sent_post-lines.json"

    # 1. tweet index
    pre_tweetIndex = stats_enriched_tweets.createTweetIndex(filename_pre)
    print len(pre_tweetIndex)
    print datetime.datetime.now()

    post_tweetIndex = stats_enriched_tweets.createTweetIndex(filename_post)
    print len(post_tweetIndex)
    print datetime.datetime.now()

    # 2. masks over tweet index pre
    print "PRE brexit"
    pre_dailyTweetsDict = stats_enriched_tweets.createDailyTweetsMask(pre_tweetIndex)
    print "Daily tweets - volumes:", len(pre_dailyTweetsDict)
    pre_userCountryTweetsDict = stats_enriched_tweets.createUserCountryTweetsMask(pre_tweetIndex)
    print "User country tweets - volumes - EU:", len(pre_userCountryTweetsDict)
    print datetime.datetime.now()

    # 2. masks over tweet index post
    print "POST brexit"
    post_dailyTweetsDict = stats_enriched_tweets.createDailyTweetsMask(post_tweetIndex)
    print "Daily tweets - volumes:", len(post_dailyTweetsDict)
    post_userCountryTweetsDict = stats_enriched_tweets.createUserCountryTweetsMask(post_tweetIndex)
    print "User country tweets - volumes - EU:", len(post_userCountryTweetsDict)

    print datetime.datetime.now()


    # plotTweetsPerCountry(userCountryTweetsMask)
    # plotTweetsPerDay(dailyTweetsMask)
    # plotSentimentPerCountry(userCountryTweetsMask, userCountryTweetsMask)
    # plotSentimentPerDay(dailyTweetsMask, userCountryTweetsMask)






if __name__ == '__main__':
    main()