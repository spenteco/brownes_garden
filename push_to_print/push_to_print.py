#!/usr/bin/python

import sys, sqlite3, re, codecs, json
from mako.template import Template

quotes_conn = sqlite3.connect('../../db/quotes.sqlite3')
poem_conn = sqlite3.connect('../../db/poems.sqlite3')
other_poem_conn = sqlite3.connect('../../db/other_poems.sqlite3')
catalog_conn = sqlite3.connect('../../db/catalog.sqlite3')

quote_template = Template(filename='templates/quote.html')
poem_template = Template(filename='templates/poem.html')
other_poem_template = Template(filename='templates/other_poem.html')
ascii_poem_template = Template(filename='templates/ascii_poem.html')
image_template = Template(filename='templates/image.html')
page_template = Template(filename='templates/page.html')

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

def get_catalog_entry(file_id):
        
    scrubbed_file_id = file_id.replace('_txt.xml', '.xml').replace('_', '-')
    
    if scrubbed_file_id == 'Song.xml' or scrubbed_file_id == 'Gen.xml' or scrubbed_file_id == 'Neh.xml' or scrubbed_file_id == 'Ps.xml':
        scrubbed_file_id = scrubbed_file_id.replace('.xml', '')
        
    if scrubbed_file_id == 'Ps':
        scrubbed_file_id = 'Psalms'
        
    if scrubbed_file_id.startswith('PG') == True:
        scrubbed_file_id = scrubbed_file_id.replace('-', '_')
        
    author = ''
    title = scrubbed_file_id
    
    c = catalog_conn.cursor()
    c.execute('SELECT author, title FROM catalog WHERE file_id = ?', (scrubbed_file_id,))
        
    entries = c.fetchall()
        
    for i, row in enumerate(entries):
        author = row[0]
        title = row[1]
        break
        
    return author, title
    
#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

def get_and_format_page(page_specs):
    
    result = ''
    
    if page_specs[0] in ['X', 'diamond', 'lattice', 'quincunx']:
        
        c = poem_conn.cursor()
        c.execute('SELECT poem_json, source_files, width, height FROM poems WHERE poem_type = ? AND start_time = ? and poem_number = ?;', (page_specs[0], page_specs[1], page_specs[2]))
        
        poem_data = c.fetchall()
        
        for d in poem_data:
            
            poem = json.loads(d[0])
            
            horizontal_spacing = (350.0 / float(d[2]))
            vertical_spacing = (500.0 / float(d[3]))
            
            positions = []
            for y in range(0, len(poem[0])):
                position_row = []
                for x in range(0, len(poem)):
                    position_row.append([horizontal_spacing * x, vertical_spacing * y + 15])
                    
                    if poem[x][y] == '#':
                        poem[x][y] = ' '
                    
                positions.append(position_row)
            
            source_file_ids = json.loads(d[1])
            
            sources = []
            for s in source_file_ids:
                
                author, title = get_catalog_entry(s)
                
                if author > '':
                    source = '<p class="source_citation">' + author + '. <i>' + title + '.</i></p>'
                    if source not in sources:
                        sources.append(source)
                else:
                    source = '<p class="source_citation"><i>' + title + '.</i></p>'
                    if source not in sources:
                        sources.append(source)
                
            sources.sort()
            
            result = poem_template.render(poem=poem, sources=sources, key=[page_specs[0], page_specs[1], page_specs[2]], positions=positions)
    
    if page_specs[0] in ['ascii_diamond', 'ascii_x', 'letter_ngrams', 'keep_sequence_10_8_10_8_10_8_10_8_10', 'keep_sequence_5_4_5_4_5']:
        
        c = other_poem_conn.cursor()
        c.execute('SELECT poem_json, source_files FROM poems WHERE poem_type = ? AND start_time = ? and poem_number = ?;', (page_specs[0], page_specs[1], page_specs[2]))
        
        poem_data = c.fetchall()
        
        for d in poem_data:
            
            poem = json.loads(d[0])
            source_file_ids = json.loads(d[1])
            
            sources = []
            for s in source_file_ids:
                
                author, title = get_catalog_entry(s)
                
                if author > '':
                    source = '<p class="source_citation">' + author + '. <i>' + title + '.</i></p>'
                    if source not in sources:
                        sources.append(source)
                else:
                    source = '<p class="source_citation"><i>' + title + '.</i></p>'
                    if source not in sources:
                        sources.append(source)
                
            sources.sort()
            
            if page_specs[0] in ['ascii_diamond', 'ascii_x', 'letter_ngrams']:
                result = ascii_poem_template.render(poem=poem, sources=sources, key=[page_specs[0], page_specs[1], page_specs[2]], poem_type=page_specs[0])
                
            if page_specs[0] in ['keep_sequence_10_8_10_8_10_8_10_8_10', 'keep_sequence_5_4_5_4_5']:
                result = other_poem_template.render(poem=poem, sources=sources, key=[page_specs[0], page_specs[1], page_specs[2]], poem_type=page_specs[0])
            
    if page_specs[0] in ['aviation', 'bands', 'one_square', 'four_square']:
        
        result = image_template.render(folder_name=page_specs[0], file_name=page_specs[1], image_class=page_specs[0], key=[page_specs[0], page_specs[1], page_specs[2]])
        
    if page_specs[0] == 'quote':
        
        c = quotes_conn.cursor()
        c.execute('SELECT cyrus_sentence, other_file_name, other_sentence FROM quotes WHERE cyrus_sentence_n = ?;', (page_specs[1],))
        
        sentence_data = []
        
        sentences = c.fetchall()
        
        for i, row in enumerate(sentences):
            
            if i == 0:
                sentence_data.append([row[0], 'Browne, Thomas, Sir', 'The garden of Cyrus, or the quincunciall, lozenge, or net-work plantations of the ancients, artificially, naturally, mystically considered.'])
                
            author, title = get_catalog_entry(row[1])
            sentence_data.append([row[2], author, title])
            
        result = quote_template.render(sentence_data=sentence_data, key=[page_specs[0], page_specs[1], page_specs[2]])
        
    if page_specs[0] == 'blank':
        result = '<br/>'
        
    if page_specs[0] == 'title_page':
        t = Template(filename='templates/title_page.html', input_encoding='utf-8')
        result = t.render()
        
    if page_specs[0] == 'publication_information':
        t = Template(filename='templates/publication_information.html', input_encoding='utf-8')
        result = t.render()
        
    if page_specs[0] == 'frontispiece':
        t = Template(filename='templates/frontispiece.html', input_encoding='utf-8')
        result = t.render()
        
    if page_specs[0] == 'concluding_page':
        t = Template(filename='templates/concluding_page.html', input_encoding='utf-8')
        result = t.render()
        
    if page_specs[0] == 'bibliography':
        t = Template(filename='templates/bibliography.html', input_encoding='utf-8')
        result = t.render()
        
    return result

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

layout = codecs.open(sys.argv[1], 'r', encoding='utf-8').read().split('\n')[1:]

content = []
bibliography = ''

for line in layout:
    if line.strip() > '':
        opening = line.split('|')
        if opening[0] == 'bibliography':
            bibliography = get_and_format_page(opening[:3])
        else:
            content.append([get_and_format_page(opening[:3]), get_and_format_page(opening[3:])])
    
page = page_template.render(content=content, bibliography=bibliography)

out_f = codecs.open(sys.argv[2], 'w', encoding='utf-8')
out_f.write(page)
out_f.close()
