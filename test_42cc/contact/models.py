from django.db import models
from itertools import chain
from django.core.exceptions import ObjectDoesNotExist
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
    """
    Helper structure for use in html templates.
    To change default value of request's priority add PRIORITY_VAR to request.
    """
    PRIORITY_VAR = 'priorityVal'
    PRIORITY_DEFAULT = 1.0


def getOrderList():
    cnt = PriorityOrder.objects.count()
    if cnt == 0:
        lst = HttpRequestLog.objects.values('priority').\
            annotate(pcount=models.Count('priority'))
        for val in lst:
            obj = PriorityOrder(
                priority=val['priority'],
                pr_order=cnt,
            )
            obj.save()
            cnt += 1

    lst = PriorityOrder.objects.all()
    orderList = [None] * cnt
    for pr in lst:
        orderList[pr.pr_order] = pr.priority
    return orderList


def existedPriority(val):
    try:
        pr_obj = PriorityOrder.objects.get(priority=val)
    except ObjectDoesNotExist:
        pr_obj = PriorityOrder(
            priority=val,
            pr_order=PriorityOrder.objects.count()
        )
        pr_obj.save()
        return False
    return True


def reorderPriority(post):
    if not 'listItem[]' in post:
        return
    order = post.getlist('listItem[]')
    i = 0
    for val in order:
        pr_obj = PriorityOrder.objects.get(priority=val)
        pr_obj.pr_order = i
        pr_obj.save()
        i += 1


def deletePriority(post):
    if not 'listItem[]' in post:
        return
    order = post.getlist('listItem[]')
    for val in order:
        PriorityOrder.objects.get(priority=val).delete()
    lst = PriorityOrder.objects.order_by('pr_order')
    i = 0
    for obj in lst:
        obj.pr_order = i
        obj.save()
        i += 1


class PriorityOrder(models.Model):
    """Dictionary of priorities for HttpRequestLog model"""
    priority = models.FloatField(primary_key=True)
    pr_order = models.IntegerField()


def getOrderedList(order_list, count=10):
    exclude_list = HttpRequestLog.objects.order_by('-datetime')
    ordered_list = []
    for pr_val in order_list:
        filter_list = HttpRequestLog.objects.filter(priority=pr_val).\
            order_by('-datetime')[:count]
        ordered_list = list(chain(ordered_list, filter_list))
        if len(ordered_list) >= count:
            return ordered_list[:count]
        exclude_list = exclude_list.exclude(priority=pr_val)
    return list(chain(ordered_list, exclude_list))[:count]


class HttpRequestLog(models.Model):
    host = models.CharField(max_length=80)
    full_path = models.TextField()
    is_ajax = models.BooleanField()
    is_secure = models.BooleanField()
    method = models.CharField(max_length=4,
        choices=(('GET', 'GET'), ('POST', 'POST')))
    datetime = models.DateTimeField()
    priority = models.FloatField(
        default=PriorityStruct.PRIORITY_DEFAULT,
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
