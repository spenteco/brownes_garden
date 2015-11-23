#!/usr/bin/python

import sys, sqlite3, re, codecs, json, random, os
from image_list import *
from mako.template import Template

quotes_conn = sqlite3.connect('../../db/quotes.sqlite3')
poem_conn = sqlite3.connect('../../db/poems.sqlite3')
other_poem_conn = sqlite3.connect('../../db/other_poems.sqlite3')

images = []
for file_name in os.listdir('test_print/svg/one_square/'):
    images.append(['one_square', file_name])
for file_name in os.listdir('test_print/svg/four_square/'):
    images.append(['four_square', file_name])
random.shuffle(images)

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------
    
c = other_poem_conn.cursor()
c.execute('SELECT DISTINCT poem_type, start_time, poem_number FROM poems')
all_other_poems = c.fetchall()

c = poem_conn.cursor()
c.execute('SELECT DISTINCT poem_type, start_time, poem_number FROM poems;')
all_poems = c.fetchall()
random.shuffle(all_poems)

selected_quote_sentences = []
    
c = quotes_conn.cursor()
c.execute('SELECT DISTINCT cyrus_sentence_n FROM quotes WHERE cyrus_sentence_n NOT IN (131, 242) ORDER BY 1;')
    
results = c.fetchall()
for r in results:
    
    matching_other_poems = []
    
    for a in all_other_poems:
        if len(a[2].split('_')) == 3:
            if str(r[0]) == a[2].split('_')[0] or str(r[0]) == a[2].split('_')[0]:
                matching_other_poems.append(a)
                if a[0] == 'keep_sequence_10_8_10_8_10_8_10_8_10' or a[0] == 'keep_sequence_5_4_5_4_5':
                    matching_other_poems.append(a)
        else:
            if str(r[0]) == a[2].split('_')[0]:
                matching_other_poems.append(a)
                if a[0] == 'keep_sequence_10_8_10_8_10_8_10_8_10' or a[0] == 'keep_sequence_5_4_5_4_5':
                    matching_other_poems.append(a)
    
    selected_quote_sentences.append([r[0], matching_other_poems])
    
random.shuffle(selected_quote_sentences)
selected_quote_sentences = selected_quote_sentences[:75]
selected_quote_sentences.sort()

print 'verso type' + '|' + 'verso key_1' + '|' + 'verso_key_2' + '|' + 'recto type' + '|' + 'recto key_1' + '|' + 'recto key_2'

print 'blank|||title_page||'
print 'publication_information|||frontispiece||'

heading_image_lines = ['aviation|LEFT_foundry.churchill_aviation.jpg||aviation|RIGHT_foundry.churchill_aviation.jpg|', 'aviation|LEFT_bunker_hill.churchill_aviation.jpg||aviation|RIGHT_bunker_hill.churchill_aviation.jpg|', 'aviation|LEFT_armstrong.flowers_aviation.jpg||aviation|RIGHT_armstrong.flowers_aviation.jpg|', 'aviation|LEFT_locomotive.jefferson_aviation.jpg||aviation|RIGHT_locomotive.jefferson_aviation.jpg|', 'aviation|LEFT_funeral.jefferson_aviation.jpg||aviation|RIGHT_funeral.jefferson_aviation.jpg|']

selected_quote_sentences_index = -1

possible_types = ['diamond', 'X', 'quincunx', 'lattice', 'ascii_diamond', 'ascii_x', 'letter_ngrams', 'keep_sequence_10_8_10_8_10_8_10_8_10', 'keep_sequence_5_4_5_4_5', 'keep_sequence_10_8_10_8_10_8_10_8_10', 'keep_sequence_5_4_5_4_5']

for section in range(0, 5):
    
    print heading_image_lines[section]
    
    for opening in range(0, 23):
        
        opening_pages = []
        
        if opening in [3, 4, 8, 9, 13, 14, 18, 19]:
            
            img = images[0]
            del images[0]
            poem = all_poems[0]
            del all_poems[0]
            
            opening_pages = [poem[0] + '|' + poem[1] + '|' + str(poem[2]), '|'.join(img) + '|']
        
        else:
            
            selected_quote_sentences_index += 1
            
            paired_page = random.choice(selected_quote_sentences[selected_quote_sentences_index][1])
            
            opening_pages = ['quote|' + str(selected_quote_sentences[selected_quote_sentences_index][0]) + '|', '|'.join(paired_page)]
        
        random.shuffle(opening_pages)
        
        print '|'.join(opening_pages)

print 'concluding_page|||aviation|RIGHT_grissom.flowers_aviation.jpg|'
print 'bibliography|||||'

