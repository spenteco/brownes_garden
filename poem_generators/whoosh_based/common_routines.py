import json, re, random, string, sqlite3
from textblob import TextBlob
from texts_in_quote_db import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


def print_poem(poem):

    print
    for y in range(0, len(poem[0])):
        out = ''
        for x in range(0, len(poem)):
            out = out + ' ' + poem[x][y]
        print out


def is_poem_valid(poem):
    
    result = True
    
    for x in range(0, len(poem)):
        for y in range(0, len(poem[x])):
            if poem[x][y] == '#':
                result = False
                
    return result


def is_poem_fixable(poem, error_limit):
    
    result = True
    n_errors = 0    

    for x in range(0, len(poem)):
        for y in range(0, len(poem[x])):
            if poem[x][y] == '#':
                n_errors += 1

    if n_errors > error_limit:
        result = False
                
    return result


def write_poem_to_database(start_time, poem_number, poem_type, POEM_WIDTH, POEM_HEIGHT,  poem, poem_sources, output_file):
    
    output_file.write(str(start_time) + '|' + str(poem_number) + '|' + str(poem_type) + '|' + str(POEM_WIDTH) + '|' + str(POEM_HEIGHT) + '|' + json.dumps(poem) + '|' + json.dumps(list(set(poem_sources))) + '\n')


def load_text(QUOTE_DB_FILE, ngram_sizes_required, cyrus_only):
    
    raw_sentences = []

    quotes_conn = sqlite3.connect(QUOTE_DB_FILE)
    c = quotes_conn.cursor()
    
    if cyrus_only == False:

        c.execute('SELECT DISTINCT other_sentence, other_file_name FROM quotes;')

        sentences = c.fetchall()

        for row in sentences:
            
            sentence = re.sub('\s+', ' ', row[0]).strip().replace('<i>', ' ').replace('</i>', ' ').replace('<br/>', ' ')
            
            raw_sentences.append([sentence, row[1]])

    c.execute('SELECT DISTINCT cyrus_sentence FROM quotes;')

    sentences = c.fetchall()

    for row in sentences:
        
        sentence = re.sub('\s+', ' ', row[0]).strip().replace('<i>', '').replace('</i>', '').replace('<br/>', '')
            
        raw_sentences.append([sentence, 'PG_the_garden_of_cyrus_txt.xml'])

    up_markov_chain = {}
    down_markov_chain = {}

    ngrams = {}
    for n in ngram_sizes_required:
        ngrams[n] = []
        
    for sentence, source_file_name in raw_sentences:

        blob = TextBlob(sentence)

        words = []
        for t in blob.words:
            words.append(t.replace('_', ''))
                
        for a in range(0, len(words)):
            if a > 0:
                try:
                    up_markov_chain[words[a]].append(words[a - 1])
                except KeyError:
                    up_markov_chain[words[a]] = [words[a - 1]]
            if a < len(words) - 1:
                try:
                    down_markov_chain[words[a]].append(words[a + 1])
                except KeyError:
                    down_markov_chain[words[a]] = [words[a + 1]]
        
        for n in ngram_sizes_required:
            if len(words) >= n:
                for a in range(0, len(words) - n + 1):
                    if tuple(words[a: a + n]) not in ngrams[n]:
                        ngrams[n].append([tuple(words[a: a + n]), source_file_name])

    return up_markov_chain, down_markov_chain, ngrams


def open_whoosh_index(WHOOSH_FOLDER):

    return open_dir(WHOOSH_FOLDER)


def search_whoosh_index(whoosh_index, regex_match_string, words_to_lookup):

    final_results = []

    query = unicode(' OR '.join(words_to_lookup))
    qp = QueryParser('content', schema=whoosh_index.schema)
    q = qp.parse(query)

    with whoosh_index.searcher() as s:
        
        results = s.search(q, limit=999, terms=True)
        
        for r in results:

            if r['sentence_key'].split('|')[0] in texts_in_quote_db:
            
                m = re.search(regex_match_string, r['content'])
                if m != None:

                    ngram = re.split('\W+', m.group(0))

                    ngram_is_valid = True
                    for n in ngram:
                        try:
                            noop = int(n)
                            ngram_is_valid = False
                        except:
                            pass

                    if ngram_is_valid == True:
                        final_results.append([ngram, r['sentence_key'].split('|')[0]])    

    return final_results


