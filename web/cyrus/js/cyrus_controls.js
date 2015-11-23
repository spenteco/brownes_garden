

function initialize_controls() {
    
    if (CYRUS['interface_state'] == 'running') {
        
        disable_widget('rewind_widget');
        disable_widget('forward_widget');
        enable_widget('pause_widget');
        disable_widget('play_widget');
        
        enable_widget('link_widget');
        enable_widget('github_widget');
        enable_widget('about_widget');
        enable_widget('twitter_widget');
        enable_widget('text_widget');
    }
    
    if (CYRUS['interface_state'] == 'from_url') {
        
        disable_widget('rewind_widget');
        disable_widget('forward_widget');
        disable_widget('pause_widget');
        enable_widget('play_widget');
        
        enable_widget('link_widget');
        enable_widget('github_widget');
        enable_widget('about_widget');
        enable_widget('twitter_widget');
        enable_widget('text_widget');
    }
}

function enable_widget(id) {
    
    $('#' + id).html(
        '<a href="javascript:handleControl(\'' + id + '\');" class="control_a">' + 
        $('#enabled_' + id).html() +
        '</a>'
    );
} 

function disable_widget(id) {
    
    $('#' + id).html($('#disabled_' + id).html());
}

function handleControl(widget) {
    
    if (widget == 'rewind_widget') {
        
        var disable_rewind = false;
        var current_poem_id = '';
        var previous_poem_id = '';
        
        var poems = $('.poem_container');
        
        for (var a = 0; a < poems.length; a++) {
            if ($(poems[a]).css('display') == 'block' || $(poems[a]).css('display') == 'inline') {
                current_poem_id = $(poems[a]).attr('id');
                if (a > 0) {
                    previous_poem_id = $(poems[a - 1]).attr('id');
                }
                if (a == 1) {
                    disable_rewind = true;
                }
            }
        }
        
        if (disable_rewind == true) {
            disable_widget('rewind_widget');
        }
        
        enable_widget('forward_widget');
        
        console.log('current_poem_id', current_poem_id, 'previous_poem_id', previous_poem_id);
        
        $('#' + current_poem_id).css('display', 'none');
        $('#' + previous_poem_id).css('display', 'block');
    }

    if (widget == 'forward_widget') {
        
        var disable_forward = false;
        var current_poem_id = '';
        var next_poem_id = '';
        
        var poems = $('.poem_container');
        
        for (var a = 0; a < poems.length; a++) {
            if ($(poems[a]).css('display') == 'block' || $(poems[a]).css('display') == 'inline') {
                current_poem_id = $(poems[a]).attr('id');
                if (a < poems.length - 1) {
                    next_poem_id = $(poems[a + 1]).attr('id')
                }
                if (a == poems.length - 2) {
                    disable_forward = true;
                }
            }
        }
        
        if (disable_forward == true) {
            disable_widget('forward_widget');
        }
        
        enable_widget('rewind_widget');
        
        $('#' + current_poem_id).css('display', 'none');
        $('#' + next_poem_id).css('display', 'block');
    }

    if (widget == 'pause_widget') {

        CYRUS['interface_state'] = 'paused';
        
        enable_widget('rewind_widget');
        disable_widget('forward_widget');
        
        disable_widget('pause_widget');
        enable_widget('play_widget');
    }

    if (widget == 'play_widget') {
      
        CYRUS['interface_state'] = 'running';
        
        disable_widget('rewind_widget');
        disable_widget('forward_widget');
        enable_widget('pause_widget');
        disable_widget('play_widget');
        
        var current_poem_id = '';
        var previous_poem_id = '';
        var is_at_end = false;
        
        var poems = $('.poem_container');
        
        for (var a = 0; a < poems.length; a++) {
            if ($(poems[a]).css('display') == 'block') {
                current_poem_id = $(poems[a]).attr('id');
                if (a == poems.length - 1) {
                    is_at_end = true;
                }
            }
        }
        
        if (is_at_end == false) {
            $('#' + current_poem_id).fadeOut(CYRUS['fade_duration'])
        }
        
        if (CYRUS['interface_type'] == 'image') {
            display_image_loop();
        }
        
        if (CYRUS['interface_type'] == 'poems') {
            display_poem_loop();
        }
        
        if (CYRUS['interface_type'] == 'quotes') {
            display_quote_loop();
        }
    }

    if (widget == 'link_widget') {
        
        var long_url = current_state.url;
        
        var header_top = $('#page_header').position().top;
        var header_left = $('#page_header').position().left;
        
        $.get('/apps/url/?longUrl=' + encodeURI(long_url), 
            function(short_url) {
                $('#url_popup_message').html('<a class="text_link" href="' + short_url + '">' + short_url + '</a>');
                $('#url_popup_box').css('top', (header_top + 40) + 'px');
                $('#url_popup_box').css('left', (header_left + 140) + 'px');
                $('#url_popup_box').css('display', 'block');
                $('#url_popup_box').css('display', 'block');
            }
        );
    }

    if (widget == 'github_widget') {
        window.open('https://github.com/spenteco/mutableStanzas');
    }

    if (widget == 'about_widget') {
        window.open('/posts/mutablestanzas.html');
    }
    
    if (widget == 'twitter_widget') {
/*        
        var long_url = current_state.url
        
        $.get('/apps/url/?longUrl=' + encodeURI(long_url), 
            function(short_url) {
        
                window.open('https://twitter.com/share?url=' + short_url,'','width=550, height=500, scrollbars=no');
            }
        );
*/
    }

    if (widget == 'text_widget') {
        window.open('https://archive.org/details/hydriotaphiaurne00browuoft');
    }
}

