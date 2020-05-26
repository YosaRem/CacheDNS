from parser.models import Request, Response, CashRecord
from .constants import FILE_NAME


class Cash:
    def __init__(self):
        self.info = {}

    def get_from_cash(self, request: Request):
        res = []
        for i in request.questions:
            data = self.info.get(CashRecord(i.domain, i.type, 0, 0))
            if data is not None and not data.is_expire():
                data.recalculate_ttl()
                res.append(data)
        return res

    def add_to_cash(self, response: Response):
        for i in response.answers:
            self.info[CashRecord(i.name, i.type, i.ttl, i.data)] = CashRecord(
                i.name, i.type, i.ttl, i.data)
        for i in response.authority:
            self.info[CashRecord(i.name, i.type, i.ttl, i.data)] = CashRecord(
                i.name, i.type, i.ttl, i.data)
        for i in response.additional:
            self.info[CashRecord(i.name, i.type, i.ttl, i.data)] = CashRecord(
                i.name, i.type, i.ttl, i.data)

    def del_ttl_expire(self):
        new = {}
        for i in self.info:
            if not i.is_expire():
                new[i] = self.info[i]
        self.info = new

    def store_cash(self):
        self.del_ttl_expire()
        print("stored")

    def restore_cash(self):
        self.del_ttl_expire()

    def __enter__(self):
        self.restore_cash()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.store_cash()
