# encoding: utf-8
import pickle


def read(file_name):
    with open(file_name, 'r') as f:
        content = f.readlines()
        content = [l.strip('\n') for l in content]

    return content


def flatten_list(lol):
    return [item for sublist in lol for item in sublist]


def flatten_dictionary(dictionary):
    values = []
    for d in dictionary.values():
        for v in d.values():
            values.append(v)
    return values


def dump(obj, file_name):
    with open(file_name, 'w') as f:
        pickle.dump(obj, f)


def load(file_name):
    with open(file_name, 'r') as f:
        return pickle.load(f)
