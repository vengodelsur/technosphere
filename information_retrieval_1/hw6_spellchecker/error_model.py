# encoding: utf-8
from collections import defaultdict
import numpy as np
import Levenshtein
from utils import flatten_dictionary


class ErrorModel:

    def __init__(self):
        self.insertions = defaultdict(int)
        self.deletions = defaultdict(int)
        self.replacements = defaultdict(lambda: defaultdict(int))

    def update_statistics(self, given, fixed):
        operations = Levenshtein.opcodes(given, fixed)
        for op in operations:
            name, i1, i2, j1, j2 = op[0], op[1], op[2], op[3], op[4]
            if name == 'insert':
                for c in fixed[j1:j2]:
                    self.insertions[c] += 1
            if name == 'delete':
                for c in given[i1:i2]:
                    self.deletions[c] += 1
            if name == 'replace':
                for c1, c2 in zip(given[i1:i2], fixed[j1:j2]):
                    self.replacements[c1][c2] += 1

    def calculate_weights(self):
        self.calculate_replacement_weights()
        self.deletion_weights = ErrorModel.calculate_list_weights(
            self.deletions)
        self.insertion_weights = ErrorModel.calculate_list_weights(
            self.insertions)

    @staticmethod
    def calculate_list_weights(dictionary):
        list_frequencies_to_weights, default_weight = ErrorModel.prepare_weights(
            dictionary.values())
        list_weights = defaultdict(lambda: default_weight)
        for k in dictionary.keys():
            list_weights[k] = list_frequencies_to_weights[dictionary[k]]
        return list_weights

    def calculate_replacement_weights(self):

        replacement_frequencies_to_weights, default_weight = ErrorModel.prepare_weights(
            (flatten_dictionary(self.replacements)))

        self.replacement_weights = defaultdict(
            lambda: defaultdict(lambda: default_weight))
        for k1, v in self.replacements.items():
            for k2 in v.keys():
                self.replacement_weights[k1][
                    k2] = replacement_frequencies_to_weights[self.replacements[k1][k2]]

    @staticmethod
    def prepare_weights(values):
        list_frequencies = np.sort(np.array(values))[::-1]
        list_weights = np.log1p(list_frequencies).astype(float)[::-1]
        list_frequencies_to_weights = {}
        for i in range(len(list_frequencies)):
            list_frequencies_to_weights[list_frequencies[i]] = list_weights[i]
        default_weight = np.max(list_weights)
        return list_frequencies_to_weights, default_weight
