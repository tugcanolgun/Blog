from logstash import TCPLogstashHandler


def _get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class CustomTCPLogstashHandler(TCPLogstashHandler):
    def emit(self, record):
        try:
            request = record.args[0]
            record.ip = _get_client_ip(request)
            record.args = None
        except Exception:
            pass

        super(TCPLogstashHandler, self).emit(record)
