from django.forms import ModelForm
from contact.models import Person, Contact
from django.forms.models import inlineformset_factory


class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('signin_date')

ContactFormSet = inlineformset_factory(Person, Contact)
