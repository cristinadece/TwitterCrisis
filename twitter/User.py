__author__ = 'cris'

import gzip
import json
import os

class User:

    id = "";
    type = "";
    screen_name = ""
    location = ""
    tweet_locations = ""

    def __init__(self, id):
        self.id = id

