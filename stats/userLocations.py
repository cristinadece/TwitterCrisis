from collections import defaultdict
import sys
import os
from twitter.User import User

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from twitter.Tweet import Tweet


__author__ = 'cris'

neutral_refugee= ['#refugeescrisis', '#syrianrefugees', '#refugees' ]
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad'] #, "#teenchoiceawards"]

def tagUsers(tweetsAsDictionary):

    screen_name_dict = defaultdict(set)

    i = 0
    for tweet in tweetsAsDictionary:
        tweetText = tweet['text'].lower()
        userID = tweet['user']['id_str']
        userScreenName = tweet['user']['screen_name']
        userLocation = tweet['user']['location']
        tweetPlace = tweet['place']
        tweetCoords = tweet['coordinates']

        i+=1
        if i%10000==0:
            print 'processing tweets: ', i
        if any(r in tweetText for r in anti_refugee):
            user = User(userID)
            screen_name_dict["ANTI"].add((userID,userScreenName))
        elif any(r in tweetText for r in pro_refugee):

            screen_name_dict["PRO"].add((userID,userScreenName))
        elif any(r in tweetText for r in neutral_refugee):

            screen_name_dict["NEUTRAL"].add((userID,userScreenName))

    return [screen_name_dict]




def getUserLocation():
    return

if __name__ == '__main__':


    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <tweetDirectory>  <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]

    tweets = Tweet.getTweetAsDictionary(tweetDir)

