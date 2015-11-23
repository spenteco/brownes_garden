#!/usr/bin/python

import sys, os, codecs

for file_name in os.listdir(sys.argv[1]):

    file_okay = False

    try:
        noop = codecs.open(sys.argv[1] + file_name, 'r', encoding='utf-8').read()
        file_okay = True
    except:
        print 'error (1)', file_name

    if file_okay == False:
        try:
            
            f = codecs.open(sys.argv[1] + file_name, 'r', encoding='iso-8859-1')
            data = f.read()
            f.close()
            
            f = codecs.open(sys.argv[1] + file_name, 'w', encoding='utf-8')
            f.write(data)
            f.close()
            
        except:
            print 'error (2)', file_name
        
