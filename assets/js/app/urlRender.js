(function ($) {
    $(document).ready(() => {
        var currentURL = window.location.href;
        // console.log(currentURL);
        if (currentURL.includes('?ID')){
            var ID = currentURL.split('?')[1];
            // console.log(ID);
            $('.nav-link').each(function () {
                var _href = $(this).attr('href');
                var newHref = _href + "?" + ID;
                $(this).attr('href', newHref);
                // console.log(newHref);
            });
            $('#setting').each(function(){
                var _href = $(this).attr('href');
                var newHref = _href + "?" + ID;
                $(this).attr('href', newHref);
            })
            $('#settingForm').each(function(){
                var _href = $(this).attr('href');
                var newHref = _href + "?" + ID;
                $(this).attr('href', newHref);
            })
            // console.log($("#form_reservation").length);
            if($("#form_reservation").length > 0){
                // console.log($("#form_reservation").attr('action'));
                // console.log(ID);
                var _href = $("#form_reservation").attr('action');
                var newHref = _href + "?" + ID;
                $("#form_reservation").attr('action', newHref)
            }
        };
        
    });
})(jQuery);