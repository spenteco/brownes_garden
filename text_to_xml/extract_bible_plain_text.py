#!/usr/bin/python

import re, codecs, sqlite3, random, sys
from lxml import etree

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

tree = etree.parse(sys.argv[1])

books = tree.xpath('//BIBLEBOOK')

for b in books:
    
    text = []
    
    verses = b.xpath('descendant::VERS')
    
    for v in verses:
        
        text.append(v.text)
        
    f = codecs.open(sys.argv[1] + b.get('bsname') + '.txt', 'w', encoding='utf-8')
    f.write('\n'.join(text) + '\n')
    f.close()
