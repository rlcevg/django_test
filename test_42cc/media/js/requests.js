var priority = {
    old_val: 1.0,
    new_val: 1.0,
//  msg = jQuery('#id_req_msg');
//  img = '<img src="{{ settings.SITE_MEDIA_PREFIX }}img/arrow.png" alt="move" width="16" height="16" class="handle" />';
//  input = jQuery('#id_pr_val_' + id);
//  btn = jQuery('#id_req_btn_' + id);
//  tag = jQuery('#id_pr_' + id);
    disableSubmit: function(val) {
        jQuery('input[type="submit"]').attr('disabled', val);
        jQuery('input[type="button"]').attr('disabled', val);
        jQuery('input[type="text"]').attr('disabled', val);
    },
};

function postChanges(id) {
    function invalidateOrderList(order_list) {
        if (typeof order_list == 'object') {
            var list = jQuery('#order_list');
            list.html('');
            for (var i = 0; i < order_list.length; i++) {
                var text = '<li id="listItem_' + order_list[i] + '"> ';
                text += order_list[i] + '</li>';
                list.append(text);
            }
            list.children().prepend(priority.img);
        }
    }

    var disableSubmit = function(val) {
        priority.input.attr('disabled', val);
        priority.btn.attr('disabled', val);
    };

    function form_validations() {
        if (isNaN(priority.new_val)) {
            priority.msg.removeClass().addClass('error').html('Priority is not a numeric value');
            return false;
        }
        return true;
    }

    var text = 'id=' + id + '&priority=' + priority.new_val;
    var options = {
        type: 'post',
        data: text,
        dataType: 'json',
        beforeSend: function() {
            if (typeof form_validations == "function" && !form_validations()) {
                return false;
            }
            priority.disableSubmit(true);
        },
        success: function(json) {
            priority.msg.removeClass().addClass(json.type).html(json.msg).fadeIn('slow');
            priority.disableSubmit(false);

            if (json.type != 'success') {
                text = '<b>' + json.msg + '</b><br />';
                text += '<div class="error">';
                jQuery.each(json.errors, function(key, value) {
                    text += '"' + key + '": ' + value + '<br />';
                });
                text += '</div>';
                priority.msg.html(text);
                priority.tag.html(priority.old_val);
            } else {
                invalidateOrderList(json.order_list);
                //jQuery('input:button[name=req_btn]').attr('disabled', false);
                jQuery('input[type=button]').attr('disabled', false);
                jQuery('input[type=submit]').attr('disabled', false);
                priority.btn.attr('value', 'Edit');
                priority.tag.html(priority.new_val);
            }
        },
    };

    jQuery.ajax(options);
}

function edit_rec(id) {
    priority.input = jQuery('#id_pr_val_' + id);
    priority.btn = jQuery('#id_req_btn_' + id);
    priority.tag = jQuery('#id_pr_' + id);

    if (priority.btn.attr('value') == 'Edit') {
        //jQuery('input:button[name=req_btn]').attr('disabled', true);
        jQuery('input[type=button]').attr('disabled', true);
        jQuery('input[type=submit]').attr('disabled', true);
        priority.btn.attr('disabled', false);
        priority.btn.attr('value', 'Save');
        priority.old_val = priority.tag.html();
        var text = '<input type="text" id="id_pr_val_' + id + '" name="priority" size=4 ';
        text += ' style="text-align: center;" value=' + priority.old_val + '>';
        priority.tag.html(text);
    } else {
        priority.new_val = parseFloat(priority.input.val());
        postChanges(id);
    }
}

function apply_order() {
    var text = jQuery('#id_reorder').attr('name') + '=true&';
    text += jQuery('#order_list').sortable('serialize');
    jQuery.ajax({
        type: 'POST',
        data: text,
        dataType: 'json',
        beforeSend: function() {
            priority.disableSubmit(true);
        },
        success: function() {
            window.location.replace('');
        },
    });
}

function delete_priority() {
    var text = 'delPriority=true';
    var elems = jQuery.find('.ui-selected');
    for (var i = 0; i < elems.length; i++) {
        var matches = jQuery(elems[i]).attr('id').match('(.+)[_](.+)');
        text += '&' + matches[1] + '[]=' + matches[2];
    }
    jQuery.ajax({
        type: 'POST',
        data: text,
        dataType: 'json',
        beforeSend: function() {
            priority.disableSubmit(true);
        },
        success: function() {
            priority.msg.hide();
            priority.disableSubmit(false);
        },
    });
    jQuery('.ui-selected').remove();
}

function add_priority() {
    var val = parseFloat(jQuery('#id_pr_add').val());
    if (isNaN(val)) {
        priority.msg.removeClass().addClass('error').html('Priority is not a numeric value');
        return false;
    }

    var text = 'addPriority=' + val;
    jQuery.ajax({
        type: 'POST',
        data: text,
        dataType: 'json',
        beforeSend: function() {
            priority.disableSubmit(true);
        },
        success: function(json) {
            priority.msg.hide();
            priority.disableSubmit(false);

            if (!json.existed) {
                var list = jQuery('#order_list');
                text = '<li id="listItem_' + val + '">' + priority.img + ' ' + val + '</li>';
                list.append(text);
            }
        },
    });
}

$(document).ready(function() {
    priority.msg = jQuery('#id_req_msg');
    priority.img = '<img src="/site_media/img/arrow.png" alt="move" width="16" height="16" class="handle" />';
    jQuery("#order_list").sortable({
        handle: '.handle',
        cursor: 'move',
    });
    jQuery("#order_list").selectable();

    // setup loading message
    priority.msg.ajaxSend(function() {
        priority.msg.removeClass().addClass('loading').html('Waiting for response...').fadeIn();
    });
});
