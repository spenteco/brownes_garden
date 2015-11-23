#!/usr/bin/python

import re, pexpect, time
from textblob import TextBlob
from mako.template import Template
from xml.sax.saxutils import escape
from lxml import etree

def derive_pickle_file_name(a):
    
    result = ''
    
    if a.startswith('http') == True:
        result = ':'.join(a.split(':')[1:])
    else:
        result = a.split('/')[-1]
        
    result = re.sub('[^a-zA-Z0-9]', '_', result) + '.xml'
        
    return result
    
#
#   STANFORD-RELATED FUNCTIONS
#
    
def read_process_stdout_until_nlp_prompt(stanford_parser):
    
    result = ''

    n_timeouts = 0    

    while True:
        
        try:

            n_timeouts = 0

            result = result + stanford_parser.read_nonblocking(999999, 1)

            if 'NLP>' in result:
                result = result.replace('NLP>', '')
                break

        except pexpect.TIMEOUT:
            n_timeouts += 1
            if n_timeouts > 10000:
                break
            continue
        except pexpect.EOF:
            break
            
    return result

def start_stanford_parser(STANFORD_PARAMETERS, PATH_TO_STANFORD_CORENLP):

    jars = ['stanford-corenlp-3.5.2.jar',
            'stanford-corenlp-3.5.2-models.jar',
            'joda-time.jar',
            'xom.jar',
            'jollyday.jar']
    
    java_path = 'java'
    classname = 'edu.stanford.nlp.pipeline.StanfordCoreNLP'
    
    jars = [PATH_TO_STANFORD_CORENLP + jar for jar in jars]
    
    cmd = '%s -Xmx1800m -cp %s %s %s' % (java_path, ':'.join(jars), classname, STANFORD_PARAMETERS)

    stanford_parser = pexpect.spawn(cmd)

    noop = read_process_stdout_until_nlp_prompt(stanford_parser)
    
    return stanford_parser

def process_stanford_output_lexparser(raw_stanford_output, sentence_n):
    
    result = ''

    template = Template(filename='mako_templates/sentence.xml')

    raw_stanford_output_unicode = raw_stanford_output.decode('utf-8')

    lines = escape(raw_stanford_output_unicode).replace('\r', '').replace("\"", "&quot;").split('\n')
    
    starting_positions = []
    
    for i, line in enumerate(lines):
        if line.find('Sentence #') != -1 and line.find('tokens):') != -1:
            starting_positions.append(i)
            
    sentences = []
    
    for i in range(0, len(starting_positions)):
        
        start = starting_positions[i]
        end = -1
        if i < len(starting_positions) - 1:
            end = starting_positions[i + 1]
        
        sentences.append(lines[start: end])
        
    for s in sentences:
        
        raw_sentence = s[1]
        raw_tokens = []
        
        parse_tree_position = -1
        dependencies_position = -1
            
        raw_parse_tree = ''
        raw_dependencies = []
    
        for i, line in enumerate(s):
            if line.startswith('[Text=') == True:
                raw_tokens.append(line)
            if line.startswith('(ROOT') == True:
                parse_tree_position = i
            if line.startswith('root(ROOT') == True:
                dependencies_position = i
                break
                
        raw_parse_tree = '\n'.join(s[parse_tree_position: dependencies_position])
        raw_dependencies = s[dependencies_position: -1]

        tokens = []

        for t in raw_tokens:
            if t.strip() > '':

                t_parts = t[1:-1].split(' ')

                token = ''
                pos = ''
                lemma = ''

                for p in t_parts:
            
                    if p.startswith('Text='):
                        token = p.replace('Text=', '')
                    if p.startswith('PartOfSpeech='):
                        pos = p.replace('PartOfSpeech=', '')
                    if p.startswith('Lemma='):
                        lemma = p.replace('Lemma=', '')

                tokens.append([token, pos, lemma])

        dependencies = []

        for d in raw_dependencies:
            if d.strip() > '':

                try:
                
                    first_p = d.strip().find('(')
                    
                    dependency_type = d.strip()[:first_p]

                    dependency_terms = d.strip()[first_p + 1: -1].split(', ')
                
                    if len(dependency_terms) == 2:

                        a_token = dependency_terms[0].split('-')[0]
                        a_token_n = dependency_terms[0].split('-')[1]

                        b_token = dependency_terms[1].split('-')[0]
                        b_token_n = dependency_terms[1].split('-')[1]

                        dependencies.append([dependency_type, a_token, a_token_n, b_token, b_token_n])
                except:
                    print 'ERROR parsing dependencies', d

        sentence_xml = template.render(sentence_n=sentence_n, raw_sentence=raw_sentence, tokens=tokens, raw_parse_tree=raw_parse_tree.strip(), dependencies=dependencies)

        result = result + sentence_xml

    return result

def stanford_parse_text(stanford_parser, text):
    
    start_time = time.time()

    result = []
    
    blob = TextBlob(text)
    
    for sentence_n, sentence in enumerate(blob.sentences):
        
        sentence_start_time = time.time()
    
        stanford_parser.sendline(sentence.raw)
        
        raw_stanford_output = read_process_stdout_until_nlp_prompt(stanford_parser)
        
        parse_result = process_stanford_output_lexparser(raw_stanford_output, sentence_n)

        result.append(parse_result)
        
        sentence_end_time = time.time()
        
        #print 'sentence processed time', (sentence_end_time - sentence_start_time)

    end_time = time.time()

    print 'len(blob.sentences)', len(blob.sentences), (end_time - start_time)

    return '<elaboratedText>\n' + '\n'.join(result) + '\n</elaboratedText>\n'

#
#   CREATE A MARKOV CHAIN FROM A LIST OF LOADED SOURCES
#

def make_markov_chain(sources, markov_chain_ngram_length):
        
    markov_chain = {}
        
    for source in sources:
    
        sentences = source.data['tree'].xpath('//sentence')
        
        for sentence in sentences:
            
            tokens = sentence.xpath('descendant::token')
            
            if len(tokens) > markov_chain_ngram_length:
            
                token_values = ['START-SENTENCE']
                
                for token in tokens:
                    token_values.append(token.text)
                    
                token_values.append('END-SENTENCE')
                
                for a in range(0, len(token_values) - markov_chain_ngram_length - 1):
                    
                    markov_key = []
                    markov_next_token = ''
        
                    for b in range(0, markov_chain_ngram_length):
                        markov_key.append(token_values[a + b])
                    
                    markov_next_token = token_values[a + markov_chain_ngram_length + 1]
                    
                    try:
                        noop = markov_chain[tuple(markov_key)]
                    except KeyError:
                        markov_chain[tuple(markov_key)] = {}
                    
                    try:
                        noop = markov_chain[tuple(markov_key)][markov_next_token]
                    except KeyError:
                        markov_chain[tuple(markov_key)][markov_next_token] = 0

                    markov_chain[tuple(markov_key)][markov_next_token] += 1
        
    return markov_chain
    
