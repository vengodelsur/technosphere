# encoding: utf-8

import dill  # used for pickling lambda functions in defaultdicts used in error model
import pandas as pd
from re import escape
from string import punctuation
from collections import Counter
from utils import read, flatten_list, dump
from error_model import ErrorModel

# READ QUERIES
queries = read('queries_all.txt')
queries = [q.split('\t') for q in queries]
# queries_lod = []
original_queries = []
fixed_queries = []
for q in queries:
    if len(q) == 2:
        original_queries.append(q[0])
        fixed_queries.append(q[1])
        # queries_lod.append({'query': q[0], 'fixed': q[1], 'needs_fix': True})
    else:
        original_queries.append(q[0])
        fixed_queries.append(q[0])
        # queries_lod.append({'query': q[0], 'fixed': q[0], 'needs_fix': False})
# queries_df = pd.DataFrame(queries_lod)

# SPLIT

punctuation = escape(punctuation)

# fixed_queries_to_words =
# queries_df['fixed'].str.decode('utf-8').replace('[' + punctuation +']',
# '', regex=True).str.split()
fixed_queries_to_words = pd.Series(fixed_queries).str.decode(
    'utf-8').replace('[' + punctuation + ']', '', regex=True).str.split()
fixed_words = flatten_list(fixed_queries_to_words)
frequency_dictionary_of_fixed_words = Counter(fixed_words)

# original_queries_to_words =
# queries_df['query'].str.decode('utf-8').replace('[' + punctuation +']',
# '', regex=True).str.split()
original_queries_to_words = pd.Series(original_queries).str.decode(
    'utf-8').replace('[' + punctuation + ']', '', regex=True).str.split()
original_words = flatten_list(original_queries_to_words)
# frequency_dictionary_of_original_words = Counter(original_words)

# CALCULATE ERROR MODEL

error_model = ErrorModel()

for original, fixed in zip(original_queries_to_words, fixed_queries_to_words):
    number_of_words = min(len(original), len(fixed))
    for i in range(number_of_words):
        error_model.update_statistics(original[i], fixed[i])

error_model.calculate_weights()

dump(error_model, 'data/error_model.pkl')
dump(frequency_dictionary_of_fixed_words,
     'data/frequency_dictionary_of_fixed_words.pkl')
