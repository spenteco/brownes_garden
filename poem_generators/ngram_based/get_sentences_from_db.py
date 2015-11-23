#!/usr/bin/python

import sys, sqlite3

#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

def extract_sentences_from_db(database_file, words_to_select):

    db = sqlite3.connect(database_file)

    c = db.cursor()

    for w in words_to_select:

        c.execute('SELECT content FROM sentences WHERE content MATCH ?', (w,))

        n = 0
        while True:
          
            row = c.fetchone()
            
            if row == None:
                break
                
            print row[0]
            
            n += 1
            if n > 9999:
                break

#   --------------------------------------------------------------------
#
#   --------------------------------------------------------------------

if __name__ == "__main__":
    
    database_file = sys.argv[1]
    words_to_select = sys.argv[2].split(',')

    extract_sentences_from_db(database_file, words_to_select)
