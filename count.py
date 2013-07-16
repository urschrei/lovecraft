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
with open("lovecraft.txt", 'r') as f:
    for line in f:
        inp = line.translate(None, string.punctuation).lower()
        for sent in nltk.sent_tokenize(inp):
            for word in nltk.word_tokenize(sent):
                fd.inc(word)
