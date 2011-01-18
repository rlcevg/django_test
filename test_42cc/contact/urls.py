from django.conf.urls.defaults import *
from contact.models import Person, HttpRequestLog

person_info = {
    'queryset': Person.objects.all(),
    'object_id': 1,
}

req_info = {
    'template_name': 'contact/requests.html',
}

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_detail', person_info, 'home'),
)

urlpatterns += patterns('contact.views',
    (r'^edit/$', 'edit', person_info, 'editperson'),
    (r'^accounts/logout/$', 'site_logout', {}, 'logout_url'),
    (r'^requests/$', 'requests_view', req_info),
)

urlpatterns += patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contact/login.html'}),
)
