from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from contact.forms import PersonForm, ContactFormSet
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import simplejson
from contact.models import HttpRequestLog, PriorityStruct as PS
from itertools import chain


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
        if 'button_reverse' in request.GET:
            form.reverseOrder(request.GET['is_reversed'] == 'False')

    response_dict['is_reversed'] = form.is_reversed
    response_dict.update({"form": form, "formset": formset})
    return render_to_response("contact/edit.html", response_dict,
            context_instance=RequestContext(request))


def site_logout(request):
    logout(request)
    return redirect("home")


def requests_view(request, template_name='contact/requests.html'):
    if request.method == "GET":
        if 'prior_btn' in request.GET:
            try:
                pr = int(request.GET['prior_btn'])
                if pr in PS.PRIORITY_DICT:
                    pr_filter = HttpRequestLog.objects.filter(priority=pr).\
                        order_by('-datetime')[:10]
                    pr_exclude = HttpRequestLog.objects.exclude(priority=pr).\
                        order_by('-datetime')[:10]
                    object_list = list(chain(pr_filter, pr_exclude))[:10]
                    return render_to_response(
                        template_name,
                        {'object_list': object_list},
                        context_instance=RequestContext(request)
                    )
            except ValueError:
                pass

    elif request.method == "POST":
        if 'clear_btn' in request.POST:
            rec = HttpRequestLog.objects.latest('datetime')
            HttpRequestLog.objects.all().delete()
            rec.save()

    object_list = HttpRequestLog.objects.order_by('-datetime')[:10]
    return render_to_response(template_name, {'object_list': object_list},
        context_instance=RequestContext(request))
