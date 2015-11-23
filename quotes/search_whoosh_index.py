#!/usr/bin/python

import sys, os, re, json
from lxml import etree
from all_good_words import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

ix = open_dir(sys.argv[1])

tree = etree.parse(sys.argv[2])
                
sentences = tree.xpath('//sentence')

for sentence in sentences:
        
    sentence_n = sentence.get('n')

    sentence_text = unicode(sentence.xpath('descendant::text')[0].text)
    
    tokens = sentence.xpath('descendant::token')
    
    lemmas = []
    
    for token in tokens:
        
        if token.get('lemma').lower() in all_good_words:
            try:
                noop = int(token.get('lemma').lower())
            except:
                lemmas.append(token.get('lemma').lower())
      
    lemmas = sorted(list(set(lemmas)))
    
    if len(sentence_text.strip()) >= 50 and len(sentence_text.strip()) <= 300 and len(lemmas) > 1:
        print
        print len(lemmas), len(sentence_text.strip()), sentence_text.strip(), lemmas

    if len(lemmas) == 0:
        
        print
        print  json.dumps([sentence_n, sentence_text.strip(), None])

    else:

        query = unicode(' OR '.join(lemmas))
        qp = QueryParser('lemmas', schema=ix.schema)
        q = qp.parse(query)

        with ix.searcher() as s:
            
            results = s.search(q, limit=30, terms=True)
            
            for r in results:
                
                matched_lemmas = []
                for t in r.matched_terms():
                    matched_lemmas.append(t[1])
                    
                matched_lemmas.sort()

                print
                print json.dumps([sentence_n, sentence_text.strip(), matched_lemmas, r['sentence_key'].split('|')[0], r['sentence_key'].split('|')[1], r['content']])
