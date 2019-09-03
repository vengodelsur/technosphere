# coding: utf-8
import sys
import re
import random
from operator import itemgetter
import urlparse
from posixpath import split, splitext, normpath
from collections import defaultdict, Counter
from random import sample
from itertools import chain

numeric_substr = re.compile('[^\d]+\d+[^\d]+$')


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def read_lines(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        #lines = [urlparse.unquote(x.strip()) for x in lines]
        lines = [x.strip() for x in lines]
    return lines


def path_to_segments(path):
    tmp = path
    tmp = normpath(tmp)
    segments = []
    while tmp != "/":
        (tmp, last) = split(tmp)
        segments.insert(0, last)
    return segments


def segments_to_features(segments):
    features = []

    # 1
    #features.append('segments:' + str(len(segments)))
    features.append('segments:%d' % len(segments))
    for index, string in enumerate(segments):
        # 4a
        #features.append('segment_name_' + str(index) + ':' + str(string))
        features.append('segment_name_%d:%s' % (index, string))
        # 4b
        if is_number(string):
            #features.append('segment_[0-9]_' + str(index) + ':' + '1')
            features.append('segment_[0-9]_%d:1' % index)
        # 4d
        extension = splitext(string)[1][1:]
        if extension:
            #features.append('segment_ext_' + str(index) + ':' + extension)
             features.append('segment_ext_%d:%s' % (index, extension))
        # 4c
        string = urlparse.unquote(string)

        if numeric_substr.match(string):
            #features.append('segment_substr[0-9]_' + str(index) + ':' + '1')
            features.append('segment_substr[0-9]_%d:1' % index)
            # 4e
            if extension:
                #features.append('segment_ext_substr[0-9]_' + str(index) + ':' + extension)
                features.append('segment_substr[0-9]_%d:%s' % (index, extension))
        # 4f
        #features.append('segment_len_' + str(index) + ':' + str(len(string)))  
        features.append('segment_len_%d:%d' % (index, len(string)))
        
    return features
def query_to_params_features(query):
    features = []
    if query:        
        parameters = dict(urlparse.parse_qsl(query))
        # 2
        features.append('param_name:' + str(parameters.keys()))
        for parameter, value in parameters.iteritems():
            # 3
            features.append('param:' + str(parameter) + '=' + str(value))   
    return features

def url_list_to_features(url_list):
    features = defaultdict(list)
    for url in url_list:
        parsed_url = urlparse.urlparse(url)
        segments = path_to_segments(parsed_url.path)
        features[url] += segments_to_features(segments)
        features[url] += query_to_params_features(parsed_url.query)
    return features

def url_list_to_all_features(url_list):
    features = []
    for url in url_list:
        parsed_url = urlparse.urlparse(url)
        segments = path_to_segments(parsed_url.path)
        features += segments_to_features(segments)
        features += query_to_params_features(parsed_url.query)
    return features
        
    
def frequency(dictionary_of_lists, threshold):
    frequencies = Counter(chain.from_iterable(dictionary_of_lists.values()))
    frequencies = {feature:count for feature, count in frequencies.iteritems() if count > threshold}
    return sorted(frequencies.items(), key=itemgetter(1), reverse=True)

def write_features(file_name, features):
    with open(file_name, 'w') as f:
        f.write('\n'.join('%s\t%s' % x for x in features))
       
def extract_features(INPUT_FILE_1, INPUT_FILE_2, OUTPUT_FILE):
    
    examined_urls = read_lines(INPUT_FILE_1)
    general_urls = read_lines(INPUT_FILE_2)\
    
    size = len(examined_urls) / 2
    examined_urls = sample(examined_urls, size)
    general_urls = sample(general_urls, size)
    
    # features = url_list_to_features(examined_urls + general_urls)    
    features = url_list_to_all_features(examined_urls + general_urls) 
    
    # frequency
    alpha = 0.1
    threshold = size * alpha
    # write_features(OUTPUT_FILE, frequency(features, threshold))
    frequencies = Counter(features)
    frequencies = {feature:count for feature, count in frequencies.iteritems() if count > threshold}
    frequencies = sorted(frequencies.items(), key=itemgetter(1), reverse=True)
    write_features(OUTPUT_FILE, frequencies)
    # return features
    # print >> sys.stderr, "Not implemented"


