from django.conf import settings  # import the settings file


def add_settings(request):
    return {
        'settings': settings,
        'request': request,
    }
