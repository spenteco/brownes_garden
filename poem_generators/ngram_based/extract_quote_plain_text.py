#!/usr/bin/python

import sys, sqlite3, re

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

selected_sentence_n = sys.argv[2].split(',')

for n in selected_sentence_n:

    quotes_conn = sqlite3.connect(sys.argv[1])
    c = quotes_conn.cursor()

    c.execute('SELECT DISTINCT other_sentence FROM quotes WHERE cyrus_sentence_n = ?;', (n,))

    sentences = c.fetchall()

    for row in sentences:
        
        sentence = re.sub('\s+', ' ', row[0]).strip().replace('<i>', ' ').replace('</i>', ' ').replace('<br/>', ' ')
        
        print sentence

    c.execute('SELECT DISTINCT cyrus_sentence FROM quotes WHERE cyrus_sentence_n = ?;', (n,))

    sentences = c.fetchall()

    for row in sentences:
        
        sentence = re.sub('\s+', ' ', row[0]).strip().replace('<i>', '').replace('</i>', '').replace('<br/>', '')
        
        print sentence
