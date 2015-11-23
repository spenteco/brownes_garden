#!/usr/bin/python

import sys, codecs

all_good_words = {}

lines = codecs.open(sys.argv[1], 'r', encoding='utf-8').read().split()

for line in lines:
    
    if len(line.strip().split('|')) == 3:
        
        cols = line.strip().split('|')
        
        if len(cols[0]) > 1 and int(cols[2]) > 1 and cols[0] != 'chapter' and cols[0].startswith('-') == False:
            
            all_good_words[cols[0]] = 1
            
print 'all_good_words = ' + str(all_good_words)
