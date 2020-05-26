import socket
from bitstring import BitArray
from parser.parsers import parse_request, parse_answers
from parser.models import Request, Question, Response, Header, Flags
from parser.constants import RecordTypes
from parser.common_parsers import str_to_hex
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
                        self.get_from_ns(request)
                        if data_to_send is not None:
                            self.socket_listener.sendto(data_to_send, sender)
                        self.socket_listener.sendto(b"", sender)
                data, sender = self.socket_listener.recvfrom(512)
                cash.del_ttl_expire()


    def get_from_ns(self, request: Request):
        answer = self.find_ns(request)
        answer = self.find_ip_for_ns(answer)
        answer = self.find_any_record_on_ns(answer, request.questions[0].domain)
        print(answer)

    def get_from_cash(self, cash, request):
        data = cash.get_from_cash(request)
        if data is None:
            return None
        return b"\x00"

    def find_ns(self, request: Request):
        ns_request = Request(
            request.header,
            [Question(request.questions[0].domain, RecordTypes.NS)],
            request.byte_header)
        byte_request = ns_request.to_bytes()
        self.socket_resolver.sendto(byte_request, (self.address_resolver, self.port_resolver))
        answer, sender = self.socket_resolver.recvfrom(512)
        answer = parse_answers(answer)
        return answer

    def find_ip_for_ns(self, response: Response):
        domain = response.answers[0].data
        request = Request(Header("aaaa", Flags(BitArray(b"\x01\x00")), 1, 0, 0, 0),
                          [Question(domain, RecordTypes.A)], str_to_hex("aa aa 01 00 00 01 00 00 00 00 00 00"))
        req_bytes = request.to_bytes()
        self.socket_resolver.sendto(req_bytes, (self.address_resolver, self.port_resolver))
        data, sender = self.socket_resolver.recvfrom(512)
        data = parse_answers(data)
        return data

    @staticmethod
    def find_any_record_on_ns(response: Response, domain):
        req = Request(Header("aaaa", Flags(BitArray(b"\x01\x00")), 1, 0, 0, 0),
                      [Question(domain, RecordTypes.ANY)],
                      str_to_hex("aa aa 01 00 00 01 00 00 00 00 00 00"))
        req_bytes = req.to_bytes()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(req_bytes, (response.answers[0].data, 53))
            data, sender = s.recvfrom(512)
            response = parse_answers(data)
        return response

    def __enter__(self):
        self.socket_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_listener.bind((self.address_listener, self.port_listener))
        self.socket_resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket_listener.close()
        self.socket_resolver.close()


with Server() as ser:
    ser.start()
