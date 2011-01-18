from contact.models import HttpRequestLog, PriorityStruct as PS
from datetime import datetime


class RequestLogMiddleware(object):
    def process_request(self, request):
        httpRequestLog = HttpRequestLog()
        httpRequestLog.datetime = datetime.now()
        httpRequestLog.host = request.get_host()
        httpRequestLog.full_path = request.get_full_path()
        httpRequestLog.is_ajax = request.is_ajax()
        httpRequestLog.is_secure = request.is_secure()
        httpRequestLog.method = request.method
        if PS.PRIORITY_VAR in request.REQUEST:
            httpRequestLog.priority = request.REQUEST[PS.PRIORITY_VAR]
        httpRequestLog.save()
