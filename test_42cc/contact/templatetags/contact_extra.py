from django import template
from django.db import models
from django.core import urlresolvers
from django.utils.safestring import mark_safe


def edit_link(obj):
    if isinstance(obj, models.Model) and obj.pk:
        object_name = obj.__unicode__()
        url = urlresolvers.reverse(
            'admin:{0}_{1}_change'.format(
                obj._meta.app_label,
                obj._meta.module_name
            ),
            args=(obj.id,)
        )
        return mark_safe(u'Edit <a href="{0}">{1}</a>'.format(
                url, object_name))
    else:
        return ''


register = template.Library()
template.libraries['django.templatetags.contact_extra'] = register
register.simple_tag(edit_link)
