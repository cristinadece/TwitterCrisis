import codecs
from collections import defaultdict
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import ngrams
from twitter.Tweet import Tweet

__author__ = 'cris'

neutral_refugee= ['#refugeescrisis', '#syrianrefugees', '#refugees' ]
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad', "#teenchoiceawards"]

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
            screen_name_dict["ANTI"].add((str(userID),str(userScreenName)))
        elif any(r in tweetText for r in pro_refugee):
            pro_refugee_users.add(userID)
            screen_name_dict["PRO"].add((str(userID),str(userScreenName)))
        elif any(r in tweetText for r in neutral_refugee):
            neutral_refugee_users.add(userID)
            screen_name_dict["NEUTRAL"].add((str(userID),str(userScreenName)))

    return [pro_refugee_users, anti_refugee_users, neutral_refugee_users, screen_name_dict]

def coocuringTagsPerUsers(tweetsAsDictionary, pro_refugee_users, anti_refugee_users, neutral_refugee_users):
    i=0
    usersWithPROHashtags = defaultdict(list)
    usersWithANTIHashtags = defaultdict(list)
    usersWithNEUTRALHashtags = defaultdict(list)

    for tweet in tweetsAsDictionary:
        i+=1
        if i%10000==0:
            print 'processing tweets: ', i
        tweetText = Tweet.tokenizeTweetText(tweet['text'])
        if tweet['user']['id_str'] in anti_refugee_users:
            hashtagList = [t for t in tweetText if ngrams.is_hashtag(t)]
            usersWithANTIHashtags[tweet['user']['id_str']].extend(hashtagList)
        elif tweet['user']['id_str'] in pro_refugee_users:
            hashtagList = [t for t in tweetText if ngrams.is_hashtag(t)]
            usersWithPROHashtags[tweet['user']['id_str']].extend(hashtagList)
        elif tweet['user']['id_str'] in neutral_refugee_users:
            hashtagList = [t for t in tweetText if ngrams.is_hashtag(t)]
            usersWithNEUTRALHashtags[tweet['user']['id_str']].extend(hashtagList)

    return [usersWithPROHashtags, usersWithANTIHashtags, usersWithNEUTRALHashtags]

def writeOutput(dictUserHashtagList, outputFile):
    output = codecs.open(outputFile, "w", "utf-8")
    for k,v in dictUserHashtagList.iteritems():
        output.write(u'{}\t{}\n'.format(k,v)) #.encode('utf-8'))
    output.close()

if __name__ == '__main__':


    if len(sys.argv)!=6:
        print "You need to pass the following 2 params: <tweetDirectory> <userFile> <outputFileForUsersWithHashtagsPRO> <outputFileForUsersWithHashtagsANTI> <outputFileForUsersWithHashtagsNEUTRAL>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    userFile = sys.argv[2]
    outputPRO = sys.argv[3]
    outputANTI = sys.argv[4]
    outputNEUTRAL = sys.argv[5]

    logger = logging.getLogger("computerWordCount.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started tagging users')

    tweetsAsDictionary = Tweet.getTweetAsDictionary(tweetDir)
    userSets = tagUsers(tweetsAsDictionary)
    pos = userSets[0]
    neg = userSets[1]
    neu = userSets[2]
    screen_names = userSets[3]

    writeOutput(screen_names, userFile)

    logger.info('Started computing coocurring hashtags per users')

    tweetsAsDict = Tweet().getTweetAsDictionary(tweetDir)
    [usersWithPROHashtags, usersWithANTIHashtags, usersWithNEUTRALHashtags] = coocuringTagsPerUsers(tweetsAsDict, pos, neg, neu)

    writeOutput(usersWithPROHashtags, outputPRO)
    writeOutput(usersWithANTIHashtags, outputANTI)
    writeOutput(usersWithNEUTRALHashtags, outputNEUTRAL)


    logger.info("Finished writing to file")

