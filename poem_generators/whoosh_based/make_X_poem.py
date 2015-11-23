#!/usr/bin/python

import sys, codecs, random, copy, time, json
from common_routines import *
from lxml import etree


def create_poem_template(POEM_WIDTH, POEM_HEIGHT):

    poem = []

    for x in range(0, POEM_WIDTH):
        row = []
        for y in range(0, POEM_HEIGHT):
            row.append(' ')
        poem.append(row)
    
    x = 0
    y = 0
    
    for a in range(0, POEM_WIDTH):
        poem[x + a][y + a] = '#'
    
    x = 0
    y = POEM_HEIGHT - 1
    
    for a in range(0, POEM_WIDTH):
        poem[x + a][y - a] = '#'

    return poem


def get_creation_order(POEM_WIDTH, POEM_HEIGHT):
    
    angle_length = POEM_WIDTH

    up_starting_points = [(0, POEM_HEIGHT - 1, angle_length)]

    down_starting_points = [(0, 0, angle_length)]

    return [angle_length], up_starting_points, down_starting_points


def actually_fill_poem(poem, ngram, positions, n, reverse_ngrams):

    for a in range(0, len(positions)):
        p = positions[a]
        poem[p[0]][p[1]] = ngram[a]


def fill_poem_with_ngrams(poem, first_ngram, ngrams, up_starting_points, down_starting_points, whoosh_index):
    
    poem_sources = []

    for i, s in enumerate(up_starting_points):

        starting_x = s[0]
        starting_y = s[1]
        n = s[2]

        positions = []

        x = starting_x
        y = starting_y
        for a in range(0, n):
            positions.append((x, y))
            x = x + 1
            y = y - 1
            
        poem_sources.append(first_ngram[1])

        actually_fill_poem(poem, first_ngram[0], positions, n, False)

    for s in down_starting_points:

        starting_x = s[0]
        starting_y = s[1]
        n = s[2]

        positions = []

        x = starting_x
        y = starting_y
        for a in range(0, n):
            positions.append((x, y))
            x = x + 1
            y = y + 1

        regex_match_string = []
        words_to_lookup = []
        
        for p in positions:
            if poem[p[0]][p[1]] == '#':
                regex_match_string.append('\w+')
            else:
                regex_match_string.append(poem[p[0]][p[1]].strip())
                words_to_lookup.append(poem[p[0]][p[1]].strip())

        regex_match_string = ' '.join(regex_match_string)

        #print 'regex_match_string', regex_match_string, 'words_to_lookup', words_to_lookup

        possible_ngrams = search_whoosh_index(whoosh_index, regex_match_string, words_to_lookup)

        #print 'possible_ngrams', possible_ngrams

        if len(possible_ngrams) > 0:
            
            selected_ngram = random.choice(possible_ngrams)
            poem_sources.append(selected_ngram[1])
            
            actually_fill_poem(poem, selected_ngram[0], positions, n, False)
            
    return poem_sources


if __name__ == "__main__":
    
    QUOTE_DB_FILE = sys.argv[1]
    WHOOSH_FOLDER = sys.argv[2]
    POEM_WIDTH = int(sys.argv[3])           
    POEM_HEIGHT = int(sys.argv[4])            
    ITERATIONS = int(sys.argv[5]) 
    OUTPUT_FILE_NAME = sys.argv[6]

    if POEM_WIDTH != POEM_HEIGHT:
        print 'POEM_WIDTH != POEM_HEIGHT -- exiting'
        exit()

    whoosh_index = open_whoosh_index(WHOOSH_FOLDER)
    output_file = codecs.open(OUTPUT_FILE_NAME, 'w', encoding='utf-8')

    start_time = time.time()
    
    n_poems_created = 0
    all_poems_created = []

    poem_template = create_poem_template(POEM_WIDTH, POEM_HEIGHT)

    print_poem(poem_template)

    ngram_sizes_required, up_starting_points, down_starting_points = get_creation_order(POEM_WIDTH, POEM_HEIGHT)

    print 'up_starting_points', up_starting_points, 'down_starting_points', down_starting_points

    up_markov_chain, down_markov_chain, ngrams = load_text(QUOTE_DB_FILE, ngram_sizes_required, True)

    #for ngrams_len, ngrams in ngrams.iteritems():
    #    for n in ngrams:
    #        print ngrams_len, n
    
    for i in range(0, ITERATIONS):
                        
        for n in ngrams.keys():
            random.shuffle(ngrams[n])
        
        first_up = up_starting_points[0]
        for n_gram in ngrams[first_up[2]]:
        
            temp_poem_template = copy.deepcopy(poem_template)

            poem_sources = fill_poem_with_ngrams(temp_poem_template, n_gram, ngrams, up_starting_points, down_starting_points, whoosh_index)

            #print_poem(temp_poem_template)
            
            if is_poem_valid(temp_poem_template) == True and temp_poem_template not in all_poems_created:

                print_poem(temp_poem_template)
                print 'poem_sources', poem_sources

                write_poem_to_database(start_time, n_poems_created, 'X', POEM_WIDTH, POEM_HEIGHT,  temp_poem_template, poem_sources, output_file)
            
                n_poems_created += 1
                all_poems_created.append(temp_poem_template)

    output_file.close()
                
    print 'n_poems_created', n_poems_created, 'time', (time.time() - start_time)
