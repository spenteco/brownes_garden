
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


var CYRUS = {
    'full_image_list': [['bands/', '20.svg'], ['bands/', '27.svg'], ['bands/', '25.svg'], ['bands/', '28.svg'], ['bands/', '22.svg'], ['bands/', '8.svg'], ['bands/', '13.svg'], ['bands/', '5.svg'], ['bands/', '16.svg'], ['bands/', '21.svg'], ['bands/', '2.svg'], ['bands/', '14.svg'], ['bands/', '3.svg'], ['bands/', '1.svg'], ['bands/', '15.svg'], ['bands/', '26.svg'], ['bands/', '23.svg'], ['bands/', '7.svg'], ['bands/', '24.svg'], ['bands/', '9.svg'], ['bands/', '17.svg'], ['bands/', '4.svg'], ['bands/', '19.svg'], ['bands/', '11.svg'], ['bands/', '12.svg'], ['bands/', '10.svg'], ['bands/', '18.svg'], ['four_square/', '20.svg'], ['four_square/', '22.svg'], ['four_square/', '8.svg'], ['four_square/', '13.svg'], ['four_square/', '5.svg'], ['four_square/', '16.svg'], ['four_square/', '21.svg'], ['four_square/', '2.svg'], ['four_square/', '14.svg'], ['four_square/', '1.svg'], ['four_square/', '15.svg'], ['four_square/', '23.svg'], ['four_square/', '9.svg'], ['four_square/', '17.svg'], ['four_square/', '6.svg'], ['four_square/', '11.svg'], ['four_square/', '12.svg'], ['four_square/', '10.svg'], ['four_square/', '18.svg'], ['one_square/', '20a.svg'], ['one_square/', '14c.svg'], ['one_square/', '14a.svg'], ['one_square/', '8a.svg'], ['one_square/', '1a.svg'], ['one_square/', '12c.svg'], ['one_square/', '15d.svg'], ['one_square/', '12b.svg'], ['one_square/', '10a.svg'], ['one_square/', '15a.svg'], ['one_square/', '22a.svg'], ['one_square/', '13b.svg'], ['one_square/', '20d.svg'], ['one_square/', '17b.svg'], ['one_square/', '9d.svg'], ['one_square/', '8b.svg'], ['one_square/', '9b.svg'], ['one_square/', '18b.svg'], ['one_square/', '21a.svg'], ['one_square/', '13a.svg'], ['one_square/', '8d.svg'], ['one_square/', '18c.svg'], ['one_square/', '14b.svg'], ['one_square/', '17c.svg'], ['one_square/', '21c.svg'], ['one_square/', '23c.svg'], ['one_square/', '22d.svg'], ['one_square/', '16d.svg'], ['one_square/', '3.svg'], ['one_square/', '21d.svg'], ['one_square/', '12d.svg'], ['one_square/', '20b.svg'], ['one_square/', '13d.svg'], ['one_square/', '15c.svg'], ['one_square/', '9c.svg'], ['one_square/', '9a.svg'], ['one_square/', '14d.svg'], ['one_square/', '11d.svg'], ['one_square/', '11b.svg'], ['one_square/', '7.svg'], ['one_square/', '11a.svg'], ['one_square/', '22c.svg'], ['one_square/', '16c.svg'], ['one_square/', '18a.svg'], ['one_square/', '16a.svg'], ['one_square/', '11c.svg'], ['one_square/', '21b.svg'], ['one_square/', '17d.svg'], ['one_square/', '13c.svg'], ['one_square/', '23a.svg'], ['one_square/', '23b.svg'], ['one_square/', '10b.svg'], ['one_square/', '12a.svg'], ['one_square/', '4.svg'], ['one_square/', '22b.svg'], ['one_square/', '16b.svg'], ['one_square/', '1b.svg'], ['one_square/', '20c.svg'], ['one_square/', '8c.svg'], ['one_square/', '19.svg'], ['one_square/', '23d.svg'], ['one_square/', '15b.svg'], ['one_square/', '17a.svg'], ['one_square/', '18d.svg'], ['aviation/', 'RIGHT_funeral.jefferson_aviation.svg'], ['aviation/', 'LEFT_locomotive.churchill_aviation.svg'], ['aviation/', 'RIGHT_armstrong.churchill_aviation.svg'], ['aviation/', 'RIGHT_foundry.jefferson_aviation.svg'], ['aviation/', 'LEFT_bunker_hill.flowers_aviation.svg'], ['aviation/', 'RIGHT_foundry.flowers_aviation.svg'], ['aviation/', 'RIGHT_armstrong.jefferson_aviation.svg'], ['aviation/', 'LEFT_funeral.flowers_aviation.svg'], ['aviation/', 'RIGHT_bunker_hill.churchill_aviation.svg'], ['aviation/', 'RIGHT_bunker_hill.flowers_aviation.svg'], ['aviation/', 'LEFT_armstrong.jefferson_aviation.svg'], ['aviation/', 'RIGHT_locomotive.jefferson_aviation.svg'], ['aviation/', 'RIGHT_funeral.churchill_aviation.svg'], ['aviation/', 'LEFT_foundry.churchill_aviation.svg'], ['aviation/', 'RIGHT_bunker_hill.jefferson_aviation.svg'], ['aviation/', 'LEFT_armstrong.churchill_aviation.svg'], ['aviation/', 'LEFT_armstrong.flowers_aviation.svg'], ['aviation/', 'LEFT_funeral.jefferson_aviation.svg'], ['aviation/', 'LEFT_foundry.flowers_aviation.svg'], ['aviation/', 'RIGHT_grissom.flowers_aviation.svg'], ['aviation/', 'RIGHT_foundry.churchill_aviation.svg'], ['aviation/', 'LEFT_funeral.churchill_aviation.svg'], ['aviation/', 'RIGHT_armstrong.flowers_aviation.svg'], ['aviation/', 'LEFT_bunker_hill.churchill_aviation.svg'], ['aviation/', 'RIGHT_locomotive.churchill_aviation.svg'], ['aviation/', 'LEFT_foundry.jefferson_aviation.svg'], ['aviation/', 'LEFT_locomotive.flowers_aviation.svg'], ['aviation/', 'LEFT_bunker_hill.jefferson_aviation.svg'], ['aviation/', 'RIGHT_funeral.flowers_aviation.svg'], ['aviation/', 'RIGHT_grissom.jefferson_aviation.svg'], ['aviation/', 'RIGHT_grissom.churchill_aviation.svg'], ['aviation/', 'RIGHT_locomotive.flowers_aviation.svg'], ['aviation/', 'LEFT_locomotive.jefferson_aviation.svg']],
    'image_list': [],
    'query_string_parameters': '',
    'image_list_index': -1,
    'interface_state': 'running',
    'timer_queue': [],
    'timeout_interval': 3000,
    'timeout_handle': '',
    'fade_duration': 250,
    'interface_type': 'image',
};


$(document).ready(
    function() {
        
        initialize_controls();
        
        CYRUS['query_string_parameters'] = get_query_string_parameters();
        
        if (CYRUS['query_string_parameters']['type'] == undefined) {
            CYRUS['image_list'] = CYRUS['full_image_list'];
        }
        else {
            for (var a = 0; a < CYRUS['full_image_list'].length; a++) {
                if (CYRUS['full_image_list'][a][0].indexOf(CYRUS['query_string_parameters']['type']) != -1) {
                    CYRUS['image_list'].push(CYRUS['full_image_list'][a]);
                }
            }
        }
        
        if (CYRUS['query_string_parameters']['process'] == 'random') {
            CYRUS['image_list'].shuffle();
        }
        
        CYRUS['image_list_index'] = -1;
        
        display_image_loop();
    }
);

function display_image_loop() {
    
    var previous_image_list_index = CYRUS['image_list_index'];
    
    CYRUS['image_list_index'] = CYRUS['image_list_index'] += 1
    
    if (CYRUS['image_list_index'] > CYRUS['image_list'].length - 1) {
        CYRUS['image_list_index'] = 0;
        if (CYRUS['query_string_parameters']['process'] == 'random') {
            CYRUS['image_list'].shuffle();
        }
    }
    
    $('#image_container').append('<img class="poem_container" id="svg_image_' + CYRUS['image_list_index'] + '" src="svg/' +  CYRUS['image_list'][CYRUS['image_list_index']][0] + CYRUS['image_list'][CYRUS['image_list_index']][1] + '"/>');

    if (previous_image_list_index != -1) {
        CYRUS['timer_queue'].push(['fadeOut', previous_image_list_index, CYRUS['fade_duration']]);
    }
        
    CYRUS['timer_queue'].push(['fadeIn', CYRUS['image_list_index'], CYRUS['fade_duration']]);
    CYRUS['timer_queue'].push(['setTimeout', -1, CYRUS['timeout_interval']]);

    handle_timer_queue();
}

function handle_timer_queue() {

    if (CYRUS['interface_state'] == 'running') {

        var queue_entry = CYRUS['timer_queue'].shift();

        if (queue_entry[0] == 'fadeOut') {
            $('#svg_image_' + queue_entry[1]).fadeOut(queue_entry[2]);
            CYRUS['timeout_handle'] = setTimeout(handle_timer_queue, queue_entry[2]);
        }

        if (queue_entry[0] == 'fadeIn') {
            $('#svg_image_' + queue_entry[1]).fadeIn(queue_entry[2]);
            CYRUS['timeout_handle'] = setTimeout(handle_timer_queue, queue_entry[2]);
        }

        if (queue_entry[0] == 'setTimeout') {
            CYRUS['timeout_handle'] = setTimeout(display_image_loop, queue_entry[2]);
        }
    }
}
