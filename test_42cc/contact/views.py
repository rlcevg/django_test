from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from contact.forms import PersonForm, ContactFormSet, RequestForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import simplejson
from contact.models import HttpRequestLog, getOrderList, getOrderedList,\
existedPriority, reorderPriority, deletePriority, sortPriority


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


def requests_view(request, template_name='contact/requests.html', priority=-1):
    def changePriority(post):
        form = RequestForm(post)
        if form.is_valid():
            dumb = form.save(commit=False)
            lst = HttpRequestLog.objects
            for field in form.fields:
                if field != 'priority':
                    kwargs = {field: getattr(dumb, field)}
                    lst = lst.filter(**kwargs)
            if lst.update(priority=dumb.priority) > 0:
                existedPriority(dumb.priority)

    def addPriority(post, rdict):
        rdict['existed'] = existedPriority(post['addPriority'])
        return simplejson.dumps(rdict, ensure_ascii=False)

    def processAjaxReq(post, rdict):
        req_obj = HttpRequestLog.objects.get(pk=post['id'])
        errors = {}
        if req_obj != None:
            req_obj.priority = post['priority']
            req_obj.save()
            if not existedPriority(req_obj.priority):
                rdict['order_list'] = getOrderList()
        else:
            errors['Request'] = 'Object not found'

        if len(errors) > 0:
            rdict['type'] = 'error'
            rdict['msg'] = 'Fix errors and submit again'
            rdict['errors'] = errors
        else:
            rdict['type'] = 'success'
            rdict['msg'] = 'Reload the page'
        return simplejson.dumps(rdict, ensure_ascii=False)

    response_dict = {}

    if request.method == "GET":
        if 'sortPriority' in request.GET:
            sortPriority()
            return redirect('request_home')
        order_list = getOrderList()
        object_list = getOrderedList(order_list, 16)
        form = RequestForm()

    elif request.method == "POST":
        if 'clear_btn' in request.POST:
            HttpRequestLog.objects.all().delete()
            return redirect('request_home')
        elif 'reorder' in request.POST:
            reorderPriority(request.POST)
            return HttpResponse()
        elif 'delPriority' in request.POST:
            deletePriority(request.POST)
            return HttpResponse()
        elif 'addPriority' in request.POST:
            json = addPriority(request.POST, response_dict)
            return HttpResponse(json, mimetype='application/javascript')
        elif 'clone' in request.POST:
            changePriority(request.POST)
            return redirect('request_home')
        elif request.is_ajax():
            json = processAjaxReq(request.POST, response_dict)
            return HttpResponse(json, mimetype='application/javascript')

    response_dict.update({
        'object_list': object_list,
        'order_list': order_list,
        'form': form,
    })
    return render_to_response(template_name, response_dict,
        context_instance=RequestContext(request))
