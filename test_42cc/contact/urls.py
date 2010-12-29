from django.conf.urls.defaults import *
from contact.models import Person, HttpRequestLog

person_info = {
    'queryset': Person.objects.all(),
    'object_id': 1,
}

requestLog_info = {
    'template_name': 'contact/requests.html',
#    'queryset': HttpRequestLog.objects.order_by('datetime')[:10],
    'queryset': HttpRequestLog.objects.all().reverse()[:10],
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_detail', person_info),
    (r'^requests/$', 'django.views.generic.list_detail.object_list', requestLog_info),
)
