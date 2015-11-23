#!/usr/bin/python

import sys, os, copy, time, json, codecs, random
import sqlite3

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()

lines = codecs.open(sys.argv[2], 'r', encoding='utf-8').read().split('\n')

indexes = []
for i, a in enumerate(lines):
    if a.strip() > '':
        indexes.append(i)

#random.shuffle(indexes)

#for i in indexes[:500]:
for i in indexes:
    
    line = lines[i]
    
    if line.strip() > '':
        
        row = line.strip().split('|')
        
        start_time = row[0]
        poem_number = row[1]
        poem_type = row[2]
        poem_json = row[3]
        source_files = row[4]
        is_good = 0

        c.execute('INSERT INTO poems VALUES (?, ?, ?, ?, ?, ?)', (start_time, poem_number, poem_type, poem_json, source_files, is_good, ))

conn.commit()
