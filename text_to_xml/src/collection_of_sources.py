#!/usr/bin/python

import re, math, json, copy, time
from collections import defaultdict
from textual_source import *
from lxml import etree
from utility_functions import *

class CollectionOfSources:
    
    def __init__(self, source_locations, pickle_location, STANFORD_PARAMETERS, PATH_TO_STANFORD_CORENLP):

        self.sources = []
        self.pickle_location = pickle_location
        
        #   LOAD THE SOURCES
        
        for source_location in source_locations:
            self.sources.append(TextualSource(source_location, pickle_location, STANFORD_PARAMETERS, PATH_TO_STANFORD_CORENLP))
