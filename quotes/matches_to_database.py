#!/usr/bin/python

import sys, os, copy, time, json, codecs
import sqlite3

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

conn = sqlite3.connect(sys.argv[2])
c = conn.cursor()

lines = codecs.open(sys.argv[1], 'r', encoding='utf-8').read().split('\n')

sentences_printed = []

for line in lines:
    
    if line.startswith('['):
        
        print line
        
        row = json.loads(line)
        
        if len(row) == 6:

            cyrus_sentence_n = int(row[0])
            cyrus_sentence = row[1]
            match_lemmas = json.dumps(row[2])
            other_file_name = row[3]
            other_sentence_n = int(row[4])
            other_sentence = row[5]

            c.execute('INSERT INTO quotes VALUES (?, ?, ?, ?, ?, ?, ?)', (cyrus_sentence_n, cyrus_sentence, match_lemmas, other_file_name, other_sentence_n, other_sentence, 0))

conn.commit()
