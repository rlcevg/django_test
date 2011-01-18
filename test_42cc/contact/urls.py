from django.conf.urls.defaults import *
from contact.models import Person

person_info = {
    'queryset': Person.objects.all(),
    'object_id': 1,
}

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_detail', person_info, 'home'),
)

urlpatterns += patterns('contact.views',
    (r'^edit/$', 'edit', person_info, 'editperson'),
    (r'^accounts/logout/$', 'site_logout', {}, 'logout_url'),
    (r'^requests/$', 'requests_view', {}, 'request_home'),
    (r'^requests/(?P<priority>\d+)/$', 'requests_view'),
)

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contact/login.html'}),
)
