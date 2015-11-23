#!/usr/bin/python

import codecs, urllib, re, time, json
from lxml import etree
from bs4 import BeautifulSoup
from utility_functions import *

class TextualSource:
    
    def __init__(self, source_location, pickle_location, STANFORD_PARAMETERS, PATH_TO_STANFORD_CORENLP):
        
        self.data = {}
        
        self.data['source_location'] = source_location
        self.data['pickle_location'] = pickle_location
        self.data['pickle_file_name'] = ''
        
        if self.data['source_location'].find(self.data['pickle_location']) > -1:
            
            #   LOAD PREVIOUSLY SERIALIZED XML
            
            self.data['pickle_file_name'] = self.data['source_location']
            
            self.data['tree'] = etree.parse(self.data['pickle_file_name'])
            
        else:
            
            #   LOAD RAW TEXT
            
            self.data['raw_text'] = ''
            self.data['pickle_file_name'] = self.data['pickle_location'] + derive_pickle_file_name(self.data['source_location'])
            
            if self.data['source_location'].startswith('http') == True:
                
                html = urllib.urlopen(self.data['source_location']).read()
                soup = BeautifulSoup(html, 'html.parser')
                
                self.data['raw_text'] = re.sub('\s', ' ', soup.get_text().replace('\r', ' ').replace('\n', ' '))
                
            else:
                self.data['raw_text'] = re.sub('\s', ' ', codecs.open(self.data['source_location'], 'r', encoding='utf-8').read().replace('\r', ' ').replace('\n', ' '))
                
            #   PARSE
            
            stanford_parser = start_stanford_parser(STANFORD_PARAMETERS, PATH_TO_STANFORD_CORENLP)
            
            result = stanford_parse_text(stanford_parser, self.data['raw_text'])
            
            #   SAVE FOR RE-USE
                
            f = codecs.open(self.data['pickle_file_name'], 'w', encoding='utf-8')
            f.write(result)
            f.close()
            
            #   LOAD THE SAVED FILE AS A TREE
            
            self.data['tree'] = etree.parse(self.data['pickle_file_name'])
