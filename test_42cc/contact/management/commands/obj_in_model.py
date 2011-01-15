from django.core.management.base import NoArgsCommand
from django.db import models


class Command(NoArgsCommand):
    help = 'Django command that prints all project models and the count of '\
            'objects in every model'

    def handle_noargs(self, **options):
        self.stdout.write('Total count of objects in:\n'.format())
        for model in models.get_models():
            self.stdout.write('{0}.{1}:  {2}\n'.format(
                    model.__module__,
                    model.__name__,
                    model._default_manager.count(),
                ))
