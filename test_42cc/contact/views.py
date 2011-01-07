from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from contact.forms import PersonForm, ContactFormSet
from django.http import HttpResponseRedirect
from django.core import urlresolvers


#@login_required
def edit(request, queryset, object_id):
    person = get_object_or_404(queryset, pk=object_id)
    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES,
                instance=person)
        formset = ContactFormSet(request.POST, request.FILES,
                instance=person)
        if form.is_valid():
            form.save()
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(urlresolvers.reverse('home'))
    else:
        form = PersonForm(instance=person)
        formset = ContactFormSet(instance=person)
    return render_to_response("contact/edit.html", {
                "form": form,
                "formset": formset,
            },
            context_instance=RequestContext(request))
