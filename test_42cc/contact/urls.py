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

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_detail', person_info,
        'home'),
    (r'^requests/$', 'django.views.generic.list_detail.object_list', req_info),
    (r'^edit/$', 'contact.views.edit', person_info),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'contact/login.html'})
)
