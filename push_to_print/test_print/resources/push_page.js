
$(document).ready(
    function() {
/*
        var desired_width = 350;
        var desired_height = 525;
        var desired_ratio = desired_width / desired_height;
        
        $('img').each(
            function() {
            
                var w = $(this).width();
                var h = $(this).height();
                
                var scale_factor = desired_height / h;
                if ((w / h) > desired_ratio) {
                    scale_factor = desired_width / w;
                }
                
                var new_w = w * scale_factor;
                var new_h = h * scale_factor;
                
                $(this).css({'width': new_w, 'height': new_h});
            }
        );
        
        alert('Done!');
/*
    }
);

/*
$('body').imagesLoaded( function() {
    
    console.log('loaded');
    
    var desired_width = 350;
    var desired_height = 525;
    var desired_ratio = desired_width / desired_height;
    
    $('img').each(
        function() {
        
            var w = $(this).width();
            var h = $(this).height();
            
            var scale_factor = desired_height / h;
            if ((w / h) > desired_ratio) {
                scale_factor = desired_width / w;
            }
            
            var new_w = w * scale_factor;
            var new_h = h * scale_factor;
            
            $(this).css({'width': new_w, 'height': new_h});
            
            console.log('fixing', $(this).attr('src'));
        }
    );
    
    alert('Done!');
});
*/
