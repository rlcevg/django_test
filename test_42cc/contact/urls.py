from django.conf.urls.defaults import *
from contact.models import Person, HttpRequestLog

person_info = {
    'queryset': Person.objects.all(),
    'object_id': 1,
}

req_info = {
    'template_name': 'contact/requests.html',
    'queryset': HttpRequestLog.objects.order_by('-datetime')[:10],
}

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_detail', person_info,
        'home'),
    (r'^requests/$', 'object_list', req_info),
)

urlpatterns += patterns('',
    (r'^edit/$', 'contact.views.edit', person_info, 'editperson'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contact/login.html'}),
    (r'^accounts/logout/$', 'contact.views.site_logout', {}, 'logout_url'),
)
