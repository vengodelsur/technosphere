# encoding: utf-8
class Candidate:

    def __init__(self, word, fixes_weight, frequency):
        self.word = word
        self.fixes_weight = fixes_weight
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)


class Node:

    def __init__(self, c):
        self.c = c
        self.children = []
        self.end_of_word = False
        self.frequency = 0

    def add_child(self, node):
        self.children.append(node)


class SearchTree:

    def __init__(self, error_model):
        self.root = Node(None)
        self.candidates = []
        self.error_model = error_model

    def add(self, word, frequency):
        node = self.root
        for c in word:
            c_in_child = False
            for child in node.children:
                if child.c == c:
                    # child.frequency += 1
                    node = child
                    c_in_child = True
                    break
            if not c_in_child:
                new_node = Node(c)
                # new_node.frequency += 1
                node.add_child(new_node)
                node = new_node
        node.frequency = frequency
        node.end_of_word = True

    def find_prefix(self, prefix):  # returns number of occurencies
        node = self.root
        if not self.root.children:
            return 0
        for c in prefix:
            c_not_found = True
            for child in node.children:
                if child.c == c:
                    c_not_found = False
                    node = child
                    break
            if c_not_found:
                return 0
        return node.frequency

    def modify_candidates_list(self, candidate):
        new_candidate = True
        for cand in self.candidates:
            if cand.word == candidate.word:
                new_candidate = False
                cand.frequency = max(candidate.frequency, cand.frequency)
                cand.fixes_weight = min(
                    candidate.fixes_weight, cand.fixes_weight)
        if new_candidate and len(self.candidates) <= self.max_number_of_candidates:
            self.candidates.append(candidate)

    def can_be_added(self, weight, part=1):
        return (weight < self.max_sum_of_weights and len(self.candidates) <= part * self.max_number_of_candidates)

    def find_candidates(self, prefix, result='', root=None, weight=0, part=1):  # returns number of occurencies

        if root is None:
            root = self.root
        node = root

        if len(prefix) < 1:
            if node.end_of_word:
                self.modify_candidates_list(
                    Candidate(result, weight, node.frequency))
            return

        c = prefix[0]

        for child in node.children:
            if child.c == c:
                self.find_candidates(
                    prefix[1:], result + c, child, weight, part)

                # insert
                additional_weight = self.error_model.insertion_weights[c]
                if self.can_be_added(weight + additional_weight, part):
                    self.find_candidates(
                        prefix, result + c, child, weight + additional_weight, part)

            else:
                fix = child.c

                # replace
                additional_weight = self.error_model.insertion_weights[fix]
                if self.can_be_added(weight + additional_weight, part):
                    self.find_candidates(
                        prefix, result + fix, child, weight + additional_weight, part)

                # insert
                additional_weight = self.error_model.replacement_weights[
                    c][fix]
                if self.can_be_added(weight + additional_weight, part):
                    self.find_candidates(
                        prefix[1:], result + fix, child, weight + additional_weight, part)
        # delete
        additional_weight = self.error_model.deletion_weights[c]
        if self.can_be_added(weight + additional_weight):
            self.find_candidates(
                prefix[1:], result, node, weight + additional_weight, part)
        return

    def generate(self, word, max_number_of_candidates=5, max_sum_of_weights=10, part=1):
        self.max_number_of_candidates = max_number_of_candidates
        self.max_sum_of_weights = max_sum_of_weights
        self.candidates = []
        self.find_candidates(word, part=part)
        return self.candidates
