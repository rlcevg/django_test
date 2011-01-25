from django.test import TestCase
from contact import models, signal_processor
from django.conf import settings
from contact.widgets import CalendarWidget
from django import forms, template
from datetime import date
from django.test import Client
from contact.forms import PersonForm
from django.core import urlresolvers, management
import sys
from StringIO import StringIO
from django.db.models.signals import post_save, post_delete


class PersonContactTest(TestCase):
    def setUp(self):
        self.person = models.Person.objects.create(
            firstname='Bob',
            biography='need to get a job',
            lastname='Solnyshko',
            birth_date='2012-01-01',
            signin_date='2010-12-07',)
        self.c1 = models.Contact.objects.create(
            person=self.person,
            contact_type='phone',
            contact='(097)979-797-22',
            contact_info='home number')
        self.c2 = models.Contact.objects.create(
            person=self.person,
            contact_type='email',
            contact='rlcevg@gamal.com',
            contact_info='')

    def test_person(self):
        self.assertEqual(self.person.firstname, 'Bob')
        self.assertNotEqual(self.person.lastname, 'Krasnoe')
        self.assertEqual(self.person.lastname, 'Solnyshko')
        self.assertEqual(unicode(self.person), 'Bob Solnyshko')
        self.assertEqual(self.person.birth_date, '2012-01-01')
        self.assertEqual(self.person.signin_date, '2010-12-07')
        self.assertNotEqual(self.person.biography, '')

    def test_c1(self):
        self.assertEqual(unicode(self.c1), 'Phone: (097)979-797-22')
        self.assertEqual(self.c1.person.pk, self.person.pk)
        self.assertEqual(self.c1.contact_type, 'phone')
        self.assertEqual(self.c1.contact, '(097)979-797-22')
        self.assertEqual(self.c1.contact_info, 'home number')

    def test_c2(self):
        self.assertEqual(unicode(self.c2), 'E-Mail: rlcevg@gamal.com')
        self.assertEqual(self.c2.person.pk, self.person.pk)
        self.assertEqual(self.c2.contact_type, 'email')
        self.assertEqual(self.c2.contact, 'rlcevg@gamal.com')
        self.assertEqual(self.c2.contact_info, '')


class ViewTest(TestCase):
    def test_view(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/requests/')
        self.failUnlessEqual(response.status_code, 200)


class HttpRequestLogTest(TestCase):
    def test_request(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        requestLog = models.HttpRequestLog.objects.get()
        self.assertNotEqual(requestLog.host, '')
        self.assertEqual(requestLog.full_path, '/')
        self.assertEqual(requestLog.method, 'GET')
        response = self.client.get('/requests/')
        self.failUnlessEqual(response.status_code, 200)
        requestLog = models.HttpRequestLog.objects.all()[1]
        self.assertEqual(requestLog.full_path, '/requests/')
        self.assertEqual(requestLog.method, 'GET')
        self.assertTemplateUsed(response, "contact/requests.html")
        self.assertTemplateUsed(response, 'base.html')


class ContextProcessorTest(TestCase):
    def test_context_processor(self):
        response = self.client.get('/requests/')
        self.assertEqual(response.context['settings'], settings)
        self.assertEqual(response.context['settings'].DEBUG,
                settings.DEBUG)
        self.assertEqual(response.context['settings'].ROOT_URLCONF,
                settings.ROOT_URLCONF)


class FormsTest(TestCase):
    def test_valid_form(self):
        "POST valid data to a form"
        post_data = {
            'biography': 'Hello World',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'a': '------------',
            'button_logout': '',
        }
        response = self.client.post('/edit/', post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/edit/')


class AuthTest(TestCase):
    fixtures = ['initial_data.json']

    def test_view_with_login(self):
        # Get the page without logging in. Should result in 302.
        response = self.client.get('/edit/')
        self.assertRedirects(response, '/accounts/login/?next=/edit/')

        # Log in
        login = self.client.login(username='login', password='password')
        self.failUnless(login, 'Could not log in')

        # Request a page that requires a login
        response = self.client.get('/edit/')
        self.assertEqual(response.status_code, 200)


class CalendarWidgetTest(TestCase):
    def test_dateField_with_inputformat(self):
        "DateFields with manually specified input formats"
        f = forms.DateField(input_formats=["%d.%m.%Y", "%d-%m-%Y"],
                widget=CalendarWidget)
        # Parse a date in an unaccepted format; get an error
        self.assertRaises(forms.ValidationError, f.clean, '2010-12-21')

        # Parse a date in a valid format, get a parsed result
        result = f.clean('21.12.2010')
        self.assertEqual(result, date(2010, 12, 21))

        # Check that the parsed result does a round trip to the same format
        text = f.widget._format_value(result)
        self.assertEqual(text, "2010-12-21")

        # Parse a date in a valid format, get a parsed result
        result = f.clean('21-12-2010')
        self.assertEqual(result, date(2010, 12, 21))

        # Check that the parsed result does a round trip to default format
        text = f.widget._format_value(result)
        self.assertEqual(text, "2010-12-21")

        self.assertRaises(forms.ValidationError, f.clean, '2010/12/21')

        class GetDate(forms.Form):
            mydate = forms.DateField(widget=CalendarWidget)

        a = GetDate({'mydate': '2008/4/1'})
        self.assertFalse(a.is_valid())

        a = GetDate({'mydate': '2008-4-1'})
        self.assertTrue(a.is_valid())
        self.assertEqual(a.cleaned_data['mydate'], date(2008, 4, 1))
        self.assertEqual(a['mydate'].as_hidden(), '<input type="hidden" \
name="mydate" value="2008-4-1" id="id_mydate" />')

    def test_calendarWidget(self):
        w = CalendarWidget()
        self.assertEqual(w.render('mydate', '1940-10-09'),
            """<input value="1940-10-09" type="text" class="vDateField" \
name="mydate" size="10" />""")

    def test_calendarWidget_img(self):
        img = settings.SITE_MEDIA_PREFIX + 'img/icon_calendar.gif'
        w = CalendarWidget(attrs={
            'img': img,
        })
        self.assertEqual(w.render('mydate', '1940-10-09'),
            """<img class="calendar" src="{0}" alt="Calendar">\
<input value="1940-10-09" type="text" class="vDateField" \
name="mydate" size="10" />""".format(img))


class AJAX_SubmitTest(TestCase):
    def test_ajax_submit(self):
        c = Client()
        c.login(username='login', password='password')

        # Extra parameters to make this a Ajax style request.
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        # A valid data
        post_data = {
            'contact_set-TOTAL_FORMS': 0,
            'contact_set-INITIAL_FORMS': 0,
            'contact_set-MAX_NUM_FORMS': 0,
            'biography': 'Hello World',
            'firstname': 'firstname',
            'lastname': 'lastname',
            'birth_date': '1940-10-09',
        }
        response = c.post('/edit/', post_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('type' in response.content)
        self.assertTrue('"type": "success"' in response.content)
        self.assertFalse('errors' in response.content)

        # A invalid data - birthday (date) doesn't exist
        post_data = {
            'contact_set-TOTAL_FORMS': 0,
            'contact_set-INITIAL_FORMS': 0,
            'contact_set-MAX_NUM_FORMS': 0,
            'birth_date': '1940-10-0999',
        }
        response = c.post('/edit/', post_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('type' in response.content)
        self.assertTrue('"type": "error"' in response.content)
        self.assertTrue('errors' in response.content)
        self.assertTrue('"birth_date": "Enter a valid date."' in
                response.content)


class ReversedFieldsTest(TestCase):
    def test_order(self):
        f = PersonForm()
        self.assertFalse(f.is_reversed)
        self.assertEqual(f.as_table(), """<tr><th><label for="id_firstname">\
Firstname:</label></th><td><input id="id_firstname" type="text" \
name="firstname" maxlength="80" /></td></tr>
<tr><th><label for="id_lastname">Lastname:</label></th><td><input \
id="id_lastname" type="text" name="lastname" maxlength="80" /></td></tr>
<tr><th><label for="id_biography">Biography:</label></th><td><textarea \
id="id_biography" rows="10" cols="80" name="biography"></textarea></td></tr>
<tr><th><label for="id_birth_date">Birth date:</label></th><td><img \
class="calendar" src="/site_media/img/baloon_24.png" alt="Calendar"><input \
id="id_birth_date" type="text" class="vDateField" name="birth_date" size="10" \
/></td></tr>""")
        f.reverseOrder(True)
        self.assertTrue(f.is_reversed)
        self.assertEqual(f.as_table(), """<tr><th><label for="id_birth_date">\
Birth date:</label></th><td><img class="calendar" src="/site_media/img/\
baloon_24.png" alt="Calendar"><input id="id_birth_date" type="text" \
class="vDateField" name="birth_date" size="10" /></td></tr>
<tr><th><label for="id_biography">Biography:</label></th><td><textarea \
id="id_biography" rows="10" cols="80" name="biography"></textarea></td></tr>
<tr><th><label for="id_lastname">Lastname:</label></th><td><input \
id="id_lastname" type="text" name="lastname" maxlength="80" /></td></tr>
<tr><th><label for="id_firstname">Firstname:</label></th><td><input \
id="id_firstname" type="text" name="firstname" maxlength="80" /></td></tr>""")


class TemplateTagTest(TestCase):
    def test_templatetag(self):
        #Test valid data
        p = models.Person(
            firstname="Any",
            lastname="Object",
            birth_date="2010-12-07",
            signin_date="2010-12-07")
        t = template.Template('{% load contact_extra %}{% edit_link person %}')
        c = template.Context({"person": p})
        self.assertEqual(t.render(c), '')
        p.save()
        text = 'Edit <a href="' +\
            urlresolvers.reverse(
                'admin:contact_' + p.__class__.__name__.lower() + '_change',
                args=(p.id,)
            ) + '">' + p.__unicode__() + '</a>'
        self.assertEqual(t.render(c), text)


class CommandTest(TestCase):
    def test_command(self):
        _stdout = sys.stdout
        sys.stdout = StringIO()
        management.call_command('obj_in_model')
        result = sys.stdout.getvalue()
        sys.stdout = _stdout
        self.assertTrue('Person (fields: 6' in result)


class ActionDBModelTest(TestCase):
    def setUp(self):
        models.Person.objects.all().delete()
        models.Contact.objects.all().delete()
        models.ActionDBModel.objects.all().delete()

    def test_action(self):
        post_save.connect(
            signal_processor.model_action_save,
            dispatch_uid=signal_processor.ACTION_DB_UNIQUE_ID
        )
        post_delete.connect(
            signal_processor.model_action_delete,
            dispatch_uid=signal_processor.ACTION_DB_UNIQUE_ID
        )

        self.assertEqual(models.ActionDBModel.objects.count(), 0)
        self.person = models.Person.objects.create(
            firstname='Bob',
            biography='need to get a job',
            lastname='Job',
            birth_date='2012-01-01',
            signin_date='2010-12-07',)
        self.assertEqual(models.ActionDBModel.objects.count(), 1)

        action = models.ActionDBModel.objects.get()
        self.assertEqual(action.model, '{0}.{1}'.format(
            models.Person.__module__, models.Person.__name__
        ))
        self.assertEqual(action.action, models.ActionDBModel.ACTION_CREATE)

        self.contact = models.Contact(
            person=self.person,
            contact_type='phone',
            contact='(097)979-797-22',
            contact_info='home number'
        )
        self.assertEqual(models.ActionDBModel.objects.count(), 1)
        self.contact.save()
        self.assertEqual(models.ActionDBModel.objects.count(), 2)

        action = models.ActionDBModel.objects.all()[1]
        self.assertEqual(action.model, '{0}.{1}'.format(
            models.Contact.__module__, models.Contact.__name__
        ))
        self.assertEqual(action.action, models.ActionDBModel.ACTION_CREATE)

        self.contact.contact_info = 'changed number'
        self.assertEqual(models.ActionDBModel.objects.count(), 2)
        self.contact.save()
        self.assertEqual(models.ActionDBModel.objects.count(), 3)

        action = models.ActionDBModel.objects.all()[2]
        self.assertEqual(action.model, '{0}.{1}'.format(
            models.Contact.__module__, models.Contact.__name__
        ))
        self.assertEqual(action.action, models.ActionDBModel.ACTION_EDIT)

        self.contact = models.Contact.objects.get()
        self.assertEqual(models.ActionDBModel.objects.count(), 3)
        self.contact.delete()
        self.assertEqual(models.ActionDBModel.objects.count(), 4)

        action = models.ActionDBModel.objects.all()[3]
        self.assertEqual(action.model, '{0}.{1}'.format(
            models.Contact.__module__, models.Contact.__name__
        ))
        self.assertEqual(action.action, models.ActionDBModel.ACTION_DELETE)

        post_delete.disconnect(
            signal_processor.model_action_delete,
            dispatch_uid=signal_processor.ACTION_DB_UNIQUE_ID
        )

        self.assertEqual(models.ActionDBModel.objects.count(), 4)
        self.person.delete()
        self.assertEqual(models.ActionDBModel.objects.count(), 4)


class PriorityFeatureTest(TestCase):
    def test_priority(self):
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        #Test basic feature
        post_data = {}
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, 200)
        p = models.HttpRequestLog.objects.get()
        self.assertEqual(p.priority, models.PriorityStruct.PRIORITY_DEFAULT)

        #Test clear requests feature
        post_data = {
            'clear_btn': 1,
        }
        response = self.client.post('/requests/', post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.HttpRequestLog.objects.count(), 0)

        #Test add priority feature
        post_data = {
            'addPriority': 0.8,
        }
        response = self.client.post('/requests/', post_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PriorityOrder.objects.count(), 2)
        post_data['addPriority'] = 0.6
        response = self.client.post('/requests/', post_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PriorityOrder.objects.count(), 3)

        #Test reorder priority feature
        pr = models.PriorityOrder.objects.get(priority=1.0)
        self.assertEqual(pr.pr_order, 0)
        pr = models.PriorityOrder.objects.get(priority=0.8)
        self.assertEqual(pr.pr_order, 1)
        pr = models.PriorityOrder.objects.get(priority=0.6)
        self.assertEqual(pr.pr_order, 2)
        post_data = {
            'reorder': 1,
            'listItem[]': [u'0.6', u'1.0', u'0.8'],
        }
        response = self.client.post('/requests/', post_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        pr = models.PriorityOrder.objects.get(priority=1.0)
        self.assertEqual(pr.pr_order, 1)
        pr = models.PriorityOrder.objects.get(priority=0.8)
        self.assertEqual(pr.pr_order, 2)
        pr = models.PriorityOrder.objects.get(priority=0.6)
        self.assertEqual(pr.pr_order, 0)

        #Test change existing request's priority feature
        req = models.HttpRequestLog.objects.all()[0]
        post_data = {
            'id': req.id,
            'priority': 0.7,
        }
        response = self.client.post('/requests/', post_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        pr = models.PriorityOrder.objects.get(priority=0.7)
        self.assertEqual(pr.pr_order, 3)
        req = models.HttpRequestLog.objects.get(pk=req.id)
        self.assertEqual(req.priority, 0.7)

        #Test delete priority feature
        post_data = {
            'delPriority': 1,
            'listItem[]': [u'0.6', u'0.7'],
        }
        response = self.client.post('/requests/', post_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PriorityOrder.objects.count(), 2)
        pr = models.PriorityOrder.objects.get(priority=1.0)
        self.assertEqual(pr.pr_order, 0)
        pr = models.PriorityOrder.objects.get(priority=0.8)
        self.assertEqual(pr.pr_order, 1)

        #Test clone template (filter) feature
        self.assertEqual(models.HttpRequestLog.objects.filter(priority=2.0).\
            count(), 0)
        post_data = {
            'clone': 1,
            'host': u'testserver',
            'full_path': u'/requests/',
            'method': u'POST',
            'is_ajax': True,
            'is_secure': False,
            'priority': 2.0,
        }
        response = self.client.post('/requests/', post_data, **kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(models.PriorityOrder.objects.count(), 3)
        self.assertTrue(models.HttpRequestLog.objects.filter(priority=2.0).\
            count() > 0)

        #Test ASC/DESC feature
        post_data = {
            'sortPriority': 1,
        }
        response = self.client.get('/requests/', post_data)
        self.assertEqual(response.status_code, 302)
        pr = models.PriorityOrder.objects.get(pr_order=0)
        self.assertEqual(pr.priority, 0.8)
        pr = models.PriorityOrder.objects.get(pr_order=1)
        self.assertEqual(pr.priority, 1.0)
        pr = models.PriorityOrder.objects.get(pr_order=2)
        self.assertEqual(pr.priority, 2.0)
        response = self.client.get('/requests/', post_data)
        self.assertEqual(response.status_code, 302)
        pr = models.PriorityOrder.objects.get(pr_order=0)
        self.assertEqual(pr.priority, 2.0)
        pr = models.PriorityOrder.objects.get(pr_order=1)
        self.assertEqual(pr.priority, 1.0)
        pr = models.PriorityOrder.objects.get(pr_order=2)
        self.assertEqual(pr.priority, 0.8)
