__author__ = 'cris'

import gzip
import json
import os

class User:

    id = "";
    type = "";
    screen_name = ""
    location = ""
    tweet_locations = []
    tweet_coordinates = []

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(self.id, self.type, self.screen_name, self.location, self.tweet_locations, self.tweet_coordinates).encode('utf-8')


    def setUserAttributes(self,type, location, screenname, place, coordinates):
        self.type = type
        self.screen_name = screenname
        if location is not None:
            self.location = location
        if place is not None:
            self.tweet_locations.append(place)
        if coordinates is not None:
            self.tweet_coordinates.append(coordinates)
        return self


    def setTweetRelatedUserAttributes(self, place, coord):
        if place is not None:
            self.tweet_locations.append(place)
        if coord is not None:
            self.tweet_coordinates.append(coord)
        return self
