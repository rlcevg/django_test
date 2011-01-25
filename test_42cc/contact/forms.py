from django.forms import ModelForm, Textarea, TextInput
from contact.models import Person, Contact, HttpRequestLog
from django.forms.models import inlineformset_factory
from contact.widgets import CalendarWidget
from django.conf import settings


class PersonForm(ModelForm):
    is_reversed = False

    class Meta:
        model = Person
        exclude = ('signin_date')
        #fields = ('birth_date', 'biography', 'lastname', 'firstname')
        widgets = {
            'biography': Textarea(attrs={'cols': 80, 'rows': 10}),
            'birth_date': CalendarWidget(attrs={
                'img': settings.SITE_MEDIA_PREFIX + "img/baloon_24.png",
            }),
        }

    class Media:
        css = {
            'all': (settings.SITE_MEDIA_PREFIX + "css/edit.css",),
        }
        js = (
            settings.SITE_MEDIA_PREFIX + "js/jquery.min.js",
            settings.SITE_MEDIA_PREFIX + "js/jquery.form.js",
            settings.SITE_MEDIA_PREFIX + "js/ajax_person_form.js",
        )

    def reverseOrder(self, val):
        if val:
            self.fields.keyOrder.reverse()
        self.is_reversed = val


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        widgets = {
            'contact_info': Textarea(attrs={'cols': 40, 'rows': 1})
        }


ContactFormSet = inlineformset_factory(Person, Contact, form=ContactForm,
        max_num=5, extra=2)


class RequestForm(ModelForm):
    class Meta:
        model = HttpRequestLog
        exclude = ('datetime')
        widgets = {
            'full_path': TextInput,
            'priority': TextInput(attrs={'size': 4}),
        }
