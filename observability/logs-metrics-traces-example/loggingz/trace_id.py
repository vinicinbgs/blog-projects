import uuid
from contextvars import ContextVar

trace_id_var = ContextVar("trace_id", default=None)


class TraceId:
    @staticmethod
    def set_id(cid=None):
        if cid is None:
            cid = str(uuid.uuid4())
        trace_id_var.set(cid)
        return cid

    @staticmethod
    def get_id():
        cid = trace_id_var.get()
        if cid is None:
            cid = TraceId.set_id()
        return cid

    @staticmethod
    def reset_id():
        trace_id_var.set(None)
