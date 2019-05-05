from flask import Flask, render_template, jsonify
from words import load_words, Word, Node, Tree
import collections
app = Flask(__name__)

TERMS, DEFS = "terms", "definitions"
AVAILABLE_COMMANDS = {
    'Terms': TERMS,
    'Definitions': DEFS
}
WORD_LIST = load_words()

def search_terms(word_list, search):
    new_word_list = []

    for word in word_list:
        if search.lower() in word.term.lower():
            entry = {}
            entry['term'] = word.term
            entry['definition'] = word.definition
            entry['greek_latin'] = word.greek_latin
            entry['pos'] = word.pos
            new_word_list.append(entry)

    return sorted(new_word_list, key=lambda w: w['term'])

def search_defs(word_list, search):
    new_word_list = []

    for word in word_list:
        if search.lower() in word.definition.lower():
            entry = {}
            entry['term'] = word.term
            entry['definition'] = word.definition
            entry['greek_latin'] = word.greek_latin
            entry['pos'] = word.pos
            new_word_list.append(entry)

    return sorted(new_word_list, key=lambda w: w['term'])

def find_prefix(word_list, prefix):
    new_word_list = []

    for word in word_list:
        if word.term.lower().startswith(prefix.lower()):
            entry = {}
            entry['term'] = word.term
            entry['definition'] = word.definition
            entry['greek_latin'] = word.greek_latin
            entry['pos'] = word.pos
            new_word_list.append(entry)

    return sorted(new_word_list, key=lambda w: w['term'])

def find_pos(word_list, pos):
    new_word_list = []

    for word in word_list:
        if word.pos == pos:
            entry = {}
            entry['term'] = word.term
            entry['definition'] = word.definition
            entry['greek_latin'] = word.greek_latin
            entry['pos'] = word.pos
            new_word_list.append(entry)

    return sorted(new_word_list, key=lambda w: w['term'])

def find_all_wr(word_list, term):
    wr_start_dict = collections.defaultdict(list)
    word_roots = []
    terms_list = []

    for word in word_list:
        if word.term.lower() in term:
            i = term.find(word.term.lower())
            wr_start_dict[i].append(word)
            entry = {}
            entry['term'] = word.term
            entry['definition'] = word.definition
            entry['greek_latin'] = word.greek_latin
            entry['pos'] = word.pos
            terms_list.append(entry)
            word_roots.append(word)

    return wr_start_dict, word_roots, terms_list

def combine_wrs(wr_dict, wr_list, term):
    possible_parses = []
    i = list(sorted(wr_dict.keys()))[0]
    for wr in wr_dict[i]:
        node = Node(wr)
        possible_parses.append(Tree(node))
    for branch in possible_parses:
        j = i
        node = branch.root
        frontier = [[node, j]]
        while frontier:
            node, j = frontier.pop(0)
            k = j + len(node.word.term)
            j = find_next_wr(wr_dict, term, k)
            while j and j < len(term):
                for wr in wr_dict[j]:
                    child = Node(wr)
                    node.children.append(child)
                    frontier.append([child, j])
                j += 1
    for p in possible_parses:
        print(p.root)
    return possible_parses

def find_next_wr(wr_dict, term, i):
    while i not in wr_dict and i < len(term):
        i += 1
    if i >= len(term):
        return None
    return i

@app.route('/')
def hello():
    return render_template('index.html', commands=AVAILABLE_COMMANDS)

#rendering the HTML page which has the button
#@app.route('/terms')
#def terms():
#    return render_template('terms.html')

@app.route('/<cmd>')
def command(cmd=None):
    cmd = cmd.split(";")
    if cmd[0] == "search":
        if cmd[1] == TERMS:
            if cmd[2]:
                search = cmd[2]
            else:
                search = "NULL"
            terms_list = search_terms(WORD_LIST, search)
            response = {}
            response['terms'] = terms_list
        elif cmd[1] == DEFS:
            if cmd[2]:
                search = cmd[2]
            else:
                search = "NULL"
            terms_list = search_defs(WORD_LIST, search)
            response = {}
            response['terms'] = terms_list
    elif cmd[0] == "prefix":
        prefix = cmd[1]
        terms_list = find_prefix(WORD_LIST, prefix)
        response = {}
        response['terms'] = terms_list
    elif cmd[0] == "pos":
        pos = cmd[1]
        terms_list = find_pos(WORD_LIST, pos)
        response = {}
        response['terms'] = terms_list
    elif cmd[0] == 'parse':
        parse = cmd[1]
        wr_dict, wr_list, terms_list = find_all_wr(WORD_LIST, parse)
        possible_parses = combine_wrs(wr_dict, wr_list, parse)
        response = {}
        response['terms'] = terms_list
        parses_list = []
        parses_dict = {}
        for p in possible_parses:
            parses_list.append(p.root.__str__())
        for p in parses_list:
            parts = p.split(";")
            parts.pop()
            last_seen = []
            last_level = -1
            levels_seen = set()
            #for elem in parts:
                #level, elem = elem.split(":")
                #elem = elem.replace("'", "")
                #if level == 0:
                    #parses_dict[elem] = {}
                #elif level == last_level:
                    
                #elif level > last_level:
                    #next_dict[elem] = {} 
                #elif level < last_level:
                    #
                #last_level = level
                #if level in levels_seen:
                    #last_level[level] = elem
                #else:
                    #last_level.append(elem)
                #levels_seen.add(level)
            print(parts)
        response['parses'] = parses_list
    else:
        response = 'No search done'
    return jsonify(response), 200, {'Content-Type': 'application/json'}

#background process happening without any refreshing
#@app.route('/search_terms')
#def search_terms():
#    print("Hello")
#    return "nothing"
