
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
    'interface_type': 'poems',
    'SVG_MARGIN': 20,
    'SVG_WIDTH': 500,
    'SVG_HEIGHT': 700,
    'query_string_parameters': '',
    'catalog': '',
    'type': '',
    'process': '',
    'poem_keys': '',
    'poem_keys_index': -1,
    'poem_width': '',
    'poem_height': '',
    'poem_source_files': '',
    'poem': '',
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
        
        if (CYRUS['query_string_parameters']['type'] == undefined || CYRUS['query_string_parameters']['process'] == undefined) {
            alert('Invalid query string');
            return;
        }
        
        CYRUS['type'] = CYRUS['query_string_parameters']['type'];
        CYRUS['process'] = CYRUS['query_string_parameters']['process'];
        
        $.ajaxSetup({async:false});
    
        $.get('get_catalog.php', 
            function(data) {
                CYRUS['catalog'] = eval(data);
            }
        );
        
        $.get('get_poem_keys.php?type=' + CYRUS['type'], 
            function(data) {
                CYRUS['poem_keys'] = eval(data);
            }
        );
        
        if (CYRUS['process'] == 'random') {
            CYRUS['poem_keys'].shuffle();
        }
        
        CYRUS['poem_keys_index'] = -1;
        
        display_poem_loop();
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


function display_poem_loop() {

    var previous_poem_keys_index = CYRUS['poem_keys_index'];
    
    CYRUS['poem_keys_index'] = CYRUS['poem_keys_index'] + 1;
    
    if (CYRUS['poem_keys_index'] > CYRUS['poem_keys'].length - 1) {
        
        CYRUS['poem_keys_index'] = 0;
        
        if (CYRUS['process'] == 'random') {
            CYRUS['poem_keys'].shuffle();
        }
    }
    
    var i = CYRUS['poem_keys_index'];
        
    $.ajaxSetup({async:false});
    
    var data_from_server = '';
    
    $.get('get_poem.php?start_time=' + CYRUS['poem_keys'][i][0] + '&poem_type=' + CYRUS['poem_keys'][i][1] + '&poem_number=' + CYRUS['poem_keys'][i][2], 
        function(data) {
            data_from_server = eval(data.replace(/\#/g, ' '));
        }
    );
    
    CYRUS['poem_width'] = parseInt(data_from_server[0]);
    CYRUS['poem_height'] = parseInt(data_from_server[1]);
    CYRUS['poem_source_files'] = eval(data_from_server[2]);
    CYRUS['poem'] = eval(data_from_server[3]);

    var html = '<div class="poem_container" id="poem_container_' + CYRUS['poem_keys_index'] + '">'

    var html = html + '<div class="poem_div"><svg width="' + CYRUS['SVG_WIDTH'] + '" height="' + CYRUS['SVG_HEIGHT'] + '">';

    var x_increment = (CYRUS['SVG_WIDTH'] - (CYRUS['SVG_MARGIN'] * 2)) / CYRUS['poem_width'];
    var y_increment = (CYRUS['SVG_HEIGHT'] - (CYRUS['SVG_MARGIN'] * 2)) / CYRUS['poem_height']

    for (var y = 0; y < CYRUS['poem'][0].length; y++) {
        for (var x = 0; x < CYRUS['poem'].length; x++) {
            html = html +'<text x="' + ((x * x_increment) + CYRUS['SVG_MARGIN']) + '" y="' + ((y * y_increment) +  + CYRUS['SVG_MARGIN']) + '">' + CYRUS['poem'][x][y] + '</text>';
        }
    }
    
    html = html + '</svg></div>';

    //var output_sources = '';
    
    var output_sources = [];
    
    for (var a = 0; a < CYRUS['poem_source_files'].length; a++) {
        
        var matching_id = CYRUS['poem_source_files'][a].replace(/_txt.xml/, '.xml').replace(/_/, '-').replace('PG-', 'PG_');
        
        var author = 'NOT FOUND'
        var title = matching_id;
        
        for (var b = 0; b < CYRUS['catalog'].length; b++) {
            if (matching_id == CYRUS['catalog'][b][0]) {
                author = CYRUS['catalog'][b][1];
                title = CYRUS['catalog'][b][2];
                break;
            }
        }
        
        if (author > '') {
            output_sources.push('<p class="source_citation">' + author + '. <i>' + title + '.</i></p>');
        }
        else {
            output_sources.push('<p class="source_citation"><i>' + title + '.</i></p>');
        }
    }

    output_sources.sort();

    html = html + '<div class="source_citations">';
    
    for (var a = 0; a < output_sources.length; a++) {
        html = html + output_sources[a];
    }
    
    html = html + '</div></div>';

    $('#poems').append(html);

    $('#poem_container_' + CYRUS['poem_keys_index']).css({'position': 'absolute', 'top': '10px', 'left': '20px'});

    if (previous_poem_keys_index != -1) {
        CYRUS['timer_queue'].push(['fadeOut', previous_poem_keys_index, CYRUS['fade_duration']]);
    }
        
    CYRUS['timer_queue'].push(['fadeIn', CYRUS['poem_keys_index'], CYRUS['fade_duration']]);
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
            CYRUS['timeout_handle'] = setTimeout(display_poem_loop, queue_entry[2]);
        }
    }
}

