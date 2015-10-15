import codecs
from collections import defaultdict
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet
from twitter.User import User

__author__ = 'cris'

neutral_refugee = ['#refugeescrisis', '#syrianrefugees', '#refugees']
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad', "#teenchoiceawards"]


def addUserToCorrespondingDict(userID, userType, userLocation, userScreenName, tweetPlace, tweetCoords, user_dict2):
    if userID in user_dict2:
        old_user = user_dict2.get(userID)
        old_user.setTweetRelatedUserAttributes(tweetPlace, tweetCoords)
        user_dict2[userID] = old_user
    else:
        user = User(userID)
        user.setUserAttributes(userType, userLocation, userScreenName)
        user.setTweetRelatedUserAttributes(tweetPlace, tweetCoords)
        user_dict2[userID] = user
    return user_dict2


def getUsersWithLocation(tweetsAsDictionary):
    user_dict = dict()

    i = 0
    for tweet in tweetsAsDictionary:
        tweetText = tweet['text'].lower()
        userID = tweet['user']['id_str']
        userScreenName = tweet['user']['screen_name']
        userLocation = tweet['user']['location']
        tweetPlace = None
        tweetCoords = None
        if tweet['place'] is not None:
            tweetPlace = tweet['place']['full_name']
        if tweet['coordinates'] is not None:
            tweetCoords = ((tweet['coordinates']['coordinates'][0], tweet['coordinates']['coordinates'][1]))

        i += 1
        if i % 10000 == 0:
            print 'processing tweets: ', i

        if any(r in tweetText for r in anti_refugee):
            # print "ANTI", userID, tweetPlace
            addUserToCorrespondingDict(userID, "ANTI", userLocation, userScreenName, tweetPlace, tweetCoords, user_dict)
        elif any(r in tweetText for r in pro_refugee):
            # print "PRO", userID, tweetPlace
            addUserToCorrespondingDict(userID, "PRO", userLocation, userScreenName, tweetPlace, tweetCoords, user_dict)
        elif any(r in tweetText for r in neutral_refugee):
            # print "NEUTRAL", userID, tweetPlace
            addUserToCorrespondingDict(userID, "NEUTRAL", userLocation, userScreenName, tweetPlace, tweetCoords, user_dict)

            # if i%5==0:
            #     break

    return user_dict


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "You need to pass the following 2 params: <tweetDirectory>  <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]

    tweets = Tweet.getTweetAsDictionary(tweetDir)
    user_dict = getUsersWithLocation(tweets)

    outputFILE = codecs.open(output, "w", "utf-8")
    for u in user_dict.values():
        outputFILE.write(u.toString())
    outputFILE.close()
