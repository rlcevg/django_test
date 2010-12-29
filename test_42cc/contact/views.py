from django.shortcuts import render_to_response
from contact.models import HttpRequestLog

def process_requests(request):
    request_list = HttpRequestLog.objects.order_by('-datetime')[:10]
    return render_to_response('contact/requests.html', {'request_list': request_list})

