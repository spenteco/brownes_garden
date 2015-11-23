#!/usr/bin/python

import os, sys
from src.textual_source import *
from src.collection_of_sources import *

input_folder = sys.argv[1]
output_folder = sys.argv[2]

#   THIS INCLUDES THE PARSE TREE
#STANFORD_PARAMETERS = '-annotators tokenize,ssplit,pos,lemma,parse' 
#   THIS INCLUDES JUST THE DEPENDENCIES.  IT TAKES 1/3 OF THE TIME NEEDED TO GET THE PARSE TREE.
STANFORD_PARAMETERS = '-annotators tokenize,ssplit,pos,lemma,depparse' 
    
PATH_TO_STANFORD_CORENLP = '/home/steve/1/eMcKuen5/stanford-corenlp-full-2015-04-20/'    

processed_files = os.listdir(output_folder)

for file_name in os.listdir(input_folder):
    
    if file_name.replace('.txt', '_txt.xml') in processed_files:
        print 'BYPASSING', file_name
    else:
        print 'Processing', file_name

        c = CollectionOfSources([input_folder + file_name,], output_folder, STANFORD_PARAMETERS, PATH_TO_STANFORD_CORENLP)
