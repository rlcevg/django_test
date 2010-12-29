#from django.http import HttpRequest
from contact.models import HttpRequestLog
import datetime

class RequestLogMiddleware(object):
    def process_request(self, request):
        httpRequestLog = HttpRequestLog()
        httpRequestLog.time = datetime.date.today()
        httpRequestLog.host = request.get_host()
        httpRequestLog.full_path = request.get_full_path()
        httpRequestLog.save()

