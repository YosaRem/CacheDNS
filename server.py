import socket
from parser.parsers import parse_request, parse_answers
from parser.models import Request, Question
from parser.constants import RecordTypes
from cash.Cash import Cash


class Server:
    def __init__(self):
        self.port_listener = 8000
        self.address_listener = "127.0.0.1"
        self.port_resolver = 53
        self.address_resolver = "77.88.8.8"  # yandex resolver

    def start(self):
        with Cash() as cash:
            data, sender = self.socket_listener.recvfrom(512)
            while data is not None:
                if data:
                    request = parse_request(data)
                    data_to_send = self.get_from_cash(cash, request)
                    if data_to_send is not None:
                        self.socket_listener.sendto(data_to_send, sender)
                    else:
                        data_to_send = self.find_ns(request)
                        if data_to_send is not None:
                            self.socket_listener.sendto(data_to_send, sender)

                data, sender = self.socket_listener.recvfrom(256)

    def get_from_cash(self, cash, request):
        data = cash.get_from_cash(request)
        if data is None:
            return None
        return b"\x00"

    def find_ns(self, request: Request):
        ns_request = Request(
            request.header,
            [Question(request.questions[0].domain, RecordTypes.A)],
            request.byte_header)
        byte_request = ns_request.to_bytes()
        self.socket_resolver.sendto(byte_request, (self.address_resolver, self.port_resolver))
        answer, sender = self.socket_resolver.recvfrom(512)
        answer = parse_answers(answer)
        return answer

    def __enter__(self):
        self.socket_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_listener.bind((self.address_listener, self.port_listener))
        self.socket_resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket_listener.close()
        self.socket_resolver.close()


with Server() as s:
    s.start()
