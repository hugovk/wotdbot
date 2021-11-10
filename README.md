wotdbot
=======

[![GitHub Actions status](https://github.com/hugovk/wotdbot/workflows/Test/badge.svg)](https://github.com/hugovk/wotdbot/actions)
[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

Word-of-the-day robot for tweeting a word of the day.

First you need a list of Wiktionary words. There's a Finnish one in the data directory. It was made like this

Download enwiktionary-20140118-pages-articles-multistream.xml.bz2 (484.5M) or newer from the [Wiktionary data dumps](https://dumps.wikimedia.org/enwiktionary/latest/) and unzip. Then run:

    python wotdbot_extract_words.py > data/finnish.txt

For other languages, change "Finnish" in the `if` and "fi" in the regex.

Then run like from a scheduled task/crontab:

    python wotdbot.py --wordlist data/finnish.txt --yaml data/wotdbot.yaml --no-web

See an example at https://twitter.com/fiwotd
