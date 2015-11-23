#!/usr/bin/python

import sys, sqlite3, re, random, copy, time, json
from nltk.corpus import cmudict
from textblob import TextBlob

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

def extract_sentences_from_db(database_file, cyrus_sentence_numbers):

    quotes_conn = sqlite3.connect(sys.argv[1])
    c = quotes_conn.cursor()

    result_sentences = []
    result_sources = []
    
    for n in cyrus_sentence_numbers:

        c.execute('SELECT other_sentence, other_file_name FROM quotes WHERE cyrus_sentence_n = ?;', (n,))

        sentences = c.fetchall()

        for row in sentences:
            
            sentence = re.sub('\s+', ' ', row[0]).strip().replace('<i>', ' ').replace('</i>', ' ').replace('<br/>', ' ')
            
            result_sentences.append(sentence)
            result_sources.append(row[1])

        c.execute('SELECT DISTINCT cyrus_sentence FROM quotes WHERE cyrus_sentence_n = ?;', (n,))

        sentences = c.fetchall()

        for row in sentences:
            
            sentence = re.sub('\s+', ' ', row[0]).strip().replace('<i>', '').replace('</i>', '').replace('<br/>', '')
            
            result_sentences.append(sentence)
            result_sources.append('PG_the_garden_of_cyrus.xml')
            
    return result_sentences, result_sources


#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

def make_markov_chain(sentences, ngram_size):

    all_sentences_words = []

    for sentence in sentences:
        all_sentences_words.append(['START_SENTENCE'] + sentence.split() + ['END_SENTENCE'])

    markov_chain = {}

    for sentence_words in all_sentences_words: 

        if len(sentence_words) > ngram_size + 2:

            for a in range(0, len(sentence_words) - ngram_size):
            
                key = sentence_words[a: a + ngram_size]
                value = sentence_words[a + ngram_size]

                key = tuple(key)

                try:
                    markov_chain[key].append(value)
                except KeyError:
                    markov_chain[key] = [value]
                    
    return markov_chain


#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

def generate_new_sentences(markov_chain, original_sentences, number_of_sentences_to_generate):

    possible_sentence_beginnings =[]
    for markov_chain_key in markov_chain.keys():
        if markov_chain_key[0] == 'START_SENTENCE':
            possible_sentence_beginnings.append(markov_chain_key)

    iteration_limit = number_of_sentences_to_generate * 2
    number_of_sentences_created = 0
    all_sentences_created = []

    i = 0
    while number_of_sentences_created < number_of_sentences_to_generate and i < number_of_sentences_to_generate:
        
        i += 1

        randomStartingPoint = random.randint(0, len(possible_sentence_beginnings) - 1)
        
        sentence_beginning = possible_sentence_beginnings[randomStartingPoint]
        
        output_words = list(sentence_beginning[1:])
        markov_chain_key = sentence_beginning
        
        next_word = ''
        
        while next_word != 'END_SENTENCE':
        
            possible_next_words = markov_chain[markov_chain_key]
            
            random_word_index = random.randint(0, len(possible_next_words) - 1)
            
            next_word = possible_next_words[random_word_index]
            
            if next_word != 'END_SENTENCE':
                output_words.append(next_word)
                
            if len(output_words) > 100:
                break
                
            markov_chain_key = markov_chain_key[1:] + (next_word,)
        
        result_text = ' '.join(output_words)

        if result_text not in original_sentences and result_text not in all_sentences_created:
        
            number_of_sentences_created = number_of_sentences_created + 1
            all_sentences_created.append(result_text)
            
    return all_sentences_created

#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

def create_poem(new_sentences, poem):
    
    combined_sentences = ' '.join(new_sentences)
    
    i = 0

    for y in range(0, height):
        for x in range(0, width):
            if poem[x][y] == '#':
                if i > len(combined_sentences) - 1:
                    i = 0
                poem[x][y] = combined_sentences[i]
                i += 1
    
    return poem
    
#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------
   
def make_template(width, height, shape):

    template = []
    for x in range(0, width):
        line = []
        for y in range(0, height):
            line.append('#')
        template.append(line)
        
    if shape == 'x':
        
        x = 0
        y = 0
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        x = 1
        y = 0
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        x = 0
        y = 1
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
            
        x = 0
        y = height - 1
        while x < width and y > -1:
            template[x][y] = ' '
            x = x + 1
            y = y - 1
            
        x = 1
        y = height - 1
        while x < width and y > -1:
            template[x][y] = ' '
            x = x + 1
            y = y - 1
            
        x = 0
        y = height - 2
        while x < width and y > -1:
            template[x][y] = ' '
            x = x + 1
            y = y - 1
        
    if shape == 'diamond':
        
        #
        
        x = (width / 2) - 1 
        y = 0
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        x = (width / 2) + 1
        y = 0
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        x = (width / 2)
        y = 0
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        #
        
        x = (width / 2) - 1 
        y = 0
        while x > -1 and y < height:
            template[x][y] = ' '
            x = x - 1
            y = y + 1
        
        x = (width / 2) + 1
        y = 0
        while x > -1 and y < height:
            template[x][y] = ' '
            x = x - 1
            y = y + 1
        
        x = (width / 2)
        y = 0
        while x > -1 and y < height:
            template[x][y] = ' '
            x = x - 1
            y = y + 1
        
        #
        
        x = 0
        y = (height / 2) - 1 
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        x = 0
        y = (height / 2)
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        x = 0
        y = (height / 2) + 1
        while x < width and y < height:
            template[x][y] = ' '
            x = x + 1
            y = y + 1
        
        #
        
        x = width - 1
        y = (height / 2) - 1 
        while x > -1 and y < height:
            template[x][y] = ' '
            x = x - 1
            y = y + 1
        
        x = width - 1
        y = (height / 2)
        while x > -1 and y < height:
            template[x][y] = ' '
            x = x - 1
            y = y + 1
        
        x = width - 1
        y = (height / 2) + 1
        while x > -1 and y < height:
            template[x][y] = ' '
            x = x - 1
            y = y + 1
        
    return template


def print_poem(poem, width, height):

    print
    print
    for y in range(0, height):
        line = ''
        for x in range(0, width):
            line = line + poem[x][y]
        print line


#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

def make_ngram_poems(database_file, cyrus_sentence_numbers, ngram_size, number_of_sentences_to_generate, number_of_poems_to_generate, template, start_time, shape):

    original_sentences, sources = extract_sentences_from_db(database_file, cyrus_sentence_numbers)

    markov_chain = make_markov_chain(original_sentences, ngram_size)
    
    new_sentences = generate_new_sentences(markov_chain, original_sentences, number_of_sentences_to_generate)
    
    for i in range(0, number_of_poems_to_generate):
        
        random.shuffle(new_sentences)
        
        temp_template = copy.deepcopy(template)

        poem = create_poem(new_sentences, temp_template)
        
        simpler_poem = []
        for y in range(0, height):
            line = ''
            for x in range(0, width):
                line = line + poem[x][y]
            simpler_poem.append(line)
        
        print start_time + '|' + str(cyrus_sentence_numbers[0]) + '_' + str(i) + '|ascii_' + shape + '|' + json.dumps(simpler_poem) + '|' + json.dumps(sources)
    
#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

if __name__ == "__main__":
    
    database_file = sys.argv[1]
    cyrus_sentence_numbers = sys.argv[2].split(',')
    ngram_size = int(sys.argv[3])
    number_of_sentences_to_generate = int(sys.argv[4])
    width = int(sys.argv[5])
    height = int(sys.argv[6])
    shape = sys.argv[7]
    number_of_poems_to_generate = int(sys.argv[8])
    
    start_time = str(time.time())
    
    template = make_template(width, height, shape)
    
    if cyrus_sentence_numbers[0] == 'all':
        
        all_cyrus_sentence_numbers = []
        
        quotes_conn = sqlite3.connect(database_file)
        c = quotes_conn.cursor()
        
        c.execute('SELECT DISTINCT cyrus_sentence_n FROM quotes WHERE is_good = 1;')

        sentences = c.fetchall()
        for row in sentences:
            all_cyrus_sentence_numbers.append(str(row[0]))
            
        quotes_conn.close()
        
        for n in all_cyrus_sentence_numbers:

            make_ngram_poems(database_file, [n], ngram_size, number_of_sentences_to_generate, number_of_poems_to_generate, template, start_time, shape)
    else:
        make_ngram_poems(database_file, cyrus_sentence_numbers, ngram_size, number_of_sentences_to_generate, number_of_poems_to_generate, template, start_time, shape)
