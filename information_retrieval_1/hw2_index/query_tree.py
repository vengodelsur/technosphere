# coding: utf-8
import re
import unittest
import mmh3
import varbyte

SPLIT_RGX = re.compile(r'\w+|[\(\)&\|!]', re.U)

class QtreeTypeInfo:
    def __init__(self, value, op=False, bracket=False, term=False):
        self.value = value
        self.is_operator = op
        self.is_bracket = bracket
        self.is_term = term

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if isinstance(other, QtreeTypeInfo):
            return self.value == other.value
        return self.value == other


class QTreeTerm(QtreeTypeInfo):
    def __init__(self, term):
        QtreeTypeInfo.__init__(self, term, term=True)


class QTreeOperator(QtreeTypeInfo):
    def __init__(self, op):
        QtreeTypeInfo.__init__(self, op, op=True)
        self.priority = get_operator_prio(op)
        self.left = None
        self.right = None


class QTreeBracket(QtreeTypeInfo):
    def __init__(self, bracket):
        QtreeTypeInfo.__init__(self, bracket, bracket=True)


def get_operator_prio(s):
    if s == '|':
        return 0
    if s == '&':
        return 1
    if s == '!':
        return 2

    return None


def is_operator(s):
    return get_operator_prio(s) is not None


def tokenize_query(q):
    tokens = []
    for t in map(lambda w: w.lower().encode('utf-8'), re.findall(SPLIT_RGX, q)):
        if t == '(' or t == ')':
            tokens.append(QTreeBracket(t))
        elif is_operator(t):
            tokens.append(QTreeOperator(t))
        else:
            tokens.append(QTreeTerm(t))

    return tokens


def build_query_tree(tokens):
    """ write your code here """
    # should be ok for simple queries

    if len(tokens) == 1:
        return tokens[0]
    #depth = 0
    for i, token in enumerate(tokens):
        #if token.value == '(':
            #token.left = build_query_tree(tokens[0:i])
        if token.is_operator:
            token.left = build_query_tree(tokens[0:i])
            token.right = build_query_tree(tokens[i+1:])
            #depth += 1
            return token #, depth
    
        
    return root#, depth
    
def evaluate_query_tree(root, index):
    # should be ok for simple queries
    # print root.value
    if root.is_term:
        return set(varbyte.decompress(index[mmh3.hash(root.value)]))
    if root.is_operator:
        left_set = evaluate_query_tree(root.left, index)
        right_set = evaluate_query_tree(root.right, index)
        return left_set.intersection(right_set)

def parse_query(q):
    tokens = tokenize_query(q)
    return build_query_tree(tokens)


""" Collect query tree to sting back. It needs for tests. """
def qtree2str(root, depth=0):
    if root.is_operator:
        need_brackets = depth > 0 and root.value != '!'
        res = ''
        if need_brackets:
            res += '('

        if root.left:
            res += qtree2str(root.left, depth+1)

        if root.value == '!':
            res += root.value
        else:
            res += ' ' + root.value + ' '

        if root.right:
            res += qtree2str(root.right, depth+1)

        if need_brackets:
            res += ')'

        return res
    else:
        return root.value

    

