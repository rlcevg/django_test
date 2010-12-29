from django.conf.urls.defaults import *
from contact.models import Person, HttpRequestLog

person_info = {
    'queryset': Person.objects.all(),
    'object_id': 1,
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_detail', person_info),
    (r'^requests/$', 'contact.views.process_requests'),
)
