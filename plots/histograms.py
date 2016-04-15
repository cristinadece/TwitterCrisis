#!/usr/bin/env python
'''
geo-events-foursquare : histograms
@euthor: Cristina Muntean (cristina.muntean@isti.cnr.it)
@date: 4/14/16
-----------------------------


'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpltools import style
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def setStyle():
    style.use('ggplot')


def loadData(filename):
    data = np.genfromtxt(filename, dtype=str)
    return data



def main():
    pass

if __name__ == '__main__':
    main()