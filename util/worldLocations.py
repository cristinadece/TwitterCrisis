import codecs
import logging
import sys
from collections import defaultdict

stopwords = ["dalai", "buy", "best", "deal", "obama", "clinton", "police", "goes", "reading", "born", "manage", "gay",
             "barry", "dinar", "sale", "march", "nice", "mary", "vladimir", "zug", "boom", "anna", "gap", "york", "bar",
             "salt", "wedding"]

# eg New York

# [[[-24.08203125,14.0939571778],[-24.08203125,66.9988437919],[70.13671875,66.9988437919],[70.13671875,14.0939571778],
# [-24.08203125,14.0939571778]]]

# -24.08203125,14.0939571778,70.13671875,66.9988437919

eurasiaBB = [tuple([-24.08203125,14.0939571778]), tuple([70.13671875,66.9988437919])]

def inBB(lon, lat, boundingbox=eurasiaBB):
    lonMin = boundingbox[0][0]
    lonMax = boundingbox[1][0]
    latMin = boundingbox[0][1]
    latMax = boundingbox[1][1]
    return lonMin < lon < lonMax and latMin < lat < latMax


class Locations:

    @staticmethod
    def loadFromFile(filename="../resources/cities15000inBB.txt"):
        worldLocations = defaultdict()  # todo: this should be a dict of lists as multiple locations with the same name
        for line in codecs.open(filename, "r", "utf-8"):
            locationData = line.split("\t")
            name = locationData[1].lower()
            asciiname = locationData[2]
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            countrycode = locationData[8]
            timezone = locationData[17]
            if name not in stopwords:
                worldLocations[name.lower()] = tuple([name, asciiname, longitude, latitude, countrycode, timezone])
        return worldLocations

    @staticmethod
    def filterLocationsInBB(filename="../resources/cities15000.txt"):
        new_file = filename.replace(".txt", "") + "inBB.txt"
        output = codecs.open(new_file, "w", "utf-8")
        for line in codecs.open(filename, "r", "utf-8"):
            locationData = line.split("\t")
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            if inBB(longitude, latitude, eurasiaBB):
                output.write(line)
        output.close()


if __name__ == '__main__':
    logger = logging.getLogger("worldLocations.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    if len(sys.argv) != 2:
        print "You need to pass the following 2 params: <inputFile> ; cities1000.txt"
        sys.exit(-1)
    inputFile = sys.argv[1]

    Locations.filterLocationsInBB()

    # wl = Locations.loadFromFile()
    # print len(wl)


