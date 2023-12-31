import codecs
import re
from collections import defaultdict
import json
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import ngrams
from twitter.Tweet import Tweet


__author__ = 'cris'

'''
This script computes cooccuring hashtags (from relevant users) with few preselected
Run it:
<python cooccurringHashtagsByUsers.py ../../../../english-tweets ../../../../users-by-type.json
../../../../cooc-hashtags-Pro.json ../../../../cooc-hashtags-Anti.json ../../../../cooc-hashtags-Neutral.json>

Parallel version:
./runParallelCooccurringHashtags.sh

'''

neutral_refugee = ['#refugeescrisis', '#syrianrefugees', '#refugees']
pro_refugee = ['#refugeeswelcome', '#refugeesnotmigrants', '#refugeesnotpawns', '#saverefugees', '#welcomerefugees']
anti_refugee = ['#nomorerefugees', '#refugeesnotwelcome', '#norefugees', '#refugeejihad']


def tagUsers(tweetsAsDictionary):
    pro_refugee_users = set()
    anti_refugee_users = set()
    neutral_refugee_users = set()
    screen_name_dict = defaultdict(set)

    i = 0
    for tweet in tweetsAsDictionary:
        tweetText = tweet['text'].lower()  # todo remember to lowercase everything
        userID = tweet['user']['id_str']
        userScreenName = tweet['user']['screen_name']

        i += 1
        if i % 10000 == 0:
            print 'processing tweets: ', i

        if any(r in tweetText for r in anti_refugee):
            anti_refugee_users.add(userID)
            screen_name_dict["ANTI"].add((str(userID), str(userScreenName)))
        if any(r in tweetText for r in pro_refugee):
            pro_refugee_users.add(userID)
            screen_name_dict["PRO"].add((str(userID), str(userScreenName)))
        if any(r in tweetText for r in neutral_refugee):
            neutral_refugee_users.add(userID)
            screen_name_dict["NEUTRAL"].add((str(userID), str(userScreenName)))

    return [pro_refugee_users, anti_refugee_users, neutral_refugee_users, screen_name_dict]


def resolveAmbiguousUsers(pro_refugee_users, anti_refugee_users, neutral_refugee_users, tweetDir):
    Anti_Pro_users = anti_refugee_users & pro_refugee_users
    Pro_Neutral_users = pro_refugee_users & neutral_refugee_users
    Anti_Neutral_users = anti_refugee_users & neutral_refugee_users
    all_intersection = anti_refugee_users & pro_refugee_users & neutral_refugee_users

    sure_Anti = anti_refugee_users - pro_refugee_users - neutral_refugee_users
    sure_Pro = pro_refugee_users - anti_refugee_users - neutral_refugee_users
    sure_Neutral = neutral_refugee_users - anti_refugee_users - pro_refugee_users

    date = re.findall('(\d+)', tweetDir)[0]

    output = open("some-processing-" + date + ".tsv", "w")
    output.write( "Anti Total: " + str(len(anti_refugee_users)) + "\n")
    output.write( "Pro Total: " + str(len(pro_refugee_users)) + "\n")
    output.write( "Neutral Total: " + str(len(neutral_refugee_users)) + "\n")
    output.write( "Anti_Pro_users: " + str(len(Anti_Pro_users)) + "\n")
    output.write( "Anti_Neutral_Users: " + str(len(Anti_Neutral_users)) + "\n")
    output.write( "Pro_Neutral_users: " + str(len(Pro_Neutral_users)) + "\n")
    output.write( "Anti_Pro_Neutral_users: " + str(len(all_intersection)) + "\n")
    output.write( "ONLY_Anti_users: " + str(len(sure_Anti)) + "\n")
    output.write( "ONLY_Pro_users: " + str(len(sure_Pro)) + "\n")
    output.write( "ONLY_Neutral_users: " + str(len(sure_Neutral)) + "\n")
    output.close()


    #  return [sure_Anti, sure_Pro, sure_Neutral] this mixed up the files inverting anti and pro between each other
    return [sure_Pro, sure_Anti, sure_Neutral]


def coocuringTagsPerUsers(tweetsAsDictionary, pro_refugee_users, anti_refugee_users, neutral_refugee_users):
    i = 0
    usersWithPROHashtags = defaultdict(list)
    usersWithANTIHashtags = defaultdict(list)
    usersWithNEUTRALHashtags = defaultdict(list)

    for tweet in tweetsAsDictionary:
        i += 1
        # if i%100000==0:
        #     break
        if i % 10000 == 0:
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
    for k, v in dictUserHashtagList.iteritems():
        output.write('{}\t{}\n'.format(k, v))
    output.close()


def writeOutputPlainAndJSON(dictUserHashtagList, outputFile):
    output = codecs.open(outputFile, "w", "utf-8")
    for k, v in dictUserHashtagList.iteritems():
        hashtagsAsString = ",".join(list(set(v)))
        output.write(
            k + '\t' + json.dumps(hashtagsAsString).replace('"', ''))  # todo: this is too strange, but it works
        output.write('\n')
    output.close()


if __name__ == '__main__':

    if len(sys.argv) != 6:
        print "Need to pass the following params: <tweetDirectory> <userFile> <outputFileForUsersWithHashtagsPRO> " \
              "<outputFileForUsersWithHashtagsANTI> <outputFileForUsersWithHashtagsNEUTRAL>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    userFile = sys.argv[2]
    outputPRO = sys.argv[3]
    outputANTI = sys.argv[4]
    outputNEUTRAL = sys.argv[5]

    logger = logging.getLogger("cooccurringHashtagsByUsers.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    # Step 1 : TAG USERS
    logger.info('Started tagging users')

    tweetsAsDictionary = Tweet.getTweetAsDictionary(tweetDir)
    userSets = tagUsers(tweetsAsDictionary)
    pro = userSets[0]
    neg = userSets[1]
    neu = userSets[2]
    screen_names = userSets[3]

    writeOutput(screen_names, userFile)

    # Step 2 : Resolve ambiguous users
    logger.info('Resolving ambiguous users')
    [usersPRO, usersANTI, usersNEUTRAL] = resolveAmbiguousUsers(pro, neg, neu, tweetDir)

    # Step 3 : Cooc hashtags
    logger.info('Started computing coocurring hashtags per users')

    tweetsAsDict = Tweet.getTweetAsDictionary(tweetDir)
    [usersWithPROHashtags, usersWithANTIHashtags, usersWithNEUTRALHashtags] = coocuringTagsPerUsers(tweetsAsDict, usersPRO, usersANTI, usersNEUTRAL)

    writeOutputPlainAndJSON(usersWithPROHashtags, outputPRO)
    writeOutputPlainAndJSON(usersWithANTIHashtags, outputANTI)
    writeOutputPlainAndJSON(usersWithNEUTRALHashtags, outputNEUTRAL)

    logger.info("Finished writing to file")
