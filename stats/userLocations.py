import codecs
from collections import defaultdict
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet
from twitter.User import User


__author__ = 'cris'

neutral_refugee= ['#refugeescrisis', '#syrianrefugees', '#refugees']
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad', "#teenchoiceawards"]

def addUserToCorrespondingDict(userID, userType, userScreenName, userLocation, tweetPlace, tweetCoords, user_dict):
    if userID in user_dict:
        old_user = user_dict.get(userID)
        old_user.setTweetRelatedUserAttributes(tweetPlace, tweetCoords)
    else:
        user = User(userID)
        user.setUserAttributes(userType, userLocation, userScreenName)
        user.setTweetRelatedUserAttributes(tweetPlace, tweetCoords)
        user_dict[userID] = user
    return user_dict


def getUsersWithLocation(tweetsAsDictionary):
    user_dict = defaultdict(User)

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
        print userID, tweetPlace

        if tweet['coordinates'] is not None:
            tweetCoords = ((tweet['coordinates']['coordinates'][0], tweet['coordinates']['coordinates'][1]))

        i+=1
        if i%10000==0:
            print 'processing tweets: ', i

        if any(r in tweetText for r in anti_refugee):
            addUserToCorrespondingDict(userID, "ANTI", userLocation, userScreenName, tweetPlace, tweetCoords, user_dict)
        elif any(r in tweetText for r in pro_refugee):
            addUserToCorrespondingDict(userID, "PRO", userLocation, userScreenName, tweetPlace, tweetCoords, user_dict)
        elif any(r in tweetText for r in neutral_refugee):
            addUserToCorrespondingDict(userID, "NEUTRAL", userLocation, userScreenName, tweetPlace, tweetCoords, user_dict)

        # if i%5==0:
        #     break

    return user_dict

if __name__ == '__main__':


    if len(sys.argv)!=3:
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

