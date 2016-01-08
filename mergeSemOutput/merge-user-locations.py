import codecs
import json
import logging
import os
import sys
import jsonpickle

__author__ = 'muntean'

'''
This is needed for merging the user info
'''

def buildUserLocationDict(path):
    userHashDict = dict()
    if os.path.isdir(path):
        for fname in os.listdir(path):
            inputFile = codecs.open(os.path.join(path, fname), 'r', 'utf8')
            for line in inputFile:
                data = json.loads(line)
                userID = data[0]
                userInfo = data[1]  #this should be a dictionary
                if userID in userHashDict:
                    # new info
                    tweetCoords = userInfo["tweet_coordinates"]
                    tweerLocations = userInfo["tweet_locations"]

                    # preexisting info
                    userData = userHashDict[userID]

                    #adding new info to preexsiting info
                    userData["tweet_locations"].append(tweerLocations)
                    userData["tweet_coordinates"].append(tweetCoords)
                else:
                    userHashDict[userID].update(userInfo)
    else:
        print "This is not a directory!"

    return userHashDict

def buildUserLocationDictWithPickle(path):
    userHashDict = dict()
    if os.path.isdir(path):
        for fname in os.listdir(path):
            inputFile = codecs.open(os.path.join(path, fname), 'r', 'utf8')
            for line in inputFile:
                data = jsonpickle.decode(line)
                userID = data[0]
                userInfo = data[1]  #this is an object
                if userID in userHashDict:
                    # new info
                    tweetCoords = userInfo.tweet_coordinates
                    tweerLocations = userInfo.tweet_locations

                    # preexisting info
                    userData = userHashDict[userID]

                    #adding new info to preexsiting info
                    userData.setTweetRelatedUserAttributes(tweerLocations, tweetCoords)
                else:
                    userHashDict[userID].update(userInfo)
    else:
        print "This is not a directory!"

    return userHashDict

def writeOutputPlain(userDict, outputFile):
    output = codecs.open(outputFile, "w", "utf-8")
    for k,v in userDict.iteritems():
        #output.write(json.dumps(item) + "\n")
        output.write(k + "\t" + v.toJson() + "\n")
    output.close()

if __name__ == '__main__':
    logger = logging.getLogger("merge-user-locations.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    logger.info('Started counting')

    if len(sys.argv) != 3:
        print "You need to pass the following 3 params: <inputDIR> <outputFileForUserLocation>"
        sys.exit(-1)
    inputDir = sys.argv[1]
    outputFile = sys.argv[2]

    # build user dict with hashtag set
    userLocationDict = buildUserLocationDictWithPickle(inputDir)

    # print to file
    writeOutputPlain(userLocationDict, outputFile)

    logger.info('Finished counting and writing to file')
