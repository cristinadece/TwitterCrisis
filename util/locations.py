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

class Cities:

    @staticmethod
    def loadFromFile(filename="../resources/cities15000inBB.txt", ascii=False):
        """
        This method load a dictionary of cities where the key is either the name or the asciiname
        :param filename:
        :param ascii: Trues if we want the dictionary to have the asciinames as key, False otherwise
        :return:
        """
        worldLocations = defaultdict()
        for line in codecs.open(filename, "r", "utf-8"):
            locationData = line.split("\t")
            name = locationData[1].lower()
            asciiname = locationData[2]
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            countrycode = locationData[8]
            timezone = locationData[17]
            if name not in stopwords:
                if ascii:
                    worldLocations[asciiname.lower()] = tuple([name, asciiname, longitude, latitude, countrycode, timezone])
                else:
                    worldLocations[name.lower()] = tuple([name, asciiname, longitude, latitude, countrycode, timezone])
        return worldLocations


    @staticmethod
    def filterEuropeanCities(worldLocations):
        citiesEurope = defaultdict()
        for city, cityTuple in worldLocations.iteritems():
            if "Europe" in cityTuple[5]:
                citiesEurope[city] = cityTuple
        print len(citiesEurope)
        return citiesEurope


    @staticmethod
    def filterCitiesInBB(filename="../resources/cities15000.txt"):
        new_file = filename.replace(".txt", "") + "inBB.txt"
        output = codecs.open(new_file, "w", "utf-8")
        for line in codecs.open(filename, "r", "utf-8"):
            locationData = line.split("\t")
            latitude = float(locationData[4])
            longitude = float(locationData[5])
            if inBB(longitude, latitude, eurasiaBB):
                output.write(line)
        output.close()


class Countries:

    @staticmethod
    def loadFromFile(filename="../resources/countryInfo.txt"):
        """
        #ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode
        CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode
        :param filename:
        :return:
        """
        countriesDict = defaultdict()
        print filename
        for line in codecs.open(filename, "r", "utf-8"):
            if not line.startswith("#") and line != "\n":
                countryData = line.split("\t")
                name = countryData[4].lower()
                capital = countryData[5]
                population = countryData[7]
                continent = countryData[8]
                if (name not in stopwords) and (continent == "EU"):
                    print name, continent
                    countriesDict[name.lower()] = tuple([name, capital, population, continent])
        print len(countriesDict)
        return countriesDict

    @staticmethod
    def filterCountriesInBB(filename="../resources/cities15000.txt"):
        """
        We can do this based on the capital coordinates to simplify stuff.
        For each country we have the capital and we search that capital in the Cities Dict, take the coords and if they
        are in the BB it means the country is in BB.
        :param filename:
        :return:
        """
        pass


if __name__ == '__main__':
    logger = logging.getLogger("locations.py")
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s;%(levelname)s;%(message)s")

    Cities.filterCitiesInBB()

    cities = Cities.loadFromFile()  #todo how should i index the cities, maybe also ascii
    citiesEU = Cities.filterEuropeanCities(cities)
    print citiesEU.keys()[:100]

    countries = Countries.loadFromFile()

