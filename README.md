# Browne's Garden Commonplace Book

## tl;dr

This is the code I used to generate *Browne's Garden Commonplace Book* for nanogenmo 2015.

For the PDF, see [http://montaukedp.com/Brownes_Garden_Commonplace_Book.pdf](http://montaukedp.com/Brownes_Garden_Commonplace_Book.pdf).
For more about the project, see [http://montaukedp.com/posts/browne.html](http://montaukedp.com/posts/browne.htmlhttp://montaukedp.com/posts/browne.html).

This repo reminds me of the joke about the pony ("I know there's a pony in there somewhere").  Not so much the pony, as the what the pony is (hopefully) buried in.  Still, I learned a few new things.


## Corpora and Catalog

No magic here.  Just *Sitzfleisch*.  I thought about a more automated approach, but decided that since *Sitzfleisch* == *done*.

Several years ago (three?  four?) I downloaded Project Gutenberg's English text files, downloaded their catalog, and parsed the catalog into CSV.  To select texts, I arranged the columns in the spreadsheet so that the PG-supplied LOC catalog codes were in one column, and then I paged and search through the spreadsheet looking for texts that I thought would work with Browne.  I selected texts which met one or more of several critera: a) Is the text one that Browne knew?  b) Is the text by a contemporary?  c) Is the text about a subject central to *The Garden of Cyrus* (*GoC*)?  d) Was the writer influenced by Browne?  e) Is the text one that I would like to put into dialog with Browne?  I also tossed in four books from the Bible which I thought would work.  The result was about 260 texts: http://localhost/cyrus/bibliography.html

Project Gutenberg (PG) provides *GoC* as a part of a collection of Browne's works, so by hand I split out Browne's works into separate files, removing the PG headers as I went.  I left the PG headers on everything else, which didn't prove to be a problem.  I should have spent more time cleaning up *GoC*, mostly removing footnotes, but I didn't.


## text_to_xml

This bit is way over-thought.  I had imagined a system which dealt with collections of sources as a single object ("object" in the software engineering sense of the word); however, that proved impractical since, at the time I first wrote this, I didn't know what I wanted to do.

Still, it's proven useful to nlp-process a batch of texts, then use xpath to query for subsets of texts.  I've actually used this code more at work than for browne's garden.  I could have done browne's garden with TextBlob and without XML (I only needed sentence splitting, tokenizing, and lemmatizing), which would have been much simpler.

To run:

>   ./process_test_data.py folder_of_plain_text_inputs folder_of_xml_outputs

Note that here and elsewhere, a trailing "/" is required on folder names.  I used to check for them and add them if necessary, but I've stopped doing so--I can usually remember to supply them.

It requires [TextBlob](https://textblob.readthedocs.org/en/dev/), java, [Mako templates](http://www.makotemplates.org/), and [the Stanford corenlp package] (http://nlp.stanford.edu/software/corenlp.shtml).  Note that the path to and parameters for corenlp are hard-coded in the script.  It splits plain text into sentences, gets a variety of information about each sentence (tokens, lemmas, parts of speech, type depedencies, and parse tree), and outputs the result as XML.  I think I could have gotten by with just TextBlob, although I'd like to think that some day type depedencies and parse trees will prove useful. 

It's not problem free.  It doesn't like texts with XML reserved characters (easy to fix).  It uses a lot of memory (I wasn't able to use Burton's *The Anatomy of Melancholy* in browne's garden, since it requires more memory that I have at home; I'm using TextBlob pre-split texts into sentences, and processing texts sentence-by-sentence through corenlp, since that reduces the memory requirements).  And occassionally it will hang--the process won't end, but it also won't use any processor, I think because the standard output deviates from what I've pexpect to expect (it starts corenlp as a separate process). 
But still, I've ran > 800 texts through it, so I'm pretty comfortable with it.  Credit is due [the stanford corenlp python project](
https://github.com/dasmith/stanford-corenlp-python), which was my starting point.

The other scripts in this folder (extract_bible_plain_text.py, fix_encoding.py, fix_sentence_n.py) are bits I found useful, and would like to hang on to.  fix_sentence_n.py is evidence that I somehow lost the ability to count. 


## Quotes

This is the core of the process, and one of the two or three things about this project that was new to me.  I've used full text indexing (Lucene, mostly) at work for "normal" text searching, but it had never occurred to me to use it as part of a text generation process.  For this project, I used [Whoosh](https://pypi.python.org/pypi/Whoosh/), which is dead easy.

I start by loading an index with everything except *GoC*.  Note that I'm loading each sentence from the corpus as a separate whoosh document.

>   ./make_whoosh_index.py folder_of_xml_inputs folder_for_whoosh_index

Next, I extract a list of words in *GoC* which are also in the rest of the corpus.  There's not any actually tf_idf in the script--I realized I didn't need it after I had started on this step.  And I'm not entirely sure that this is necessary.

>   ./tf_idf_etc.py folder_of_xml_inputs > some_file_name

>   ./word_list_from_tf_idf.py some_file_name > all_good_words.py

I then search whoosh.  For every *GoC* sentence, I look for matching sentences in the corpus;

>   ./search_whoosh_index.py folder_for_whoosh_index path_to_garden_of_cyrus.xml > some_output_file

Next, I load a sqlite3 database with the results (see data/db/quotes.sqlite3.SKELETON for the schema--note that I'm using sqlite3 as a container for json objects, i.e., as a poor man's mongo).  Why a separate step?  Kind of a try before you buy deal . . . 

>   ./matches_to_database.py some_output_file path_to_quotes_database

Epic *Sitzfleisch* ensued.  I used [a simple web interface]( http://montaukedp.com/apps/cyrus/quotes.html?type=sentences) to pick through matching sentences, effectively culling out *GoC* "sentences which were bogus, and then futher culling out what I perceived to be high-quality matching sentences.  

This curation was not as mind-numbing as it seems (although it was thoroughly ass-numbing).  In fact, it ended up being an interesting reading experience.  For example, I had heard about Tagore, but I didn't know how congenial he could be to someone raised on Emerson and Thoreau.  Job one next is, I think, to actually read an entire book by him.


## Poem Generators

### Whoosh-based

These scripts produced the shaped poems paired with ornament images in the PDF.

>   ./make_X_poem.py path_to_quotes_db path_to_whoosh_index width height number_of_poems_per_sentence some_output_file

>   ./make_diamond_poem.py path_to_quotes_db path_to_whoosh_index width height number_of_poems_per_sentence some_output_file

>   ./make_lattice_poem.py path_to_quotes_db path_to_whoosh_index width height number_of_poems_per_sentence some_output_file

>   ./make_quincunx_poem.py path_to_quotes_db path_to_whoosh_index width height number_of_poems_per_sentence some_output_file
                
Then, I loaded the results into a sqlite3 database (see data/db/poems.sqlite3.SKELETON):

>   ./load_poem_database.py some_output_file path_to_poems_database

I'm not happy with the results, mostly because they don't leave enough black on the page.  And I'm not sure, but I think I managed to mangle the coordinate system somewhere (lines, which should run left-to-right, whether up or down, seem to run in the opposite direction in some cases).  I don't know whether to invest more in these or not.

The poems were generated by searching the whoosh index, and then by applying regexes to the results.  The process deserves more thought, especially the use of whoosh, which would seem to enable ngram and, with the proper preparation of the data and an appropriate schema, CFG-based text generation across very large corpora.  Even though I'm not happy with these results, the use of whoosh in this sort of work deserves further attention.
 

### ngram-based

These scripts generated the poems paired with quotations in the PDF (cut-and-pasted from my notes):
                
>   ./make_asci_poem.py path_to_quotes_database all 1 20 31 31 diamond 2 

>   ./make_asci_poem.py path_to_quotes_database all 1 20 31 31 x 2 

>   ./make_letter_ngrams.py path_to_quotes_database all 5 30 40 25 2

>   ./make_ngram_keep_sequence.py path_to_quotes_database all 1 20 "5,4,5,4,5" 2 5 

>   ./make_ngram_keep_sequence.py path_to_quotes_database all 1 20 "10,8,10,8,10,8,10,8,10" 2 3 

Apologies for not explaining the parameters . . . the scripts are pretty obvious, however.

I loaded the results into a sqlite3 database (see data/db/other_poems.sqlite3.SKELETON . . . toward the end of the project, I completely list the ability to name things sensibly):

>   ./load_poem_database.py some_output_file path_to_poems_database

I don't much care for the "diamond" and "x" poems.  The "letter ngram" poems are potentially interesting--I like the idea of legible words emerging from a soup of characters--but underdeveloped.  I really like the "ngram keep sequence" and thought seriously about including just them and the quotations in the PDF.

The important point here: These scripts generate poems based on very few sentences.  For the PDF, I ran them on single rows from the quotation database.  I.e., on just five sentences, one from *GoC* plus four matching sentences.  I'm able to do this because I curated quotations, and because the five sentence sets overlap enough to make ngram generation (mostly) practical.  And, because I start with matching sentences, I'm able to use very short (one word!) markov chain keys and still get reasonable results simply because I started with a coherent set of sentences.

                
## Web

Not much to see here.  I basically recycled the code of Mutable Stanzas (http://montaukedp.com/apps/mutableStanzas/).  The code (very php-y php) simply reads one or another of the projects sqlite3 database and returns json, which the client formats appropriately.  At one point, I thought the web site would be the result, so I spent a fair amount of time getting it to look pleasant.

URL's:
                
[quotations](http://montaukedp.com/apps/cyrus/quote_poems.html?process=sequential)

[x poems](http://montaukedp.com/apps/cyrus/poems.html?type=X&process=sequential)

[diamond poems](http://montaukedp.com/apps/cyrus/poems.html?type=diamond&process=sequential)

[lattice poems](http://montaukedp.com/apps/cyrus/poems.html?type=lattice&process=sequential)

[quincunx poems](http://montaukedp.com/apps/cyrus/poems.html?type=quincunx&process=sequential)

[one square ornaments](http://montaukedp.com/apps/cyrus/image.html?process=random&type=one_square)

[four square ornaments](http://montaukedp.com/apps/cyrus/image.html?process=random&type=four_square)

[aviation images](http://montaukedp.com/apps/cyrus/image.html?process=random&type=aviation)

[ascii diamond poems](http://montaukedp.com/apps/cyrus/other_poems.html?type=ascii_diamond&process=sequential)

[ascii x poems](http://montaukedp.com/apps/cyrus/other_poems.html?type=ascii_x&process=sequential)

[letter ngrams](http://montaukedp.com/apps/cyrus/other_poems.html?type=letter_ngrams&process=sequential)

[wide ngram poems](http://montaukedp.com/apps/cyrus/other_poems.html?type=keep_sequence_10_8_10_8_10_8_10_8_10&process=sequential)

[narrow ngram poems](http://montaukedp.com/apps/cyrus/other_poems.html?type=keep_sequence_5_4_5_4_5&process=sequential)


## Images

I downloaded images by hand and cropped them by hand.  I pushed images of ornaments through potrace and tweaked the colors.  I processed the aviation images through [linoleumBlocks](
https://github.com/spenteco/linoleumBlocks).


## Push to Print

This part is really embarrassing.  I have no command whatsoever of any page layout or desktop publishing solution.  I've done a little bit of PDF generation, but it's been ages, and I can't recall what I did.

First, I generate a CSV file which contains one line per opening.  Each line contains the keys into whatever content types (two, a recto and verso) go on that page.  I ran the process on every content type individually:

>   ./generate_test_layout_csv.py database_type content_type > some_layout_file_name.csv

And then I ran a similar process to generate the layout for the PDF:

>   ./generate_live_layout_csv.py > some_layout_file_name.csv

In both cases, I then generated HTML:

>   ./push_to_print.py some_layout_file_name.csv test_print/some_page_name.html

I pushed the test_print folder to my local apache, opened the web page in Chrome, clicked print, and saved the PDF.  Done, right?

Not really.  It was hideous.  The css turned into a mess.  Print in both Chrome and Firefox did not work like I expected.  I ended up converting SVG's to jpg, then pre-sizing the jpgs (for some reason, I was breaking the browser's expected jpg-resize behavior).  Little bits got different CSS rules.  Rules piled on top of rules.  Etc.  I finally said, "good enough."

The next thing I do, as soon as I've recovered from this week, is learn how to properly layout content for print.

