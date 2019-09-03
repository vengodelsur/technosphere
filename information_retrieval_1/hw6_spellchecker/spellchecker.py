# encoding: utf-8
import operator
import re
import numpy as np
from string import punctuation
from utils import load
from prefix_tree import Candidate, Node, SearchTree

# cyrillic_to_latin = {u'.': u'/', u'\u0431': u',', u'\u0430': u'f',
# u'\u0433': u'u', u'\u0432': u'd', u'\u0435': u't', u'\u0434': u'l',
# u'\u0437': u'p', u'\u0436': u';', u'\u0439': u'q', u'\u0438': u'b',
# u'\u043b': u'k', u'\u043a': u'r', u'\u043d': u'y', u'\u043c': u'v',
# u'\u043f': u'g', u'\u043e': u'j', u'\u0441': u'c', u'\u0440': u'h',
# u'\u0443': u'e', u'\u0442': u'n', u'\u0445': u'[', u'\u0444': u'a',
# u'\u0447': u'x', u'\u0446': u'w', u'\u0449': u'o', u'\u0448': u'i',
# u'\u044b': u's', u'\u044a': u']', u'\u044d': u"'", u'\u044c': u'm',
# u'\u044f': u'z', u'\u044e': u'.', u'\u0451': u'`'}

latin_to_cyrillic = {39: 1101, 44: 1073, 46: 1102, 47: 46, 59: 1078, 91: 1093, 93: 1098, 96: 1105, 97: 1092, 98: 1080, 99: 1089, 100: 1074, 101: 1091, 102: 1072, 103: 1087, 104: 1088, 105:
                     1096, 106: 1086, 107: 1083, 108: 1076, 109: 1100, 110: 1090, 111: 1097, 112: 1079, 113: 1081, 114: 1082, 115: 1099, 116: 1077, 117: 1075, 118: 1084, 119: 1094, 120: 1095, 121: 1085, 122: 1103}


def fix_word(word):
    global tree
    candidates = tree.generate(
        word, max_number_of_candidates=60, max_sum_of_weights=2, part=0.7)
    if len(candidates) < 1:
        return Candidate(word=word, frequency=0, fixes_weight=0)
    else:
        candidates.sort(key=operator.attrgetter('frequency'))
        candidates.sort(key=operator.attrgetter('fixes_weight'))
        part = max(1, len(candidates) / 8)
        candidates = candidates[:part]
        return sorted(candidates, key=operator.attrgetter('frequency'))[-1]


def fix_tokens(tokens):
    result = ''
    frequency = 0
    fixes_weight = 0
    for t in tokens:
        is_word = not re.match('[' + punctuation + ' ' + ']*$', t)
        if is_word:
            fixed = fix_word(t)
            t = fixed.word
            frequency += fixed.frequency
            fixes_weight += fixed.fixes_weight
        result += t

    return Candidate(word=result, frequency=frequency, fixes_weight=fixes_weight)


def split_join_tokens(tokens):
    global frequency_dictionary_of_fixed_words
    words = frequency_dictionary_of_fixed_words.keys()
    joined = False
    split = False
    words_positions = []
    split_tokens = []

    for i, token in enumerate(tokens):
        if token.isalpha():
            words_positions.append(i)

    for i in words_positions:
        token = tokens[i]
        if len(token) > 2:
            for pos in range(1, len(token)):
                left = token[:pos]
                right = token[pos:]
                if (left in words and right in words) and (token not in words):
                    split_tokens = list(tokens)
                    split_tokens[i] = right
                    split_tokens.insert(i, u' ')
                    split_tokens.insert(i, left)
                    split = True
                    break
        if (split == True):
            break

    for i in range(len(words_positions) - 1):
        left = tokens[words_positions[i]]
        right = tokens[words_positions[i + 1]]
        if (left not in words or right not in words) and left + right in words:
            tokens[words_positions[i]] = left + right
            for pos in sorted(range(words_positions[i] + 1, words_positions[i + 1] + 1), reverse=True):
                del tokens[pos]
            joined = True
            break

    return tokens, joined, split_tokens, split


def fix_query(query):
    result = ''

    # GENERATOR
    tokens = re.split('([' + punctuation + ' ' + '])', query)
    candidate = fix_tokens(tokens)

    # LAYOUT
    if re.search('[a-zA-Z]', query):
        cyrillic_query = query.translate(latin_to_cyrillic)
        cyrillic_tokens = re.split(
            '([' + punctuation + ' ' + '])', cyrillic_query)
        cyrillic_candidate = fix_tokens(cyrillic_tokens)
        if cyrillic_candidate.frequency > candidate.frequency:
            return cyrillic_candidate.word
    # SPLIT, JOIN
    joined_tokens, joined, split_tokens, split = split_join_tokens(tokens)
    if joined:
        joined_candidate = fix_tokens(joined_tokens)
        if joined_candidate.fixes_weight < candidate.fixes_weight:
            return joined_candidate.word
    if split:
        split_candidate = fix_tokens(split_tokens)
        return split_candidate.word

    return candidate.word


def iterations(query):
    max_counter = 3
    iterations_counter = 0

    query = query.decode('utf-8')

    while (iterations_counter < max_counter):

        new_query = fix_query(query)
        if (new_query == query):
            break
        query = new_query
        iterations_counter += 1

    return new_query


error_model = load('data/error_model.pkl')
frequency_dictionary_of_fixed_words = load(
    'data/frequency_dictionary_of_fixed_words.pkl')
tree = SearchTree(error_model)
for word, frequency in frequency_dictionary_of_fixed_words.iteritems():
    tree.add(word, frequency)
punctuation = re.escape(punctuation)

while (True):
    try:
        query = raw_input()
    except (EOFError):
        break

    print iterations(query).encode('utf-8')
