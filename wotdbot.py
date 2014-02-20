#!/usr/bin/env python
"""
Pick a random [Finnish] word from a word list, open its Wiktionary page and tweet it
"""
import argparse
import io
import random
from twitter import * # https://github.com/sixohsix/twitter `pip install twitter`
import urllib
import webbrowser

# Twitter: create and authorise an app with (read and) write access at https://dev.twitter.com/apps/new
CONSUMER_KEY = "TODO_ADD_YOURS_HERE"
CONSUMER_SECRET = "TODO_ADD_YOURS_HERE"
OAUTH_TOKEN = "TODO_ADD_YOURS_HERE"
OAUTH_TOKEN_SECRET = "TODO_ADD_YOURS_HERE"

def random_word(filename):
    words = []
    with io.open(filename, encoding='utf-8') as infile:
        for line in infile:
            words.append(line.rstrip())
    print "Loaded", len(words), "words"
    randnum = random.randrange(len(words))
    print "Random number:", randnum
    word = words[randnum]
    print word
    return word

def tweet_it(string):
    if len(string) <= 0:
        return

    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET))

    print "TWEETING THIS:\n", string

    if args.test:
        print "(Test mode, not actually tweeting)"
    else:
        result = t.statuses.update(status=string)
        url = "http://twitter.com/" + result['user']['screen_name'] + "/status/" + result['id_str']
        print "Tweeted:\n" + url
        if not args.no_web:
            webbrowser.open(url, new=2) # 2 = open in a new tab, if possible

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pick a random word from a word list, open its Wiktionary page and tweet it", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-w', '--wordlist', default="data/finnish.txt",
        help="Filename of word list with a single word per line")
    parser.add_argument('-x', '--test', action='store_true',
        help="Test mode: don't tweet")
    parser.add_argument('-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    args = parser.parse_args()

    # Can generate word lists with wotdbot_extract_words.py
    word = random_word(args.wordlist)
    
    url = "https://en.wiktionary.org/wiki/" + urllib.quote(word.encode('utf8')) + "#Finnish"
    print url
    if not args.no_web:
        webbrowser.open(url, new=2) # 2 = open in a new tab, if possible

    tweet = "Finnish word of the day: " + word + " " + url + " #Finnish #WOTD"
    print "Tweet this:\n", tweet
    tweet_it(tweet)

# End of file
