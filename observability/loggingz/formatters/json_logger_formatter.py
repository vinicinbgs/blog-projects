import json
import logging
from datetime import datetime

from ..trace_id import TraceId


class JsonLoggerFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "extra": getattr(record, "args", {}),
            "trace_id": TraceId().get_id(),
        }
        return json.dumps(log_record)
