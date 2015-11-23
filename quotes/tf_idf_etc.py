#!/usr/bin/python

import sys, os, copy, time, json
from lxml import etree
from nltk.corpus import stopwords

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

def get_lemma_count(path_to_file):
    
    print 'loading', path_to_file

    lemma_count = {}

    tree = etree.parse(path_to_file)
    tokens = tree.xpath('//token')
    
    for t in tokens:
        l = t.get('lemma').lower()
        if l not in stopwords.words('english'):
            try:
                lemma_count[l] += 1
            except KeyError:
                lemma_count[l] = 1
                
    return lemma_count
    
#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

df = {}

cyrus_lemma_count = get_lemma_count(sys.argv[1] + 'PG_the_garden_of_cyrus_txt.xml')

for lemma, count in cyrus_lemma_count.iteritems():
    try:
        df[lemma] += 1
    except KeyError:
        df[lemma] = 1
    
for xml_file_name in os.listdir(sys.argv[1]):
        
    if xml_file_name.find('PG_the_garden_of_cyrus') == -1:

        other_lemma_count = get_lemma_count(sys.argv[1] + xml_file_name)

        for lemma, count in other_lemma_count.iteritems():
            try:
                df[lemma] += 1
            except KeyError:
                pass
                
for lemma, count in cyrus_lemma_count.iteritems():

    print lemma + '|' + str(count) + '|' + str(df[lemma])
        
    
    
