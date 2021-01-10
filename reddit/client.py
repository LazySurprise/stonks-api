from collections import Counter
from datetime import datetime
from flask import Flask, current_app
from os.path import dirname, abspath

import praw
import re

# 0: upvotes
#   - only get posts w/ certain num upVotes
# 1: date restrictons
#   - if date is too soon, save in db, call lambda when date is of age

# TODO:
#   - rename class
#   - factor out stonk; make seperate class for stonk
# should rename to something like 'RedditStonk' bc single use pattern
class Reddit:

    def __init__(self, mode = '', client_id = '', client_secret = '', user_agent = ''):
        self.stonk_list  = self.__build_stonk_list()
        self.__reddit = {} if mode == 'test' else self.__build_reddit_client(client_id, client_secret, user_agent)
        self.__stonks = []

    def get_stonks(self):
        posts = self.fetch_stonks()
        stonks = self.parse_stonks(posts)
        return stonks

    def fetch_stonks(self, stonk_query = False):
        # query resolver
        #   - graph vs rest?
        #fetch = self.__build_api_call(stonk_query)
        #top_posts = fetch()
        #top_posts = self.__reddit.subreddit('wallstreetbets').top("all")
        top_posts = self.__reddit.subreddit('wallstreetbets').top("week")

        posts = []
        for post in top_posts:
            time = self.__convert_time(post.created_utc)
            today = datetime.today().strftime('%Y-%m-%d %HH:%MM:%SS')
            if (time == today):
                print('too early. add stonk to db to be checked by lambda')
            else:
                posts.append([post.title, post.selftext, time]) 
        return posts

    # TODO:
    #  - refactor to use filter method
    def parse_stonks(self, posts):
        stonks = []
        for post in posts:
            stonk_symbol = self.parse_stonk( post )
            if ( stonk_symbol and ( len(stonk_symbol) > 1 ) ) :
                stonks.append([stonk_symbol, post[2]])
        #stonks = filter(posts, stonk)
        return stonks

    def parse_stonk(self, post):
        def stonk_exists(stonk_symbol):
            return stonk_symbol in self.stonk_list
        title = post[0]
        body = post[1]
        words = re.sub('$', '', title).split() + re.sub('$', '', body).split()
        clean_words = [word.upper() for word in words]
        
        # TODO: store stonks that don't exist in database
        #           set up lambda to notify me when a non-existant
        #               stonk occurs frequently
        stonks = list(filter(stonk_exists, clean_words))
        if ( len(stonks) <= 0 ) :
            print('stonk not found')
            return False

        c = Counter(stonks) 
        return c.most_common(1)[0][0]

    # helper methods
    def __build_reddit_client(self, client_id2, client_secret2, user_agent2):
        reddit = praw.Reddit(client_id = client_id2, client_secret = client_secret2, user_agent=user_agent2)
        return reddit


    def __build_stonk_list(self):
        stonk_list = {}
        
        f = open(dirname(abspath(__file__)) + '/tickers.csv', 'r')
        for stonk in f.readlines():
            stonk = stonk.rstrip('\n')
            stonk_list[stonk] = True
        f.close()
        return stonk_list

    def __convert_time(self, t):
        return datetime.utcfromtimestamp(int(t)).strftime('%Y-%m-%d %H:%M:%S')
