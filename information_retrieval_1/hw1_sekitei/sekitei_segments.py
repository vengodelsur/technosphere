 # coding: utf-8


import sys
import os
import re
import random
import time
from sklearn.cluster import KMeans
import numpy
# from numpy import isin, array, arange
from operator import itemgetter
from urlparse import unquote, urlparse, parse_qsl
from posixpath import split, splitext, normpath
from collections import defaultdict, Counter
from random import sample
from itertools import chain
from pandas import DataFrame, Series, concat
#from sklearn.linear_model import LogisticRegression
#from xgboost import XGBClassifier
import random
# EXTRACTING FEATURES PART

numeric_substr = re.compile('[^\d]+\d+[^\d]+$')
is_wiki = re.compile('^/wiki/')
date = re.compile('.*/\d\d/\d\d/')
year = re.compile('.*[^\d]+(19\d\d|20\d\d)[^\d]*')
wiki_features = {
    #'category:1': re.compile('^/wiki/Категория:'),
                 #'wiki:1': re.compile('.+Википедия:'),
                 #'portal:1': re.compile('.+Портал:'),
                 #'project:1': re.compile('.+Проект:'),
                 #'template:1': re.compile('.+Шаблон:'),
                 #'service:1': re.compile('.+Служебная:'),
                 #'file_page:1': re.compile('^/wiki/Файл:[^/]+$'),
                 'talk:1': re.compile('.+Обсуждение:'),
                 'image:1': re.compile('.+Изображение:'),
                 #'incubator:1': re.compile('^.+Инкубатор:'),
                 'surname:1': re.compile('^/wiki/[^/]+,_[^/]+$'),
                 #'number:1': re.compile('^/wiki/[^/]+_\(число\)$'),
                 #'user:1': re.compile('^/wiki/user:[^/]+$'),
                 #'album:1': re.compile('^/wiki/[^/]+_\(альбом\)$'),
                 #'year:1': re.compile('^/wiki/.+год'),
                 'brackets:1': re.compile('^/wiki/[^/]+\([^/]+\)$')
}
wiki_starts = {'category:1': '/wiki/Категория:',
               'file_page:1': '/wiki/Файл:',
               'user:1': '/wiki/user:'#,
               #'en_category:1': '/wiki/Category:',
               #'en_file_page:1': '/wiki/File:',
               #'en_talk:1': '/wiki/Talk:',
               #'en_image:1': '/wiki/Image:'
              }


class sekitei:
    pass


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def is_ascii(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
    
def read_lines(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        # lines = [unquote(x.strip()) for x in lines]
        lines = [x.strip() for x in lines]
    return lines


def write_lines(file_name, url_list):
    with open(file_name, 'w') as f:
        lines = unquote('\n'.join(url_list))
        f.write(lines)


def path_to_segments(path):
    tmp = path
    tmp = normpath(tmp)
    segments = []
    while tmp != "/":
        (tmp, last) = split(tmp)
        segments.insert(0, last)
    return segments


def path_to_special_features(path):
    features = []
    if year.match(path):
                #if int(string) < 2010:
        features.append('year_given:1')
    
    if is_ascii(path):
        features.append('ascii:1')
    
    if date.match(path):
        features.append('date:1')
    
    if path.startswith('/wiki/'):
    
        for name, regex in wiki_features.iteritems():
            if regex.match(path):
                features.append(name)
        for name, string in wiki_starts.iteritems():
            if path.startswith(string):
                features.append(name)
        features.append('_:' + str(path.count('_')))
    return features


def segments_to_features(segments):
    features = []
   
    # 1
    features.append('segments:' + str(len(segments)))
    # features.append('segments:%d' % len(segments))
    for index, string in enumerate(segments):
        
        
        
        # 4a
        features.append('segment_name_' + str(index) + ':' + str(string))
        # features.append('segment_name_%d:%s' % (index, string))
        # 4b
        if is_number(string):
            features.append('segment_[0-9]_' + str(index) + ':' + '1')
            # features.append('segment_[0-9]_%d:1' % index)
            
        # 4d
        extension = splitext(string)[1][1:]
        if extension:
            features.append('segment_ext_' + str(index) + ':' + extension)
            # features.append('segment_ext_%d:%s' % (index, extension))
        # 4c
        # string = unquote(string)

        if numeric_substr.match(string):
            features.append('segment_substr[0-9]_' + str(index) + ':' + '1')
            # features.append('segment_substr[0-9]_%d:1' % index)
            # 4e
            if extension:
                features.append(
                    'segment_ext_substr[0-9]_' + str(index) + ':' + extension)
                # features.append('segment_substr[0-9]_%d:%s' % (index, extension))
        # 4f
        features.append('segment_len_' + str(index) + ':' + str(len(string)))
        # features.append('segment_len_%d:%d' % (index, len(string)))

    return features


def query_to_params_features(query):
    features = []
    if query:
        parameters = dict(parse_qsl(query))
        # 2
        features.append('param_name:' + str(parameters.keys()))
        # features.append('param_name:%s' % str(parameters.keys()))
        for parameter, value in parameters.iteritems():
            # 3
            features.append('param:' + str(parameter) + '=' + str(value))
            # features.append('param:%s=%s' % (parameter, value))
    return features


def url_to_features_list(url):
    features_list = []
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    segments = path_to_segments(path)
    features_list += segments_to_features(segments)
    features_list += query_to_params_features(parsed_url.query)
    features_list += path_to_special_features(path)
    return features_list


def url_list_to_features(url_list):
    features = defaultdict(list)
    for url in url_list:
        features[url] = url_to_features_list(url)
    return features

# DEFINING SEGMENTS PART


def dictionary_of_lists_to_dataframe(dictionary_of_lists):
    df = DataFrame.from_dict(dictionary_of_lists, orient='index')
    df = df.stack().reset_index()
    df.level_1 = 1
    df = df.pivot(index='level_0', columns=0, values='level_1').fillna(0)
    return df


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def combine_features(qlink_features, unknown_features):
    qlink_df = dictionary_of_lists_to_dataframe(qlink_features)
    qlink_df['is_qlink'] = 1
    unknown_df = dictionary_of_lists_to_dataframe(unknown_features)
    unknown_df['is_qlink'] = 0
    df = concat([qlink_df, unknown_df], axis=0).fillna(0)
    # !!! contains is_qlink info
    return df


def choose_features(dictionary_of_lists, threshold):
    frequencies = Counter(chain.from_iterable(dictionary_of_lists.values()))

    frequencies = {feature: count for feature,
                   count in frequencies.iteritems() if count > threshold}
    features_list = frequencies.keys()

    return features_list


def max_series(s1, s2):
    return DataFrame([s1, s2]).max()


def define_segments(QLINK_URLS, UNKNOWN_URLS, QUOTA):
    global sekitei

    MIN_QUOTA = 100

    # print "define_segments is not implemented";
    qlink_features = url_list_to_features(QLINK_URLS)
    unknown_features = url_list_to_features(UNKNOWN_URLS)
    sekitei.dataframe = combine_features(qlink_features, unknown_features)

    all_features_dict = merge_two_dicts(qlink_features, unknown_features)
    sekitei.alpha = 0.01
    size = len(QLINK_URLS)  + len(UNKNOWN_URLS)
    
    # threshold_frequency = 0
    threshold_frequency = size * sekitei.alpha
    sekitei.dataframe = sekitei.dataframe[
        choose_features(all_features_dict, threshold_frequency) + ['is_qlink']]

    train = sekitei.dataframe.drop(['is_qlink'], axis=1).values.astype(float)
    number_of_features = train.shape[1]
    cluster_factor = 0.1
    number_of_clusters = int(cluster_factor * number_of_features)
    sekitei.kmeans = KMeans(n_clusters=number_of_clusters).fit(train)
    #sekitei.classifier = LogisticRegression().fit(train, sekitei.dataframe['is_qlink'])
    sekitei.dataframe['label'] = sekitei.kmeans.labels_
    sekitei.features = numpy.array(
        sekitei.dataframe.drop(['is_qlink', 'label'], axis=1).columns)
    
    #print sekitei.features
    grouped = sekitei.dataframe[['label', 'is_qlink']].groupby(
        'label')
    sekitei.quota_rates = grouped.mean()['is_qlink']
    sekitei.quota_parts = sekitei.quota_rates * QUOTA
    # cluster_sizes = grouped.count()['is_qlink']
    cluster_qlinks = grouped.sum()['is_qlink']
    # if (sekitei.quota_parts < 0.1*size)
    #if (cluster_qlinks > 0.15 * size).any():
        #print cluster_qlinks
        #MIN_QUOTA *= 2
    sekitei.quota_parts = max_series(sekitei.quota_parts, Series(
        data=MIN_QUOTA, index=numpy.arange(len(sekitei.quota_parts)))).to_dict()
    keys = set(numpy.arange(number_of_clusters)) - set(sekitei.quota_rates.keys())
    addition = defaultdict.fromkeys(keys, MIN_QUOTA)
    sekitei.quota_parts = merge_two_dicts(sekitei.quota_parts, addition)
    #addition =  defaultdict.fromkeys(keys, float(MIN_QUOTA)/QUOTA)
    #sekitei.quota_rates = merge_two_dicts(sekitei.quota_rates.to_dict(), addition)
def isin(element, test_elements, assume_unique=False, invert=False):
    "..."
    element = numpy.asarray(element)
    return numpy.in1d(element, test_elements, assume_unique=assume_unique,
                      invert=invert).reshape(element.shape)

def decision(probability):
    return random.random() < probability

def fetch_url(url):
    # return sekitei.fetch_url(url);
    current_url_features = url_to_features_list(url)
    current_url_row = isin(sekitei.features, current_url_features).reshape(1, -1).astype(float)
    current_url_label = sekitei.kmeans.predict(
        current_url_row)[0]
    if sekitei.quota_parts[current_url_label] > 0:
        #if not sekitei.classifier.predict(current_url_row)[0]:
            #probability = sekitei.quota_rates[current_url_label] * 0.5
            #if decision(probability):
                #return True
        sekitei.quota_parts[current_url_label] -= 1
        return True
    else:
        return False
