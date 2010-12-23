from django.db import models
#import datetime

class Person(models.Model):
    firstname = models.CharField(max_length=80)
    lastname = models.CharField(max_length=80)
    biography = models.TextField()
    birth_date = models.DateTimeField()
    signin_date = models.DateTimeField('date signed')

    def __unicode__(self):
        return "{0} {1}".format(self.firstname, self.lastname)


class Contact(models.Model):
    CONTACT_TYPES = (('phone', 'Phone'),
                     ('email', 'E-Mail'),
                     ('icq',   'ICQ'))
    contact_id = models.ForeignKey(Person)
    contact = models.CharField(max_length=20)
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPES)
    contact_info = models.TextField()

    def __unicode__(self):
        return self.contact
