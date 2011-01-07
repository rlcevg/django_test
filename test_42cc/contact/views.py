from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from contact.forms import AboutFormSet


#@login_required
def edit(request, queryset, object_id):
    person = get_object_or_404(queryset, pk=object_id)
    if request.method == "POST":
        formset = AboutFormSet(request.POST, request.FILES,
                instance=person)
        if formset.is_valid():
            formset.save()
            # Do something.
    else:
        formset = AboutFormSet(instance=person)
    return render_to_response("contact/edit.html", {"formset": formset},
            context_instance=RequestContext(request))
