
//  FROM http://www.kirupa.com/html5/shuffling_array_js.htm

Array.prototype.shuffle = function() {
    var input = this;
     
    for (var i = input.length-1; i >=0; i--) {
     
        var randomIndex = Math.floor(Math.random()*(i+1)); 
        var itemAtIndex = input[randomIndex]; 
         
        input[randomIndex] = input[i]; 
        input[i] = itemAtIndex;
    }
    return input;
}


//  START MY CODE

var CYRUS = {
    'query_string_parameters': '',
    'sentences': [],
};


$(document).ready(
    function() {
        
        CYRUS['query_string_parameters'] = get_query_string_parameters();
        
        if (CYRUS['query_string_parameters']['type'] == undefined) {
            alert('Invalid query string');
            return;
        }
        
        $.ajaxSetup({async:false});
        
        $.get('get_quote_counts.php?type=quote_poem_sentences', 
            function(data) {
                CYRUS['sentences'] = eval(data);
            }
        );
    
        if (CYRUS['query_string_parameters']['cyrus_sentence_n'] != undefined) {
            $.get('get_quotes.php?type=' + CYRUS['query_string_parameters']['type'] + '&cyrus_sentence_n=' + CYRUS['query_string_parameters']['cyrus_sentence_n'], 
                function(data) {
                    $('#quotes_body').html(data);

                    $('input:radio').change(
                        function() {

                            console.log('changed', $(this), $(this).val(), $(this).attr('name'), $(this).attr('n'));

                            $.get('update_quotes.php?n=' + $(this).attr('n') + '&value=' + $(this).val(), 
                                function(data) {
                                }
                            );
                        }
                    );
                }
            );
        }
        else {
            if (CYRUS['query_string_parameters']['other_file_name'] != undefined) {
                $.get('get_quotes.php?type=' + CYRUS['query_string_parameters']['type'] + '&other_file_name=' + CYRUS['query_string_parameters']['other_file_name'], 
                    function(data) {
                        $('#quotes_body').html(data);
                    }
                );
            }
            else {
                $.get('get_quote_counts.php?type=' + CYRUS['query_string_parameters']['type'], 
                    function(data) {
                        $('#quotes_body').html(data);
                    }
                );
            }
        }
    }
);


function get_query_string_parameters() {
 
    var results = {};
 
    var parts = window.location.search.substring(1).split('&');
    for (var a = 0; a < parts.length; a++) {
        var key = parts[a].split('=')[0];
        var value = parts[a].split('=')[1];
        results[key] = value;
    }
    
    return results;
}


function mark_sentence_bogus(sentence_n) {
    $.get('mark_bogus.php?sentence_n=' + sentence_n, 
        function(data) {
            window.location.assign(window.location.href);
        }
    );
}

function next_sentence(sentence_n) {
    
    var next_sentence_n = -1;
    for (var a = 0; a < CYRUS['sentences'].length - 1; a++) {
        if (CYRUS['sentences'][a] == sentence_n) {
            next_sentence_n = CYRUS['sentences'][a + 1];
            break;
        }
    }
    
    if (next_sentence_n != -1) {
        window.location.assign('/cyrus/quotes.html?type=sentences&cyrus_sentence_n=' + next_sentence_n);
    }
}

