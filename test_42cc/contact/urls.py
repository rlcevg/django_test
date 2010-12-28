from django.conf.urls.defaults import *
from contact.models import Person

info_dict = {
    'queryset': Person.objects.all(),
    'object_id': 1,
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_detail', info_dict),
)
