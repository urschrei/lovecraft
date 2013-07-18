# -*- coding: utf-8 -*-
#! /usr/bin/env python
"""
I scraped the text from http://gutenberg.net.au/ebooks06/0600031h.html
wc -w gives the count as 499143 words

"""
import string
import nltk

fd = nltk.FreqDist()
# read in the corpus, remove punctuation, and convert it all to lowercase
# this is slightly slower than reading the entire file into memory
# but it's more memory-efficient by far
# we want to keep the dash/minus, since en and em aren't used in the text
punc = [char for char in string.punctuation]
punc.remove('-')
with open("lovecraft.txt", 'r') as f:
    for line in f:
        inp = line.translate(None, ''.join(punc)).lower().decode('utf8')
        for sent in nltk.sent_tokenize(inp):
            tagged = nltk.pos_tag(nltk.word_tokenize(sent))
            # we really only want nouns
            nouns = [word for word in tagged if word[1] == 'NN']
            if nouns:
                [fd.inc(noun[0].encode('utf8')) for noun in nouns]
