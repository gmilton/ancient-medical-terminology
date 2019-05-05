import csv

FILENAME = 'word_lists.csv'

class Word(object): 
    def __init__(self, word): 
        self.term = word[0].replace("-", "").replace(" ", "") 
        self.definition = word[1] 
        self.greek_latin = word[2] 
        self.pos = word[3] 
 
class Node(object): 
    def __init__(self, word): 
        self.word = word 
        self.children = [] 
 
    def __str__(self, level=0): 
        ret = str(level)+":"+repr(self.word.term)+";" 
        for child in self.children: 
            ret += child.__str__(level+1) 
        return ret 
 
    def __repr__(self): 
        return '<tree node representation>' 
 
class Tree(object): 
    def __init__(self, root): 
        self.root = root 

def load_words():
    word_list = []

    with open(FILENAME, newline='') as csvfile:
        wlreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for index, row in enumerate(wlreader):
            if index: # ignore first line with template
                word_list.append(Word(row))

    return word_list
