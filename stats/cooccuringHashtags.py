from collections import defaultdict
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import ngrams
from util.TweetTextTokenizer import TweetTextTokenizer

__author__ = 'cris'

neutral_refugee= ['#refugeescrisis', '#syrianrefugees', '#refugees' ]
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad'] #, "#teenchoiceawards"]

def tagUsers(tweetsAsDictionary):
    pro_refugee_users = set()
    anti_refugee_users = set()
    neutral_refugee_users = set()
    screen_name_dict = defaultdict(set)

    i = 0
    for tweet in tweetsAsDictionary:
        tweetText = tweet['text'].lower() #todo remember to lowercase everything
        userID = tweet['user']['id_str']
        userScreenName = tweet['user']['screen_name']
        i+=1
        if i%10000==0:
            print 'processing tweets: ', i
        if any(r in tweetText for r in anti_refugee):
            anti_refugee_users.add(userID)
            screen_name_dict["ANTI"].add((userID,userScreenName))
        elif any(r in tweetText for r in pro_refugee):
            pro_refugee_users.add(userID)
            screen_name_dict["PRO"].add((userID,userScreenName))
        elif any(r in tweetText for r in neutral_refugee):
            neutral_refugee_users.add(userID)
            screen_name_dict["NEUTRAL"].add((userID,userScreenName))

    return [pro_refugee_users, anti_refugee_users, neutral_refugee_users, screen_name_dict]

def coocuringTagsPerUsers(tweetsAsDictionary, pro_refugee_users, anti_refugee_users):
    i=0
    usersWithPROHashtags = defaultdict(list)
    usersWithANTIHashtags = defaultdict(list)

    for tweet in tweetsAsDictionary:
        i+=1
        if i%10000==0:
            print 'processing tweets: ', i
        tweetText = TweetTextTokenizer.tokenizeTweetText(tweet['text'])
        if tweet['user']['id_str'] in anti_refugee_users:
            hashtagList = [t for t in tweetText if ngrams.is_hashtag(t)]
            usersWithANTIHashtags[tweet['user']['id_str']].extend(hashtagList)
        elif tweet['user']['id_str'] in pro_refugee_users:
            hashtagList = [t for t in tweetText if ngrams.is_hashtag(t)]
            usersWithPROHashtags[tweet['user']['id_str']].extend(hashtagList)
    return [usersWithPROHashtags, usersWithANTIHashtags]

def writeOutput(dictUserHashtagList, outputFile):
    output = open(outputFile, 'w')
    for k,v in dictUserHashtagList.iteritems():
        output.write(u'{}\t{}\n'.format(k,v).encode('utf-8'))
    output.close()

if __name__ == '__main__':


    if len(sys.argv)!=5:
        print "You need to pass the following 2 params: <tweetDirectory>  <userFile> <outputFileForUsersWithHashtagsPRO> <outputFileForUsersWithHashtagsANTI>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    userFile = sys.argv[2]
    outputPRO = sys.argv[3]
    outputANTI = sys.argv[4]

    logger = logging.getLogger("computerWordCount.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started tagging users')

    tweetsAsDictionary = TweetTextTokenizer(tweetDir).getTweetAsDictionary()
    userSets = tagUsers(tweetsAsDictionary)
    pos = userSets[0]
    neg = userSets[1]
    screen_names = userSets[3]
    print screen_names

    writeOutput(screen_names, userFile)

    logger.info('Started computing coocurring hashtags per users')

    tweetsAsDict = TweetTextTokenizer(tweetDir).getTweetAsDictionary()
    [usersWithPROHashtags, usersWithANTIHashtags] = coocuringTagsPerUsers(tweetsAsDict, pos, neg)

    writeOutput(usersWithPROHashtags, outputPRO)
    writeOutput(usersWithANTIHashtags, outputANTI)

