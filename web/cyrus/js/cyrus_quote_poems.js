
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
    'interface_state': 'running',
    'interface_type': 'quotes',
    'SVG_MARGIN': 20,
    'SVG_WIDTH': 500,
    'SVG_HEIGHT': 700,
    'query_string_parameters': '',
    'process': '',
    'sentence_numbers': '',
    'sentence_numbers_index': -1,
    'sentence_data': '',
    'timeout_interval': 5000,
    //'timeout_interval': 1000,
    'timeout_handle': '',
    'fade_duration': 1000,
    //'fade_duration': 250,
    'timer_queue': [],
    'interface_state': 'running',
};


$(document).ready(
    function() {
        
        initialize_controls();
        
        CYRUS['query_string_parameters'] = get_query_string_parameters();
        
        if (CYRUS['query_string_parameters']['process'] == undefined) {
            alert('Invalid query string');
            return;
        }
        
        CYRUS['process'] = CYRUS['query_string_parameters']['process'];
        
        $.ajaxSetup({async:false});
        
        $.get('get_quote_counts.php?type=quote_poem_sentences', 
            function(data) {
                CYRUS['sentence_numbers'] = eval(data);
            }
        );
        
        if (CYRUS['process'] == 'random') {
            CYRUS['sentence_numbers'].shuffle();
        }
        
        CYRUS['sentence_numbers_index'] = -1;
        
        display_quote_loop();
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


function display_quote_loop() {

    var previous_sentence_numbers_index = CYRUS['sentence_numbers_index'];
    
    CYRUS['sentence_numbers_index'] = CYRUS['sentence_numbers_index'] + 1;
    
    if (CYRUS['sentence_numbers_index'] > CYRUS['sentence_numbers'].length - 1) {
        
        CYRUS['sentence_numbers_index'] = 0;
        
        if (CYRUS['process'] == 'random') {
            CYRUS['sentence_numbers'].shuffle();
        }
    }
    
    var i = CYRUS['sentence_numbers_index'];
    
    $.ajaxSetup({async:false});
        
    $.get('get_quotes.php?type=quote_poem_sentences&cyrus_sentence_n=' + CYRUS['sentence_numbers'][i], 
        function(data) {
            CYRUS['sentence_data'] = eval(data);
        }
    );

    //console.log(CYRUS['sentence_data'][1][0]);
    //CYRUS['sentence_data'].shuffle();
    //console.log(CYRUS['sentence_data'][1][0]);

    var indexes = [];
    for (var a = 0; a < CYRUS['sentence_data'][1].length; a++) {
        indexes.push(a);
    }
    indexes.shuffle();
    
    var html = '<div class="poem_container" id="poem_container_' + CYRUS['sentence_numbers_index'] + '" style="width: 600px; display: none;">'

    html = html + '<p class="cyrus_sentence">' + CYRUS['sentence_data'][0] + '</p>' + CYRUS['sentence_data'][2];
    
    for (var a = 0; a < indexes.length; a++) {
        html = html + '<p class="other_sentence">' + CYRUS['sentence_data'][1][indexes[a]][0] + '</p>';
        if (CYRUS['sentence_data'][1][indexes[a]][1] > '') {
            html = html + '<p class="other_sentence_source"><span class="author">' + CYRUS['sentence_data'][1][indexes[a]][1] + '. </span> <span class="title">' + CYRUS['sentence_data'][1][indexes[a]][2] + '.</span></p>';
        }
        else {
            html = html + '<p class="other_sentence_source"><span class="title">' + CYRUS['sentence_data'][1][indexes[a]][2] + '.</span></p>';
        }
    }

    html = html + '</div>';

    $('#quote_poems').append(html);

    $('#quote_poem_container_' + CYRUS['sentence_numbers_index']).css({'position': 'absolute', 'top': '10px', 'left': '20px'});

    if (previous_sentence_numbers_index != -1) {
        CYRUS['timer_queue'].push(['fadeOut', previous_sentence_numbers_index, CYRUS['fade_duration']]);
    }
        
    CYRUS['timer_queue'].push(['fadeIn', CYRUS['sentence_numbers_index'], CYRUS['fade_duration']]);
    CYRUS['timer_queue'].push(['setTimeout', -1, CYRUS['timeout_interval']]);

    handle_timer_queue();
}

function handle_timer_queue() {

    if (CYRUS['interface_state'] == 'running') {

        var queue_entry = CYRUS['timer_queue'].shift();

        if (queue_entry[0] == 'fadeOut') {
            $('#poem_container_' + queue_entry[1]).fadeOut(queue_entry[2]);
            CYRUS['timeout_handle'] = setTimeout(handle_timer_queue, queue_entry[2]);
        }

        if (queue_entry[0] == 'fadeIn') {
            $('#poem_container_' + queue_entry[1]).fadeIn(queue_entry[2]);
            CYRUS['timeout_handle'] = setTimeout(handle_timer_queue, queue_entry[2]);
        }

        if (queue_entry[0] == 'setTimeout') {
            CYRUS['timeout_handle'] = setTimeout(display_quote_loop, queue_entry[2]);
        }
    }
}

