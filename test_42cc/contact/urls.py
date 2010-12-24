from django.conf.urls.defaults import *
from contact.models import Person

info_dict = {
    'queryset': Person.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
)
