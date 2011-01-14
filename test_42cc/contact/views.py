from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from contact.forms import PersonForm, ContactFormSet
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
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
        return redirect("home")
    else:
        form = PersonForm(instance=person)
        formset = ContactFormSet(instance=person)

    return render_to_response("contact/edit.html", {
                "form": form,
                "formset": formset,
            },
            context_instance=RequestContext(request))


def site_logout(request):
    logout(request)
    return redirect("home")
