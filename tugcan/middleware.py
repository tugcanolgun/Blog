import sys
import traceback

from logstash import TCPLogstashHandler

from django.core.handlers.wsgi import WSGIRequest


def _get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class DjangoLogstashFormatter:

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(DjangoLogstashFormatter, self).__init__(*args, **kwargs)
        self._django_version = None
        self._fetch_django_version()

    # ----------------------------------------------------------------------
    def _fetch_django_version(self):
        from django import (
            get_version,
        )  # pylint: disable=import-error,import-outside-toplevel

        self._django_version = get_version()

    def _get_extra_fields(self, record):
        return {
            "func_name": record.funcName,
            "interpreter": sys.executable,
            "interpreter_version": u"{}.{}.{}".format(
                sys.version_info.major, sys.version_info.minor, sys.version_info.micro
            ),
            "line": record.lineno,
            "logger_name": record.name,
            "path": record.pathname,
            "process_name": record.processName,
            "thread_name": record.threadName,
        }

    # ----------------------------------------------------------------------
    def get_fields(self, record):
        extra_fields = {}
        if hasattr(record, "status_code"):
            extra_fields["status_code"] = record.status_code

        # Django's runserver command passes socketobject and WSGIRequest instances as "request".
        # Hence the check for the META attribute.
        # For details see https://code.djangoproject.com/ticket/27234
        if record.exc_info:
            extra_fields["stack_trace"] = self._format_exception(record.exc_info)

        extra_fields.update(self._get_extra_fields(record))

        if hasattr(record, "request") and hasattr(record.request, "META"):
            request = record.request

            request_user = self._get_attribute_with_default(request, "user", "")
            extra_fields["django_version"] = self._django_version
            extra_fields["req_useragent"] = request.META.get(
                "HTTP_USER_AGENT", "<none>"
            )
            extra_fields["req_ip"] = _get_client_ip(record.request)
            extra_fields["req_host"] = self._try_to_get_host_from_remote(request)
            extra_fields["req_uri"] = request.get_raw_uri()
            extra_fields["req_user"] = str(request_user)
            extra_fields["req_method"] = request.META.get("REQUEST_METHOD", "")
            extra_fields["req_referer"] = request.META.get("HTTP_REFERER", "")

            forwarded_proto = request.META.get("HTTP_X_FORWARDED_PROTO", None)
            if forwarded_proto is not None:
                extra_fields["req_forwarded_proto"] = forwarded_proto

            forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", None)
            if forwarded_for is not None:
                # make it a list
                forwarded_for_list = forwarded_for.replace(" ", "").split(",")
                extra_fields["req_forwarded_for"] = forwarded_for_list

            # template debug
            if isinstance(record.exc_info, tuple):
                exc_value = record.exc_info[1]
                template_info = getattr(exc_value, "template_debug", None)
                if template_info:
                    extra_fields["tmpl_name"] = template_info["name"]
                    extra_fields["tmpl_line"] = template_info["line"]
                    extra_fields["tmpl_message"] = template_info["message"]
                    extra_fields["tmpl_during"] = template_info["during"]

        return {key: value for key, value in extra_fields.items() if value is not None}

    # ----------------------------------------------------------------------
    def _get_attribute_with_default(self, obj, attr_name, default=None):
        """
        Query an attribute from an object but check before if it exists or return
        a default value if it is missing
        """
        if hasattr(obj, attr_name):
            value = getattr(obj, attr_name)
            if value is not None:
                return value
        # fallback
        return default

    # ----------------------------------------------------------------------
    def _try_to_get_host_from_remote(self, request):
        try:
            return request.get_host()
        except Exception:
            if "HTTP_HOST" in request.META:
                return request.META["HTTP_HOST"]
            else:
                return request.META["SERVER_NAME"]

    def _format_exception(self, exc_info):
        if isinstance(exc_info, tuple):
            stack_trace = "".join(traceback.format_exception(*exc_info))
        elif exc_info:
            stack_trace = "".join(traceback.format_stack())
        else:
            stack_trace = ""
        return stack_trace


class CustomTCPLogstashHandler(TCPLogstashHandler):
    def emit(self, record):
        if record.args:
            record.request = record.args[0]
            if isinstance(record.args[0], WSGIRequest):
                record.args = None

        extra_fields = DjangoLogstashFormatter().get_fields(record)
        for key, field in extra_fields.items():
            setattr(record, key, field)

        super(TCPLogstashHandler, self).emit(record)
