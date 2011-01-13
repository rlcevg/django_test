$(function() {
    $.datepicker.setDefaults({
        showOn: 'both',
        buttonImageOnly: true,
        buttonImage: '/site_media/img/icon_calendar.gif',
        buttonText: 'Calendar',
        dateFormat: 'yy-mm-dd',
        firstDay: 1
    });
    $('.vDateField').datepicker($.datepicker.regional['ua']);
});

function toggleCalendarImg(val) {
    $('.vDateField').datepicker('option', 'showOn', val ? 'focus' : 'both');
}
