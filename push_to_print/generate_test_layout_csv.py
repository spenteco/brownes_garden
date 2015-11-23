#!/usr/bin/python

import sys, sqlite3, re, codecs, json
from image_list import *
from mako.template import Template

quotes_conn = sqlite3.connect('../../db/quotes.sqlite3')
poem_conn = sqlite3.connect('../../db/poems.sqlite3')
other_poem_conn = sqlite3.connect('../../db/other_poems.sqlite3')

bad_pages = []
lines = codecs.open('bad_pages.csv', 'r', encoding='utf-8').read().split('\n')
for line in lines:
    if line.strip() > '':
        bad_pages.append(line.strip().split('|'))

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

print 'verso type' + '|' + 'verso key_1' + '|' + 'verso_key_2' + '|' + 'recto type' + '|' + 'recto key_1' + '|' + 'recto key_2'

if sys.argv[1] == 'images':
    
    n = 0
    line = []
    for image in image_list:
        if image[0][:-1] == sys.argv[2]:
            n = n + 1
            line.append(image[0][:-1])
            line.append(image[1].replace('.svg', '.jpg'))
            line.append('')
            if n % 2 == 0:
                print '|'.join(line)
                line = []
                
    if len(line) > 0:
        print '|'.join(line + ['', '', ''])

if sys.argv[1] == 'poems':
    
    c = poem_conn.cursor()
    c.execute('SELECT poem_type, start_time, poem_number FROM poems WHERE poem_type = ? ORDER BY 1, 2, 3;', (sys.argv[2],))
        
    results = c.fetchall()
    
    n = 0
    line = []
    for row in results:
        n = n + 1
        line.append(row[0])
        line.append(row[1])
        line.append(str(row[2]))
        if n % 2 == 0:
            print '|'.join(line)
            line = []
                
    if len(line) > 0:
        print '|'.join(line + ['', '', ''])

if sys.argv[1] == 'other_poems':
    
    c = other_poem_conn.cursor()
    c.execute('SELECT poem_type, start_time, poem_number FROM poems WHERE poem_type = ? ORDER BY 1, 2, 3;', (sys.argv[2],))
        
    results = c.fetchall()
    
    n = 0
    line = []
    for row in results:
        n = n + 1
        line.append(row[0])
        line.append(row[1])
        line.append(str(row[2]))
        if n % 2 == 0:
            print '|'.join(line)
            line = []
        
    if len(line) > 0:
        print '|'.join(line + ['', '', ''])
        
if sys.argv[1] == 'quotes':
    
    c = quotes_conn.cursor()
    c.execute('SELECT DISTINCT cyrus_sentence_n FROM quotes ORDER BY 1;')
        
    results = c.fetchall()
    
    n = 0
    line = []
    for row in results:
        
        is_bad = False
        for b in bad_pages:
            if b[0] == 'quote' and int(b[1]) == row[0]:
                is_bad = True
                
        if is_bad == False:
                    
            n = n + 1
            line.append('quote')
            line.append(str(row[0]))
            line.append('')
            if n % 2 == 0:
                print '|'.join(line)
                line = []
                
    if len(line) > 0:
        print '|'.join(line + ['', '', ''])

if sys.argv[1] == 'static':
    
    r = ['blank', '', '', 'title_page', '', '']
    print '|'.join(r)
    
    r = ['publication_information', '', '', 'frontispiece', '', '']
    print '|'.join(r)
    
    r = ['concluding_page', '', '', 'blank', '', '']
    print '|'.join(r)
    
    r = ['bibliography', '', '', '', '', '']
    print '|'.join(r)
    
