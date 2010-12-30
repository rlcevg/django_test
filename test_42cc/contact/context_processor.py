from django.conf import settings # import the settings file

def add_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        'CURRENT_PATH': settings.CURRENT_PATH,
        'DATABASES': settings.DATABASES,
        'TIME_ZONE': settings.TIME_ZONE,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'SITE_ID': settings.SITE_ID,
        'USE_I18N': settings.USE_I18N,
        'USE_L10N': settings.USE_L10N,
        'MEDIA_ROOT': settings.MEDIA_ROOT,
        'MEDIA_URL': settings.MEDIA_URL,
        'ADMIN_MEDIA_PREFIX': settings.ADMIN_MEDIA_PREFIX,
        'TEMPLATE_LOADERS': settings.TEMPLATE_LOADERS,
        'ROOT_URLCONF': settings.ROOT_URLCONF,
    }
