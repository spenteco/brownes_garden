#!/usr/bin/python

import sys, os, time, codecs, json
from lxml import etree

#   --------------------------------------------------------------------
#   
#   --------------------------------------------------------------------

input_folder = sys.argv[1]
output_folder = sys.argv[2]

for xml_file_name in os.listdir(input_folder):

    start_time = time.time()

    tree = etree.parse(input_folder + xml_file_name)
            
    sentences = tree.xpath('//sentence')
    
    for n, sentence in enumerate(sentences):
            
        sentence.set('n', str(n))
                
    f = codecs.open(output_folder + xml_file_name, 'w', encoding='utf-8')
    f.write(etree.tostring(tree))
    f.close()

    stop_time = time.time()

    print 'xml_file_name', xml_file_name, 'time', (stop_time - start_time)
