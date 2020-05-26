from parser.models import Request
from .constants import FILE_NAME


class Cash:
    def __init__(self):
        self.info = {}

    def get_from_cash(self, request: Request):
        return None

    def add_to_cash(self, response):
        pass

    def del_ttl_expire(self):
        pass

    def store_cash(self):
        print("stored")

    @staticmethod
    def restore_cash():
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.store_cash()
