from django import template
from django.core import urlresolvers
from django.utils.safestring import mark_safe


def do_edit_link(parser, token):
    try:
        tag_name, object_link = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError,\
            "%r tag requires exactly two arguments" % token.contents.split()[0]
    return ResolveLinkNode(object_link)


class ResolveLinkNode(template.Node):
    def __init__(self, object_link):
        self.object_link = template.Variable(object_link)

    def render(self, context):
        try:
            obj = self.object_link.resolve(context)
            class_name = obj.__class__.__name__.lower()
            object_name = obj.__unicode__()
            url = urlresolvers.reverse(
                'admin:contact_' + class_name + '_change', args=(obj.id,)
            )
            return mark_safe(u'<a href="' + url + '">' + object_name + '</a>')
        except template.VariableDoesNotExist:
            return ''


register = template.Library()
template.libraries['django.templatetags.contact_extra'] = register
register.tag(name='edit_link', compile_function=do_edit_link)
