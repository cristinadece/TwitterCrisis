import sys

__author__ = 'cris'

pro_refugee = []
anti_refugee = []

def tagUsers(tweets):
    pro_refugee_users = set()
    anti_refugee_users = set()




if __name__ == '__main__':
    if len(sys.argv)!=3:
        print "You need to pass the following 2 params: <tweetDirectory>  <outputFileForWordCount>"
        sys.exit(-1)
    tweetDir = sys.argv[1]
    output = sys.argv[2]
