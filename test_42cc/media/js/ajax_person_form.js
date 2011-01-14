function setupAjaxForm(e, form_validations) {
    e.preventDefault();

    var form = jQuery(e.target);
    var form_message = '#' + form.attr('id') + '_msg';

	// en/disable submit button
    var disableSubmit = function(val) {
        $('#logout_btn').attr('disabled', val);
        $('form#reverse_frm input[type="submit"]').attr('disabled', val);
        for (var i = 0; i < form[0].elements.length; i++) {
            form[0].elements[i].disabled = val;
        }
        toggleCalendarImg(val);
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
            if (typeof form_validations == "function" && !form_validations()) {
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

function setupReverseForm(e) {
    e.preventDefault();

    var $table = $('#bio_info_tbl');
    var rows = $table.find('tbody > tr').get();
    for (var i = rows.length; i > 0; i--) {
        $table.children('tbody').append(rows[i-1]);
    }
}

$(document).ready(function() {
    //these two line adds the color to each different row
    $("#mytable tbody tr:even").addClass("eventr");
    $("#mytable tbody tr:odd").addClass("oddtr");
    //handle the mouseover , mouseout and click event
    $("#mytable tbody tr").mouseover(function() {$(this).addClass("trover");}).
        mouseout(function() {$(this).removeClass("trover");});
        //.click(function() {$(this).toggleClass("trclick");});
    jQuery("form#person_frm").submit(function(e) {
        setupAjaxForm(e);
    });
    jQuery("form#reverse_frm").submit(function(e) {
        setupReverseForm(e);
    });
});
