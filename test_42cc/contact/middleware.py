#from django.http import HttpRequest
from contact.models import HttpRequestLog
from datetime import datetime

class RequestLogMiddleware(object):
    def process_request(self, request):
        httpRequestLog = HttpRequestLog()
        # date could be formatted with datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        httpRequestLog.datetime = datetime.now()
        httpRequestLog.host = request.get_host()
        httpRequestLog.full_path = request.get_full_path()
        httpRequestLog.save()

