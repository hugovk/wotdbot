#!/usr/bin/env python
"""
Pick a random [Finnish] word from a word list,
open its Wiktionary page and tweet it
"""
import argparse
import io
import random
import sys
import webbrowser

import yaml  # pip install pyyaml
from twitter import OAuth, Twitter  # pip install twitter


try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+


def load_yaml(filename):
    with open(filename) as f:
        data = yaml.safe_load(f)
    keys = data.viewkeys() if sys.version_info.major == 2 else data.keys()
    if not keys >= {
        'oauth_token', 'oauth_token_secret',
        'consumer_key', 'consumer_secret'
    }:
        sys.exit("Twitter credentials missing from YAML: " + filename)
    return data


def random_word(filename):
    words = []
    with io.open(filename, encoding='utf-8') as infile:
        for line in infile:
            words.append(line.rstrip())
    print("Loaded", len(words), "words")
    randnum = random.randrange(len(words))
    print("Random number:", randnum)
    word = words[randnum]
    print(word)
    return word


def open_url(url):
    print(url)
    if not args.no_web:
        webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


def tweet_it(string, credentials):
    if len(string) <= 0:
        return

    # Create and authorise an app with (read and) write access at:
    # https://dev.twitter.com/apps/new
    # Store credentials in YAML file. See data/onthisday_example.yaml
    t = Twitter(auth=OAuth(credentials['oauth_token'],
                           credentials['oauth_token_secret'],
                           credentials['consumer_key'],
                           credentials['consumer_secret']))

    print("TWEETING THIS:\n", string)

    if args.test:
        print("(Test mode, not actually tweeting)")
    else:
        result = t.statuses.update(status=string)
        url = "http://twitter.com/" + result['user']['screen_name'] + \
            "/status/" + result['id_str']
        print("Tweeted:\n" + url)
        if not args.no_web:
            webbrowser.open(url, new=2)  # 2 = open in a new tab, if possible


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pick a random word from a word list, open its "
        "Wiktionary page and tweet it",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-y', '--yaml',
        default='/Users/hugo/Dropbox/bin/data/wotdbot.yaml',
        help="YAML file location containing Twitter keys and secrets")
    parser.add_argument(
        '-w', '--wordlist', default="data/finnish.txt",
        help="Filename of word list with a single word per line")
    parser.add_argument(
        '-x', '--test', action='store_true',
        help="Test mode: don't tweet")
    parser.add_argument(
        '-nw', '--no-web', action='store_true',
        help="Don't open a web browser to show the tweeted tweet")
    args = parser.parse_args()

    twitter_credentials = load_yaml(args.yaml)

    # Can generate word lists with wotdbot_extract_words.py
    word = random_word(args.wordlist)

    url_word = quote(word.encode('utf8'))

    foreign_url = "https://fi.wiktionary.org/wiki/" + url_word + "#Suomi"
    open_url(foreign_url)

    native_url = "https://en.wiktionary.org/wiki/" + url_word + "#Finnish"
    open_url(native_url)

    tweet = "Finnish word of the day: " + word + " " + native_url + " " + \
        foreign_url + " #Finnish #WOTD #Suomi #" + word.replace(" ", "")
    print("Tweet this:\n", tweet)
    tweet_it(tweet, twitter_credentials)

# End of file
