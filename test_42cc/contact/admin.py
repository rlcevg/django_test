from contact.models import Person, Contact
from django.contrib import admin


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 3


class PersonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['firstname', 'lastname']}),
        (
            'Bio info',
            {
                'fields': [
                    'biography',
                    'birth_date',
                    'signin_date'
                ],
                'classes': ['collapse']
            }
        ),
    ]
    inlines = [ContactInline]
    list_display = (
        'firstname',
        'lastname',
        'biography',
        'birth_date',
        'signin_date'
    )
    list_filter = ['lastname']
    search_fields = ['firstname', 'lastname']
    date_hierarchy = 'birth_date'


admin.site.register(Person, PersonAdmin)
