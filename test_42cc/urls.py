from django.conf.urls.defaults import *
from settings import CURRENT_PATH
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('contact.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(CURRENT_PATH, 'media')}),
    # Example:
    # (r'^test_42cc/', include('test_42cc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
