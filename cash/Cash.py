from parser.models import Request, Response, CashRecord
from .constants import FILE_NAME


class Cash:
    def __init__(self):
        self.info = {}

    def get_from_cash(self, request: Request):
        res = []
        for i in request.questions:
            data = self.info.get((i.domain, i.type))
            for j in data:
                if not j.is_expire():
                    j.recalculate_ttl()
                    res.append(j)
        if len(res) == 0:
            return None
        return res

    def add_to_cash(self, response: Response):
        for i in response.answers + response.authority + response.additional:
            record = CashRecord(i.name, i.type, i.ttl, i.data)
            if (i.domain, i.type) in self.info:
                self.info[(i.domain, i.type)].append(record)
            else:
                self.info[(i.domain, i.type)] = [record]

    def del_ttl_expire(self):
        new = {}
        for i in self.info:
            new[(i[0], i[1])] = []
            for j in self.info[i]:
                if not j.is_expire():
                    new[i].append(j)
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
