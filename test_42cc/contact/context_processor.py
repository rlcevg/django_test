from django.conf import settings  # import the settings file
from contact.models import PriorityStruct


def add_settings(request):
    return {
        'settings': settings,
        'request': request,
        'priorityObj': PriorityStruct,
    }
