from django.db import models


class Person(models.Model):
    firstname = models.CharField(max_length=80)
    lastname = models.CharField(max_length=80)
    biography = models.TextField()
    birth_date = models.DateField()
    signin_date = models.DateTimeField('date signed')

    def __unicode__(self):
        return "{0} {1}".format(self.firstname, self.lastname)


class Contact(models.Model):
    CONTACT_TYPES = (('phone', 'Phone'),
                     ('email', 'E-Mail'),
                     ('icq',   'ICQ'))
    person = models.ForeignKey(Person)
    contact = models.CharField(max_length=20)
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPES,
            default='email')
    contact_info = models.TextField()

    def __unicode__(self):
        return "{0}: {1}".format(self.get_contact_type_display(), self.contact)


class HttpRequestLog(models.Model):
    host = models.CharField(max_length=80)
    full_path = models.TextField()
    is_ajax = models.BooleanField()
    is_secure = models.BooleanField()
    method = models.CharField(max_length=4)
    datetime = models.DateTimeField()

    def __unicode__(self):
        return self.host + " " + self.full_path
