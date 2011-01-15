from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import os

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('contact.urls')),
    (r'^' + settings.SITE_MEDIA_PREFIX[1:] + '(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': os.path.join(settings.CURRENT_PATH, 'media')}),
    (r'^admin/', include(admin.site.urls)),
)
