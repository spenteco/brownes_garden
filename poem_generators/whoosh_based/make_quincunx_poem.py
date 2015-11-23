#!/usr/bin/python

import sys, codecs, random, copy, time, json
from common_routines import *
from lxml import etree
        

def create_poem_template(POEM_WIDTH, POEM_HEIGHT):

    poem = []

    for x in range(0, POEM_WIDTH):
        row = []
        for y in range(0, POEM_HEIGHT):
            if y % 2 == 0:
                if x % 2 == 0:
                    row.append('#')
                else:
                    row.append(' ')
            else:
                if x % 2 == 0:
                    row.append(' ')
                else:
                    row.append('#')
        
        poem.append(row)

    return poem


def get_creation_order(POEM_WIDTH, POEM_HEIGHT):

    up_starting_points = []
        
    #   UP
        
    for z in range(1, POEM_HEIGHT - 1):
        if z % 4 == 0:
            x = 0
            y = z
            positions = []
            while True:
                positions.append((x, y))
                x += 1
                y -= 1
                if x > POEM_WIDTH - 1 or y < 0:
                    break
            up_starting_points.append((0, z, len(positions)))
        
    for z in range(0, POEM_WIDTH - 1):
        if z % 4 == 0:
            x = z
            y = POEM_HEIGHT - 1
            positions = []
            while True:
                positions.append((x, y))
                x += 1
                y -= 1
                if x > POEM_WIDTH - 1 or y < 0:
                    break
            up_starting_points.append((z, POEM_HEIGHT - 1, len(positions)))
        
    #   DOWN

    down_starting_points = []
        
    for z in range(0, POEM_HEIGHT - 1):
        if z % 4 == 0:
            x = 0
            y = z
            positions = []
            while True:
                positions.append((x, y))
                x += 1
                y += 1
                if x > POEM_WIDTH - 1 or y > POEM_HEIGHT - 1:
                    break
            down_starting_points.append((0, z, len(positions)))
        
    for z in range(1, POEM_WIDTH - 1):
        if z % 4 == 0:
            x = z
            y = 0
            positions = []
            while True:
                positions.append((x, y))
                x += 1
                y += 1
                if x > POEM_WIDTH - 1 or y > POEM_HEIGHT - 1:
                    break
            down_starting_points.append((z, 0, len(positions)))
            
    ngram_sizes_required = []

    for p in up_starting_points:
        ngram_sizes_required.append(p[2])  
    for p in down_starting_points:
        ngram_sizes_required.append(p[2])  

    ngram_sizes_required = list(set(ngram_sizes_required))

    return ngram_sizes_required, up_starting_points, down_starting_points


def actually_fill_poem(poem, ngram, positions, n, reverse_ngrams):

    for a in range(0, len(positions)):
        p = positions[a]
        poem[p[0]][p[1]] = ngram[a]


def fill_poem_with_ngrams(poem, starting_ngrams, working_starting_indexes, ngrams, up_starting_points, down_starting_points, whoosh_index):

    #print 'starting_ngrams', starting_ngrams, 'working_starting_indexes', working_starting_indexes, 'up_starting_points', up_starting_points, 'down_starting_points', down_starting_points

    poem_sources = []

    for s in up_starting_points:

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
            
        #print 'positions', positions
            
        poem_sources.append(starting_ngrams[n][working_starting_indexes[n]][1])

        actually_fill_poem(poem, starting_ngrams[n][working_starting_indexes[n]][0], positions, n, False)

        working_starting_indexes[n] += 1

    for s in down_starting_points:
        
        #print 's', s
        
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

        regex_matches = []
        
        for p in positions:
            if poem[p[0]][p[1]] == '#':
                regex_matches.append('\w+')
            else:
                regex_matches.append(poem[p[0]][p[1]].strip())

        #regex_match_string = ' '.join(regex_matches)
        
        regex_match_slices = []
        one_slice = []
        for r in regex_matches:
            if r != '\\w+':
                one_slice.append(r)
                if len(one_slice) > 1:
                    regex_match_slices.append(one_slice)
                    one_slice = []
            else:
                one_slice.append(r)
        
        if len(one_slice) > 0:
            regex_match_slices.append(one_slice)

        #print 'positions', positions, 'regex_matches', regex_matches, 'regex_match_slices', regex_match_slices

        position_index = -1
        for one_slice in regex_match_slices:

            regex_match_string = ' '.join(one_slice)

            these_positions = []
            for a in one_slice:
                position_index += 1
                these_positions.append(positions[position_index])

            words_to_lookup = []
            for a in one_slice:
                if a != '\\w+':
                    words_to_lookup.append(a)

            #print 'regex_match_string', regex_match_string, 'words_to_lookup', words_to_lookup

            possible_ngrams = search_whoosh_index(whoosh_index, regex_match_string, words_to_lookup)

            #print 'possible_ngrams', possible_ngrams

            if len(possible_ngrams) > 0:
            
                selected_ngram = random.choice(possible_ngrams)
                poem_sources.append(selected_ngram[1])
            
                actually_fill_poem(poem, selected_ngram[0], these_positions, n, False)
            
    return poem_sources


def fill_remaining_places_in_poem(poem, starting_ngrams, working_starting_indexes, ngrams, up_starting_points, down_starting_points, whoosh_index, after_markov_chain, before_markov_chain):
    
    poem_sources = []

    for x in range(0, POEM_WIDTH):
        for y in range(0, POEM_HEIGHT):
            if poem[x][y] == '#':

                before_words = []
                after_words = []

                for x_diff in (-1, 1):
                    for y_diff in (-1, 1):

                        if x + x_diff >= 0 and x + x_diff < POEM_WIDTH and y + y_diff >= 0 and y + y_diff < POEM_HEIGHT:

                            if poem[x + x_diff][y + y_diff] != '#':
                                if x == -1:
                                    before_words.append(poem[x + x_diff][y + y_diff])
                                else:
                                    after_words.append(poem[x + x_diff][y + y_diff])

                #print 'x', x, 'y', y, 'before_words', before_words, 'after_words', after_words

                word = None
                if len(before_words) == 0 and len(after_words) == 0:
                    word = random.choice(after_markov_chain.keys())
                else:
                    if len(before_words) > 0 and len(after_words) == 0:

                        possible_words = []

                        for b in before_words:
                            try:
                                for w in before_markov_chain[b]:
                                    possible_words.append(w)
                            except KeyError:
                                pass

                        if len(possible_words) == 0:
                            pass
                        else:
                            word = random.choice(possible_words)

                    else:
                        if len(before_words) == 0 and len(after_words) > 0:

                            possible_words = []

                            for b in after_words:
                                try:
                                    for w in after_markov_chain[b]:
                                        possible_words.append(w)
                                except KeyError:
                                    pass

                            if len(possible_words) == 0:
                                pass
                            else:
                                word = random.choice(possible_words)

                        else:

                            possible_words = []

                            for b in before_words:
                                try:
                                    for w in before_markov_chain[b]:
                                        possible_words.append(w)
                                except KeyError:
                                    pass

                            for b in after_words:
                                try:
                                    for w in after_markov_chain[b]:
                                        possible_words.append(w)
                                except KeyError:
                                    pass

                            if len(possible_words) == 0:
                                pass
                            else:
                                word = random.choice(possible_words)

                if word != None:
                    poem[x][y] = word
                    #print 'PICKED', word


if __name__ == "__main__":
    
    QUOTE_DB_FILE = sys.argv[1]
    WHOOSH_FOLDER = sys.argv[2]
    POEM_WIDTH = int(sys.argv[3])           
    POEM_HEIGHT = int(sys.argv[4])            
    ITERATIONS = int(sys.argv[5]) 
    OUTPUT_FILE_NAME = sys.argv[6]

    #if POEM_WIDTH != POEM_HEIGHT:
    #    print 'POEM_WIDTH != POEM_HEIGHT -- exiting'
    #    exit()

    whoosh_index = open_whoosh_index(WHOOSH_FOLDER)
    output_file = codecs.open(OUTPUT_FILE_NAME, 'w', encoding='utf-8')

    start_time = time.time()
    
    n_poems_created = 0
    all_poems_created = []

    poem_template = create_poem_template(POEM_WIDTH, POEM_HEIGHT)

    print_poem(poem_template)

    ngram_sizes_required, up_starting_points, down_starting_points = get_creation_order(POEM_WIDTH, POEM_HEIGHT)
    
    number_of_ngrams_required_by_size = {}
    for p in up_starting_points:
        try:
            number_of_ngrams_required_by_size[p[2]] += 1
        except KeyError:
            number_of_ngrams_required_by_size[p[2]] = 1

    print 'ngram_sizes_required', ngram_sizes_required, 'number_of_ngrams_required_by_size', number_of_ngrams_required_by_size
    print 'up_starting_points', up_starting_points, 'down_starting_points', down_starting_points

    up_markov_chain, down_markov_chain, ngrams = load_text(QUOTE_DB_FILE, ngram_sizes_required, False)

    #for k, v in ngrams.iteritems():
    #    print k, 'len(ngrams[k])', len(ngrams[k])
    
    for i in range(0, ITERATIONS):
        
        #print 'i', i
                        
        for n in ngrams.keys():
            random.shuffle(ngrams[n])
            
        ngram_indexes = {}
        working_starting_indexes = {}
        for n in number_of_ngrams_required_by_size.keys():
            ngram_indexes[n] = 0
            working_starting_indexes[n] = 0
        
        loop_counter = 0
        keep_looping = True
        while keep_looping == True:

            #loop_counter += 1
            #if loop_counter > 25:
            #    keep_looping = False
            #    break
            
            #print 'ngram_indexes', ngram_indexes, 'number_of_ngrams_required_by_size', number_of_ngrams_required_by_size
            
            for n in ngram_indexes.keys():
                if ngram_indexes[n] + number_of_ngrams_required_by_size[n] > len(ngrams[n]) - number_of_ngrams_required_by_size[n]:
                    keep_looping = False
                    break
                    
            #for n in ngram_indexes.keys():
            #    print 'n', n, 'ngram_indexes[n]', ngram_indexes[n], 'number_of_ngrams_required_by_size[n]', number_of_ngrams_required_by_size[n]
            #    noop = ngrams[n][ngram_indexes[n] + number_of_ngrams_required_by_size[n]]
        
            starting_ngrams = {}
        
            for n in ngram_sizes_required:
                for a in range(0, number_of_ngrams_required_by_size[n]):
                    try:
                        starting_ngrams[n].append(ngrams[n][ngram_indexes[n] + a])
                    except KeyError:
                        starting_ngrams[n] = [ngrams[n][ngram_indexes[n] + a]]
            
            #print 'starting_ngrams', starting_ngrams
                
            #starting_ngrams = [ngrams[ngram_sizes_required[0]][a], ngrams[ngram_sizes_required[0]][a + 1]]
            #a += 2
            
            for n in ngram_indexes.keys():
                ngram_indexes[n] += number_of_ngrams_required_by_size[n]
                
            #continue
        
            temp_poem_template = copy.deepcopy(poem_template)

            poem_sources = fill_poem_with_ngrams(temp_poem_template, starting_ngrams, copy.deepcopy(working_starting_indexes), ngrams, up_starting_points, down_starting_points, whoosh_index)

            #print_poem(temp_poem_template)

            fill_remaining_places_in_poem(temp_poem_template, starting_ngrams, copy.deepcopy(working_starting_indexes), ngrams, up_starting_points, down_starting_points, whoosh_index, up_markov_chain, down_markov_chain)
            
            if is_poem_fixable(temp_poem_template, 3) == True and temp_poem_template not in all_poems_created:

                print_poem(temp_poem_template)
                print 'poem_sources', poem_sources

                write_poem_to_database(start_time, n_poems_created, 'quincunx', POEM_WIDTH, POEM_HEIGHT,  temp_poem_template, poem_sources, output_file)
            
                n_poems_created += 1
                all_poems_created.append(temp_poem_template)

    output_file.close()
                
    print 'n_poems_created', n_poems_created, 'time', (time.time() - start_time)
