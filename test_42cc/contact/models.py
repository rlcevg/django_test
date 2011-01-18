from django.db import models
#from django.contrib.auth.models import User


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


class PriorityStruct(object):
    PRIORITY_VAR = 'priorityVal'
    PRIORITY_HIGH = 0
    PRIORITY_MEDIUM = 1
    PRIORITY_LOW = 2
    PRIORITY_TYPES = (
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_LOW, 'Low'),
    ) 


class HttpRequestLog(models.Model):
    host = models.CharField(max_length=80)
    full_path = models.TextField()
    is_ajax = models.BooleanField()
    is_secure = models.BooleanField()
    method = models.CharField(max_length=4)
    datetime = models.DateTimeField()
    priority = models.SmallIntegerField(
        choices=PriorityStruct.PRIORITY_TYPES,
        default=PriorityStruct.PRIORITY_MEDIUM,
    )

    def __unicode__(self):
        return self.host + " " + self.full_path


class ActionDBModel(models.Model):
    ACTION_CREATE = 0
    ACTION_EDIT = 1
    ACTION_DELETE = 2
    ACTION_TYPES = (
        (ACTION_CREATE, 'Create'),
        (ACTION_EDIT, 'Edit'),
        (ACTION_DELETE, 'Delete')
    )
    model = models.CharField(max_length=100)
    action = models.SmallIntegerField(choices=ACTION_TYPES)
    time = models.DateTimeField()
#    user = models.ForeignKey(User)


from signal_processor import start_signal_processor
start_signal_processor()
