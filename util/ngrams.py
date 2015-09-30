__author__ = 'cris'

from itertools import islice

'''
    Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
'''

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield u' '.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        yield u' '.join(result)