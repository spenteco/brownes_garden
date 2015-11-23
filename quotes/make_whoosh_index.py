#!/usr/bin/python

import sys, os
from lxml import etree
from whoosh.index import create_in
from whoosh.fields import *

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

input_folder = sys.argv[1]

schema = Schema(sentence_key=ID(stored=True), content=TEXT(stored=True), lemmas=TEXT(stored=True))
ix = create_in(sys.argv[2], schema)
writer = ix.writer()

for xml_file_name in os.listdir(input_folder):
    
    if xml_file_name.find('garden_of_cyrus') == -1:

        tree = etree.parse(input_folder + xml_file_name)
                
        sentences = tree.xpath('//sentence')
        
        print 'processing', xml_file_name, 'len(sentences)', len(sentences)
        
        for sentence in sentences:
        
            sentence_n = sentence.get('n')
        
            sentence_text = unicode(sentence.xpath('descendant::text')[0].text)
            
            sentence_key = unicode(xml_file_name + '|' + sentence_n)
            
            lemmas = []
            tokens = sentence.xpath('descendant::token')
            for token in tokens:
                lemmas.append(token.get('lemma'))
            lemmas_text = unicode(' '.join(lemmas))

            writer.add_document(sentence_key=sentence_key, content=sentence_text, lemmas=lemmas_text)
            
writer.commit()
