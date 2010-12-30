from django.test import TestCase
from contact import models


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


class ContextProcessorTest(TestCase):
    def test_context_processor(self):
        response = self.client.get('/requests/')
        self.assertEqual(response.context['DEBUG'], True)
        self.assertEqual(response.context['DATABASES'], {'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'contact.db',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': ''}})
        self.assertEqual(response.context['TIME_ZONE'], 'America/Chicago')
        self.assertEqual(response.context['LANGUAGE_CODE'], 'en-us')
        self.assertEqual(response.context['SITE_ID'], 1)
        self.assertEqual(response.context['USE_I18N'], True)
        self.assertEqual(response.context['USE_L10N'], True)
        self.assertEqual(response.context['MEDIA_ROOT'], '')
        self.assertEqual(response.context['MEDIA_URL'], '')
        self.assertEqual(response.context['ADMIN_MEDIA_PREFIX'], '/media/')
        self.assertNotEqual(response.context['SECRET_KEY'], 'lol')
        self.assertEqual(response.context['TEMPLATE_LOADERS'], (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'))
        self.assertEqual(response.context['ROOT_URLCONF'], 'test_42cc.urls')

