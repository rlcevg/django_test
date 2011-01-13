from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from contact.forms import PersonForm, ContactFormSet
from django.http import HttpResponseRedirect, HttpResponse
from django.core import urlresolvers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import simplejson


@login_required
def edit(request, queryset, object_id):
    person = get_object_or_404(queryset, pk=object_id)
    response_dict = {}

    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES,
                instance=person)
        formset = ContactFormSet(request.POST, request.FILES,
                instance=person)
        errors = {}

        if form.is_valid():
            form.save()
        else:
            errors.update([(key, unicode(value[0]))
                for key, value in form.errors.items()])

        if formset.is_valid():
            formset.save()
        else:
            errors.update([(key, unicode(value[0]))
                for key, value in formset.errors.items()])

        if len(errors) > 0:
            response_dict['type'] = 'error'
            response_dict['msg'] = 'Fix errors and submit again'
            response_dict['errors'] = errors
        else:
            response_dict['type'] = 'success'
            response_dict['msg'] = 'Thank you-u-u'

        if request.is_ajax():
            json = simplejson.dumps(response_dict, ensure_ascii=False)
            return HttpResponse(json, mimetype='application/javascript')

    else:
        form = PersonForm(instance=person)
        formset = ContactFormSet(instance=person)

    response_dict.update({"form": form, "formset": formset})
    return render_to_response("contact/edit.html", response_dict,
            context_instance=RequestContext(request))


def site_logout(request):
    logout(request)
    return HttpResponseRedirect(urlresolvers.reverse("home"))
