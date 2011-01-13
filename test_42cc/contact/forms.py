from django.forms import ModelForm, Textarea
from contact.models import Person, Contact
from django.forms.models import inlineformset_factory
from contact.widgets import CalendarWidget
from django.conf import settings


class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('signin_date')
        widgets = {
            'biography': Textarea(attrs={'cols': 80, 'rows': 20}),
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


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        widgets = {
            'contact_info': Textarea(attrs={'cols': 40, 'rows': 2})
        }


ContactFormSet = inlineformset_factory(Person, Contact, form=ContactForm,
        max_num=5, extra=2)