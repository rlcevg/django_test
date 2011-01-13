from django.forms import DateInput
from django.utils.safestring import mark_safe
from django.conf import settings


class CalendarWidget(DateInput):
    class Media:
        css = {
            'all': (
                settings.SITE_MEDIA_PREFIX + 'css/jquery-ui.css',
                settings.SITE_MEDIA_PREFIX + 'css/calendar.css',
            )
        }
        js = (
            settings.SITE_MEDIA_PREFIX + 'js/jquery.min.js',
            settings.SITE_MEDIA_PREFIX + 'js/jquery-ui.min.js',
            settings.SITE_MEDIA_PREFIX + 'js/calendar.js',
        )

    def __init__(self, attrs={}, format=None):
        super(CalendarWidget, self).__init__(attrs={
                'class': 'vDateField',
                'size': '10'
            }, format=format)
        self.cw_attrs = attrs

    def render(self, name, value, attrs=None):
        output = super(DateInput, self).render(name, value, attrs)
        if 'img' in self.cw_attrs:
            output = mark_safe(u'''<img class="calendar" src="{0}" \
alt="Calendar">'''.format(self.cw_attrs['img'])) + output

        return output
