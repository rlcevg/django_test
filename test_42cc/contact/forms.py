from django.forms import ModelForm, Textarea
from contact.models import Person, Contact
from django.forms.models import inlineformset_factory


class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('signin_date')
        widgets = {
            'biography': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

ContactFormSet = inlineformset_factory(Person, Contact, max_num=5, extra=2)
