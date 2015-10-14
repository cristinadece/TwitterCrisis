from collections import defaultdict
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet
from twitter.User import User


__author__ = 'cris'

neutral_refugee= ['#refugeescrisis', '#syrianrefugees', '#refugees' ]
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad', "#teenchoiceawards"]


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

        if tweet['coordinates'] is not None:
            tweetCoords = ((tweet['coordinates']['coordinates'][0], tweet['coordinates']['coordinates'][1]))

        i+=1
        if i%10000==0:
            print 'processing tweets: ', i
        if any(r in tweetText for r in anti_refugee):
            if userID in user_dict:
                User.setTweetRelatedUserAttributes(user_dict.get(userID), tweetPlace, tweetCoords)
            else:
                user = User(userID)
                user = User.setUserAttributes(user, "ANTI", userLocation, userScreenName, tweetPlace, tweetCoords)
                user_dict[userID] = user
        elif any(r in tweetText for r in pro_refugee):
            if userID in user_dict:
                User.setTweetRelatedUserAttributes(user_dict.get(userID), tweetPlace, tweetCoords)
            else:
                user = User(userID)
                user = User.setUserAttributes(user, "ANTI", userLocation, userScreenName, tweetPlace, tweetCoords)
                user_dict[userID] = user
        elif any(r in tweetText for r in neutral_refugee):
            if userID in user_dict:
                User.setTweetRelatedUserAttributes(user_dict.get(userID), tweetPlace, tweetCoords)
            else:
                user = User(userID)
                user = User.setUserAttributes(user, "ANTI", userLocation, userScreenName, tweetPlace, tweetCoords)
                user_dict[userID] = user

        # if i%5==0:
        #     break

    return user_dict



if __name__ == '__main__':


    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <tweetDirectory>  <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]

    tweets = Tweet(tweetDir).getTweetAsDictionary()
    user_dict = getUsersWithLocation(tweets)

    outputFILE = open(output, "w")
    for u in user_dict.values():
        outputFILE.write(str(u) + '\n')
    outputFILE.close()

