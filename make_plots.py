#!/usr/bin/env python
'''
geo-events-foursquare : make_plots
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 4/18/16
-----------------------------

'''
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

    # tweetIndex = createTweetIndex("/Users/muntean/refugees-output/refugees-with-final-new.json")
    # dailyTweetsMask = createDailyTweetsMask(tweetIndex)
    # userCountryTweetsMask = createUserCountryTweetsMask(tweetIndex)
    # print "Finished indexing tweets and creating masks"
    #
    # plotTweetsPerCountry(userCountryTweetsMask)
    # plotTweetsPerDay(dailyTweetsMask)
    # plotSentimentPerCountry(userCountryTweetsMask, userCountryTweetsMask)
    # plotSentimentPerDay(dailyTweetsMask, userCountryTweetsMask)

    ### plot country sentiment per day
    countryIndex = stats_enriched_tweets.buildCountrySentiIndexMention("/Users/muntean/refugees-output/Final2/refugees_all.json")
    print "finished building index", len(countryIndex)
    # for country in countryIndex.keys():
    #     plotCountrySentimentPerDay(countryIndex[country])

    plotCountrySentimentPerDay(countryIndex["france"], "france")
    plotCountrySentimentPerDay(countryIndex["syria"], "syria")




if __name__ == '__main__':
    main()