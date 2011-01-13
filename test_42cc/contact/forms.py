from django.forms import ModelForm, Textarea
from contact.models import Person, Contact
from django.forms.models import inlineformset_factory
from contact.widgets import CalendarWidget
from django.conf import settings
from django.utils.safestring import mark_safe


class PersonForm(ModelForm):
    is_reversed = False

    class Meta:
        model = Person
        exclude = ('signin_date')
        #fields = ('birth_date', 'biography', 'lastname', 'firstname')
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

    def as_table(self):
        output = super(PersonForm, self).as_table()
        if self.is_reversed:
            lines = output.split('\n')
            lines.reverse()
            output = mark_safe(u'\n'.join(lines))
        return output


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        widgets = {
            'contact_info': Textarea(attrs={'cols': 40, 'rows': 2})
        }


ContactFormSet = inlineformset_factory(Person, Contact, form=ContactForm,
        max_num=5, extra=2)
