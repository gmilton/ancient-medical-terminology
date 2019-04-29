#!/usr/bin/env python3

import sys
import csv
import os

ARGUMENTS = sys.argv[1:]
FILENAME = 'word_lists.csv'
PREFIX = ''
CONTAINS = ''
MEANING = ''
POS = ''
POS_DIR = {'wr'  : 'Word Root',
           'suf' : 'Suffix',
           'pre' : 'Prefix',
           'ba'  : 'Body Axis',
           'pos' : 'Position' }

class Word(object):
    def __init__(self, word):
        self.term = word[0]
        self.definition = word[1]
        self.greek_latin = word[2]
        self.pos = word[3]

def usage(exit_code=0):
    print('''Usage: {} [-f filename -p PREFIX -l]
    -f   FILENAME Load in words from file (Default: \'word_lists.csv\')
    -p   PREFIX   Get all words beginning with prefix
    -c   CONTAINS Get words containing substring (to be: word matching)
    -m   MEANING  Get words that contain MEANING in their definition
    -pos POS      Narrow down list by part of speech (wr, suf, pre, ba, pos)'''.format(os.path.basename(sys.argv[0])))
    sys.exit(exit_code)


def load_words():
    word_list = []

    with open(FILENAME, newline='') as csvfile:
        wlreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(wlreader):
            if index: # ignore first line with template
                word_list.append(Word(row))

    return word_list

def list_all(word_list):
    for i, w in enumerate(word_list):
        print("Term {}: {}\nDefinition: {}\nGreek/Latin: {}\nPOS: {}\n\n".format(i + 1, w.term, w.definition, w.greek_latin, w.pos))

    print("Grace 'G$' Milton's Project for CLAS 30330")

def prefix(word_list):
    new_word_list = []

    for word in word_list:
        if word.term.lower().startswith(PREFIX.lower()):
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def contains(word_list):
    new_word_list = []

    for word in word_list:
        if CONTAINS.lower() in word.term.lower():
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def meaning(word_list):
    new_word_list = []

    for word in word_list:
        if MEANING.lower() in word.definition.lower():
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def pos(word_list):
    new_word_list = []

    for word in word_list:
        if word.pos == POS:
            new_word_list.append(word)

    return sorted(new_word_list, key=lambda w: w.term)

def list_pos(word_list):

    pos_set = set()

    for word in word_list:
        pos_set.add(word.pos)

    for pos in pos_set:
        print(pos)

if __name__ == "__main__":

    while ARGUMENTS and ARGUMENTS[0].startswith('-') and len(ARGUMENTS[0]) > 1:
        arg = ARGUMENTS.pop(0)
        if arg == '-f':
            FILENAME = ARGUMENTS.pop(0)
        elif arg == '-p':
            PREFIX = ARGUMENTS.pop(0)
        elif arg == '-c':
            CONTAINS = ARGUMENTS.pop(0)
        elif arg == '-m':
            MEANING = ARGUMENTS.pop(0)
        elif arg == '-pos':
            POS = ARGUMENTS.pop(0)
            if POS in POS_DIR:
                POS = POS_DIR[POS]
            else:
                POS = ''
        elif arg == '-h':
            usage(0)
        else:
            usage(1)

    word_list = load_words()
 
    if PREFIX:
        word_list = prefix(word_list)
    if CONTAINS:
        word_list = contains(word_list)
    if MEANING:
        word_list = meaning(word_list)
    if POS:
        word_list = pos(word_list)

    list_all(word_list)
