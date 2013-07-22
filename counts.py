#/usr/bin/env/python

import os
import string
import requests
from bs4 import BeautifulSoup
import nltk
import pickle
import matplotlib.pyplot as plt


def classify():
    """
    Read in the corpus, remove punctuation, and convert it all to lowercase
    This is slightly slower than reading the entire file into memory
    but it's more memory-efficient by far
    We want to keep the dash/minus, since en and em aren't used in the text

    """
    punc = [char for char in string.punctuation]
    punc.remove('-')
    punc.remove('.')
    if not os.path.isfile('results.pickle'):
        cleanup = []
        soup = BeautifulSoup(
            requests.get("http://gutenberg.net.au/ebooks06/0600031h.html").text)
        # leading and trailing paras don't contain anything useful
        text = tuple(sec.get_text().encode('utf8') for sec in soup.find_all('p')[4:-5])
        for line in text:
            inp = line.translate(None, ''.join(punc)).lower().decode('utf8')
            for sent in nltk.sent_tokenize(inp):
                tagged = nltk.pos_tag(nltk.word_tokenize(sent))
                cleanup.append(tagged)
        # classification is time-consuming. Let's save our results
        with open('results.pickle', 'w') as out:
            pickle.dump(cleanup, out)
    else:
        cleanup = pickle.load('results.pickle')
    return cleanup


def restrict(tagged_sentences, tags):
    """
    remove words we don't want to count
    classifications are here:
    from http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    returns an NLTK frequency distribution object

    """

    fd = nltk.FreqDist()
    for classified in tagged_sentences:
        words = [word for word in classified if word[1] in tags]
        if words:
            [fd.inc(word[0]) for word in words]
    return fd

permitted_tags = set([
    'JJS',
    'FW',
    'NN',
    'NNS',
    'NNP',
    'NNPS',
    'UH',
])


counts = restrict(classify(), permitted_tags)
# Let's do some plotting
plt.xkcd()
counts.plot(100, color='r')
plt.xlabel("Nouns")
plt.tick_params(axis='x', which='both', top='off', labelsize=10)
plt.title(
    "100 most frequently-occurring words in 'The Collected Works of H. P. Lovecraft'")
plt.tight_layout()
# Now manually resize the graph horizontally, and call tight_layout again
