__author__ = 'cris'

from itertools import islice

'''
    Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
'''


def contains_hashtag(iterable):
    for elem in iterable:
        if elem.startswith('#'):
            return True
    return False

def contains_mention(iterable):
    for elem in iterable:
        if elem.startswith('@'):
            return True
    return False

def contains_url(iterable):
    for elem in iterable:
        if elem.startswith('http'):
            return True
    return False

def contains_non_words(iterable):
    for elem in iterable:
        if elem.startswith('http') or elem.startswith('#') or elem.startswith("@"):
            return True
    return False

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield u' '.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        yield u' '.join(result)

def window_no_twitter_elems(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if (len(result) == n) and ( not contains_non_words(result)):
        yield u' '.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        if not contains_non_words(result):
            yield u' '.join(result)

def window_no_hashtags(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if (len(result) == n) and ( not contains_hashtag(result)):
        yield u' '.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        if not contains_hashtag(result):
            yield u' '.join(result)