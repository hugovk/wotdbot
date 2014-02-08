#!/usr/bin/env python
"""
Extract [Finnish] words from English Wiktionary.

Download enwiktionary-20140118-pages-articles-multistream.xml.bz2 (484.5M) 
or newer and unzip. Then run:

python wotdbot_extract_words.py > finnish.txt

For other languages, change "Finnish" in the if and "fi" in the regex.
"""
import re

words = set() # a set ensures no duplicates

with open("enwiktionary-20140118-pages-articles-multistream.xml") as infile:
    for line in infile:
        if "* Finnish: " in line:
            # https://en.wiktionary.org/wiki/Help:Translations
            
            # Match first text after t|fi in double squiggly brackets, for example:
            # * Finnish: {{t+|fi|muukalainen}}, {{t+|fi|ulkomaalainen}}, {{t|fi|vierasmaalainen}}
            # ->
            # muukalainen

            # May or may not have a plus: {t+|fi|  or {t|fi|   (plus indicates fi.wiki page)
            # May have grammatical gender, like the "|p" in:
            # * Finnish: {{t+|fi|tee}}, {{t|fi|teenlehdet|p}}
            
            match = re.match(r"[^{]*{{t[+]+\|fi\|([^}|]+)", line)
            if match:
                # Test:
                # print line.rstrip()
                # print match.group(0), "--->", match.group(1)

                # print match.group(1)
                words.add(match.group(1))
                
# print len(words)

for word in words:
    print word

# End of file
