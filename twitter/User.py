__author__ = 'cris'

import gzip
import json
import os

class User:

    def __init__(self, id):
        self.id = id
        self.type = "";
        self.screen_name = ""
        self.location = ""
        self.tweet_locations = []
        self.tweet_coordinates = []

    def __str__(self): # this is tricky
        return u"{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(self.id, self.type, self.screen_name, self.location, self.tweet_locations, self.tweet_coordinates).encode('utf-8')

    def toString(self):
        return u"{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(self.id, self.type, self.screen_name, self.location, self.tweet_locations, self.tweet_coordinates)

    def setUserAttributes(self, type, location, screenname):
        self.type = type
        self.screen_name = screenname
        if location is not None:
            self.location = location



    def setTweetRelatedUserAttributes(self, place, coord):
        if place is not None:
            self.tweet_locations.append(place)
        if coord is not None:
            self.tweet_coordinates.append(coord)

