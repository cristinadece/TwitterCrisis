import codecs
import json
import logging
import os
import sys
from collections import Counter

from geopy.geocoders import Nominatim
# https://github.com/geopy/geopy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util import worldLocations

"""
{"user_id": "26900055", "screen_name": "DrMartyFox", "text": "RT @petefrt: Scientists Blast Obamas Global Warming Claims
http://t.co/Z7VS2tNaNn  #tcot #teaparty #pjnet #gop #tlot #ccot #p2 http://t.co/\u2026", "created_at": "Tue Aug 04 23:59:28 +0000 2015",
"hashtags": [{"indices": [83, 88], "text": "tcot"}, {"indices": [89, 98], "text": "teaparty"}, {"indices": [99, 105], "text": "pjnet"},
{"indices": [106, 110], "text": "gop"}, {"indices": [111, 116], "text": "tlot"}, {"indices": [117, 122], "text": "ccot"},
{"indices": [123, 126], "text": "p2"}], "place": null, "id_str": "628716917310771201",
"tokenized_text": ["@petefrt", "scientists", "blast", "obamas", "global", "warming", "claims", "http://t.co/z7vs2tnann",
"#tcot", "#teaparty", "#pjnet", "#gop", "#tlot", "#ccot", "#p2", "http://t.co/\u2026"]}
"""

def searchWithGeopy(query):
    geolocator = Nominatim()
    location = geolocator.geocode(query)
    print location.raw

    # we need title

    # we need coords
    print((location.latitude, location.longitude))


def getFilterredTweetsAsDict(path):
    if os.path.isdir(path):
         for fname in os.listdir(path):
            for line in codecs.open(os.path.join(path, fname), "r", "utf-8"):
                try:
                    tweet = json.loads(line)
                except:
                    print "Couldn't parse tweet: ", line[:200]
                yield tweet
    else:
        print "Opening file: ", path
        for line in codecs.open(path, "r", "utf-8"):
            try:
                tweet = json.loads(line)
            except:
                print "Couldn't parse tweet: ", line[:200]
            yield tweet


if __name__ == '__main__':
    logger = logging.getLogger("worldLocations.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 3:
        print "You need to pass the following param: <inputFile> <output>"
        sys.exit(-1)
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    # searchWithGeopy("Paris")

    wl = worldLocations.Locations.loadFromFile()
    print "Loaded city dict", len(wl)

    i = 0
    locationList = list()
    filterredTweets = getFilterredTweetsAsDict(inputFile)
    for tweet in filterredTweets:
        i += 1
        # print tweet["tokenized_text"]
        # todo check is hashtag is a place by removing hash
        for token in tweet["tokenized_text"]:
            if token in wl.keys():
                locationList.append(token.lower())

        if i % 1000 == 0:
            print i
        if i % 4000 == 0:
            break

    #
    output = codecs.open(outputFile, "w", "utf-8")
    orderredLocations = Counter(locationList).most_common()
    print orderredLocations
    # for loc in orderredLocations:
    #     lat = wl[loc[0]][3]
    #     lon = wl[loc[0]][2]
    #     s = str(loc[0]) + str(lon) + str(lat) + str(loc[1])


    # [(u'obama', 73), (u'clinton', 55), (u'police', 46), (u'vienna', 34), (u'man', 17), (u'budapest', 15),
    # (u'reading', 13), (u'harper', 13), (u'munich', 12), (u'liberal', 11), (u'dallas', 10), (u'goes', 8),
    # (u'dortmund', 8), (u'gay', 8), (u'moscow', 8), (u'liberty', 7), (u'university', 6), (u'born', 6),
    # (u'sale', 6), (u'london', 5), (u'young', 5), (u'teresa', 4), (u'sydney', 4), (u'march', 4), (u'stockholm', 4),
    # (u'david', 4), (u'carson', 4), (u'aleppo', 4), (u'franklin', 3), (u'paradise', 3), (u'davis', 3), (u'calais', 3),
    # (u'pearl', 3), (u'toronto', 3), (u'imperial', 3), (u'mexico', 3), (u'jefferson', 3), (u'hammond', 3), (u'hassan', 3),
    # (u'ron', 2), (u'mosul', 2), (u'damascus', 2), (u'virginia', 2), (u'lala', 2), (u'nice', 2), (u'madrid', 2),
    # (u'fatwa', 2), (u'mecca', 2), (u'savage', 2), (u'central', 2), (u'melbourne', 2), (u'zug', 2), (u'colorado', 2),
    # (u'bell', 2), (u'washington', 2), (u'spring', 2), (u'mary', 2), (u'benghazi', 2), (u'gaza', 2), (u'gallup', 2),
    # (u'delta', 2), (u'vladimir', 2), (u'male', 2), (u'vancouver', 2), (u'walker', 2), (u'date', 2), (u'latakia', 2),
    # (u'dinar', 2), (u'green', 2), (u'fresno', 1), (u'lansing', 1), (u'liberia', 1), (u'bar', 1), (u'asia', 1),
    # (u'martin', 1), (u'marion', 1), (u'belgrade', 1), (u'lebanon', 1), (u'birmingham', 1), (u'brits', 1),
    # (u'portland', 1), (u'chicago', 1), (u'federal', 1), (u'newark', 1), (u'surprise', 1), (u'venezuela', 1), (u'anna', 1),
    # (u'wa', 1), (u'nashville', 1), (u'dome', 1), (u'saalfeld', 1), (u'york', 1), (u'malm\xf6', 1), (u'hobart', 1),
    # (u'metro', 1), (u'langley', 1), (u'barry', 1), (u'kendall', 1), (u'hyderabad', 1), (u'evans', 1), (u'manage', 1),
    # (u'pop', 1), (u'hebron', 1), (u'gary', 1), (u'oakland', 1), (u'george', 1), (u'ontario', 1), (u'union', 1),
    # (u'gap', 1), (u'tehran', 1), (u'walnut', 1), (u'tampa', 1), (u'tokyo', 1), (u'levin', 1), (u'crystal', 1), (u'plymouth', 1),
    # (u'patos', 1), (u'galt', 1), (u'boston', 1), (u'smyrna', 1), (u'barcelona', 1), (u'geneva', 1), (u'boom', 1),
    # (u'puri', 1), (u'canterbury', 1), (u'elizabeth', 1), (u'victoria', 1), (u'opportunity', 1), (u'humble', 1),
    # (u'kyle', 1), (u'rome', 1), (u'salt', 1), (u'ho', 1)]

