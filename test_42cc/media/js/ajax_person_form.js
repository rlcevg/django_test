function setupAjaxForm(e, form_validations) {
    e.preventDefault();

    var form = jQuery(e.target);
    var form_message = '#' + form.attr('id') + '_msg';

	// en/disable submit button
    var disableSubmit = function(val) {
        for(var i = 0; i < form[0].elements.length; i++) {
            form[0].elements[i].disabled = val;
        }
        toggleCalendarImg(val)
    };

	// setup loading message
    form.ajaxSend(function() {
        $(form_message).removeClass().addClass('loading').html('Loading...').fadeIn();
    });

    var options = {
        type: form.attr('method'),
        data: form.serialize(),
        dataType: 'json',
        beforeSend: function() {
            if(typeof form_validations == "function" && !form_validations()) {
                return false;
            }
            disableSubmit(true);
        },
        success: function(json) {
            $(form_message).hide()
            $(form_message).removeClass().addClass(json.type).html(json.msg).fadeIn('slow');
            disableSubmit(false);

            if(json.type != 'success') {
                var text = '<b>' + json.msg + '</b><br />';
                text += '<div class="error">';
                jQuery.each(json.errors, function(key, value) {
                    text += '"' + key + '": ' + value + '<br />';
                });
                text += '</div>';
                $(form_message).html(text);
            }
        },
        error: function(xhr, ajaxOptions, thrownError){
            // log ajax errors?
        }
    };

    jQuery.ajax(options);
}

$(document).ready(function() {
    jQuery("form#person_frm").submit(function(e) {
        setupAjaxForm(e)
    });
});
