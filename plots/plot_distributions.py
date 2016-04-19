#!/usr/bin/env python
'''
geo-events-foursquare : distributions
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


def plotBarMinimal(distrib):
    setStyle()
    plt.figure()
    ind = np.arange(len(distrib))  # the x locations for the groups
    width = 0.35  # the width of the bars
    plt.bar(ind, distrib, width)
    plt.show()


def plotBarWithLables(distrib, labels, title, rot=0):
    setStyle()
    plt.figure()
    ind = np.arange(len(distrib))
    plt.bar(ind, distrib, align='center')
    plt.xticks(ind, labels, rotation=rot)
    plt.legend(loc='upper left')
    plt.title(title)
    plt.show()


def plotBarWithLables2Distrib(a,b, labels, title, rot=0):

    setStyle()

    ind = np.arange(len(a))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, a, width, color='r')
    rects2 = ax.bar(ind + width, b, width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Frequencies')
    ax.set_title(title)
    ax.set_xticks(ind + width)
    ax.set_xticklabels(labels)

    plt.setp(ax.get_xticklabels(), rotation=70, horizontalalignment='right')

    # ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
    #
    # def autolabel(rects):
    #     # attach some text labels
    #     for rect in rects:
    #         height = rect.get_height()
    #         ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
    #                 '%d' % int(height),
    #                 ha='center', va='bottom')
    #
    # autolabel(rects1)
    # autolabel(rects2)

    plt.show()

    # # plt.show()
    # plt.tight_layout()
    # plt.savefig("/tmp/midsomma2-hour.pdf")


def main():
    pass


if __name__ == '__main__':
    main()