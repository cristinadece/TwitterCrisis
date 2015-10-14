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
        return u"{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(self.id, self.type, self.screen_name, self.location, self.tweet_locations, self.tweet_coordinates).encode('utf-8')

    @staticmethod
    def setUserAttributes(user, type, location, screenname, place, coordinates):
        user.type = type
        user.screen_name = screenname
        if location is not None:
            user.location = location
        if place is not None:
            user.tweet_locations.append(place)
        if coordinates is not None:
            user.tweet_coordinates.append(coordinates)
        return user

    @staticmethod
    def setTweetRelatedUserAttributes(user, place, coord):
        if place is not None:
            user.tweet_locations.append(place)
        if coord is not None:
            user.tweet_coordinates.append(coord)
        return user
