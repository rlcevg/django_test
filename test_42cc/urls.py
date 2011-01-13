from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('contact.urls')),
    (r'^' + settings.SITE_MEDIA_PREFIX[1:] + '(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': os.path.join(settings.CURRENT_PATH, 'media')}),
    # Example:
    # (r'^test_42cc/', include('test_42cc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
