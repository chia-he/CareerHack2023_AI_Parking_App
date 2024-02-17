(function($) {
    "use strict"; // Start of use strict
    $('.custom-select').change(function(){
        if($(this).val()=='staff'){
            $('#option1').hide();
            $('#option2').show();
        }
        else if($(this).val()=='vip'){
            $('#option2').hide();
            $('#option1').show();
        };
    });

})(jQuery);