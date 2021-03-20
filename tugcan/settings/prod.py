from .base import *

DEBUG = False


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "logstash": {
            "level": "INFO",
            "class": "tugcan.middleware.CustomTCPLogstashHandler",
            "host": os.environ.get("LOGSTASH_URL", ""),
            "port": os.environ.get("LOGSTASH_PORT", 5100),
            "version": 1,
            "message_type": "django",
            "fqdn": False,
            "tags": os.environ.get("LOGSTASH_TAGS", "").split(","),
        },
    },
    "loggers": {
        "": {"handlers": ["logstash"], "level": "DEBUG"},
    },
}
