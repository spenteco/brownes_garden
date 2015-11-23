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

def lookup_word_in_cmudict(word, cmu, cmu_shortcut):
    
    n_syllables = 0
    
    try:
        n_syllables = cmu_shortcut[word.lower()]
    except KeyError:
    
        vowels = ['AO', 'AA', 'IY', 'UW', 'EH', 'IH', 'UH', 'AH', 'AX', 'AE', 'EY', 'AY', 'OW', 'AW', 'OY', 'ER']
            
        inDictionary = False
        if word.lower() in cmu:
            inDictionary = True
        
        cmu_entry = None
        if inDictionary == True:
            cmu_entry = cmu[word.lower()][0]
            
        if cmu_entry != None:
            for r in cmu_entry:
                if r[-1].isdigit() == True:
                    n_syllables += 1
                    
        if n_syllables == 0:
            if word.strip() == '' or '~`!@#$%^&*()_+-={}|[]\:";\'<>?,./'.find(word.strip()) != -1 or word == '--':
                n_syllables = None
            else:
                if word.strip().startswith('-') and word.strip().endswith('-') or word.strip().startswith(';-') and word.strip().endswith('-'):
                    n_syllables = None
                else:
                    if word.strip().startswith('\'') and len(word.strip()) == 2:
                        n_syllables = None
                    else:
                    
                        n_syllables = 0
                        
                        word_less_hyphen = word.strip().split('-')
                        
                        for word_less in word_less_hyphen:
                            
                            if word_less > '':
                                
                                trimmed_word = word_less.strip().lower()
                                result_letters = []
                                for a in range(0, len(trimmed_word)):
                                    if trimmed_word[a] in ['a', 'e', 'i', 'o', 'u', 'y']:
                                        result_letters.append(trimmed_word[a])
                                    else:
                                        result_letters.append(' ')
                                        
                                if result_letters[-1] == 'e':
                                    result_letters[-1] = ' '
                                trimmed_word = ''.join(result_letters).strip()
                            
                                syllables = re.split('\s+', trimmed_word)
                                
                                n_syllables += len(syllables)
                        
                        if n_syllables == 0:
                            n_syllables = None
                            
        cmu_shortcut[word.lower()] = n_syllables
                  
    return n_syllables
    

def find_sentence_syllable_n(new_sentences, cmu, cmu_shortcut):
    
    new_sentence_syllables = []
    
    for sentence in new_sentences:

        sentence_parts = re.split(' ', re.sub('\'|"|_', '', sentence))

        sentence_breaks = [0]
        expanded_sentence_parts = []

        for b in range(0, len(sentence_parts)):
        
            word = sentence_parts[b]
            word_n_syllables = 0

            if sentence_parts[b].strip() > '':

                if sentence_parts[b][-1] in ',.?;:()!':
                    sentence_breaks.append(b)
                    word = sentence_parts[b][:-1]
        
                word_n_syllables = lookup_word_in_cmudict(word, cmu, cmu_shortcut)

            if word_n_syllables != None:
                new_sentence_syllables.append([sentence_parts[b], word_n_syllables])
    
    return new_sentence_syllables


#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

def create_stanzas(new_sentence_syllables, stanza_pattern):
    
    first_pass_stanzas = []
        
    stanza = []
    line = []
    line_syllables = 0
    
    for i in range(0, len(new_sentence_syllables)):
        
        if len(stanza) == len(stanza_pattern):
            
            first_pass_stanzas.append(stanza)
            
            stanza = []
            line = []
            line_syllables = 0
        
        line.append(new_sentence_syllables[i][0])
        line_syllables += new_sentence_syllables[i][1]
        
        if line_syllables >= stanza_pattern[len(stanza)]:
            stanza.append([' '.join(line), line_syllables])
            line = []
            line_syllables = 0
        
    if len(stanza) == len(stanza_pattern):
        first_pass_stanzas.append(stanza)
            
    final_stanzas = []
    
    for stanza in first_pass_stanzas:
        stanza_is_good = True
        for i in range(0, len(stanza)):
            if stanza[i][1] != stanza_pattern[i]:
                stanza_is_good = False
        if stanza_is_good == True:
            final_stanza = []
            for s in stanza:
                final_stanza.append(re.sub('\s+', ' ', re.sub('[^a-z1-9\-]', ' ', s[0].lower())))
                #final_stanza.append(s[0])
            final_stanzas.append(final_stanza)
            
    return final_stanzas
    
    
#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

def make_ngram_poems(database_file, cyrus_sentence_numbers, ngram_size, number_of_sentences_to_generate, stanza_pattern, number_of_poems_to_generate, number_of_stanzas_per_poem, start_time):

    original_sentences, sources = extract_sentences_from_db(database_file, cyrus_sentence_numbers)

    markov_chain = make_markov_chain(original_sentences, ngram_size)
    
    new_sentences = generate_new_sentences(markov_chain, original_sentences, number_of_sentences_to_generate)
        
    cmu = cmudict.dict()
    cmu_shortcut = {}
    
    accumulated_stanzas = []
    
    for i in range(0, 100):
        
        random.shuffle(new_sentences)
        
        new_sentence_syllables = find_sentence_syllable_n(new_sentences, cmu, cmu_shortcut)

        stanzas = create_stanzas(new_sentence_syllables, stanza_pattern)
         
        for s in stanzas:
            if s not in accumulated_stanzas:
                accumulated_stanzas.append(s)
                
    if len(accumulated_stanzas) > number_of_stanzas_per_poem:
            
        for a in range(0, number_of_poems_to_generate):
            
            random.shuffle(accumulated_stanzas)
            
            finished_poem = []
            
            for b in range(0, number_of_stanzas_per_poem):
                
                finished_poem.append(accumulated_stanzas[b])
                
                stanza_pattern_str = []
                for s in stanza_pattern:
                    stanza_pattern_str.append(str(s))
        
            print start_time + '|' + str(cyrus_sentence_numbers[0]) + '_' + str(i) + '_' + str(a) + '|keep_sequence_' + '_'.join(stanza_pattern_str) + '|' + json.dumps(finished_poem) + '|' + json.dumps(sources)
    
#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

if __name__ == "__main__":
    
    database_file = sys.argv[1]
    cyrus_sentence_numbers = sys.argv[2].split(',')
    ngram_size = int(sys.argv[3])
    number_of_sentences_to_generate = int(sys.argv[4])
    
    temp = sys.argv[5].split(',')
    stanza_pattern = []
    for t in temp:
        stanza_pattern.append(int(t))
        
    number_of_poems_to_generate = int(sys.argv[6])
    number_of_stanzas_per_poem = int(sys.argv[7])
    
    start_time = str(time.time())
    
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
            
            make_ngram_poems(database_file, [n], ngram_size, number_of_sentences_to_generate, stanza_pattern, number_of_poems_to_generate, number_of_stanzas_per_poem, start_time)
    else:
        
        make_ngram_poems(database_file, cyrus_sentence_numbers, ngram_size, number_of_sentences_to_generate, stanza_pattern, number_of_poems_to_generate, number_of_stanzas_per_poem, start_time)
