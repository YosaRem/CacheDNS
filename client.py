import socket
from parser.constants import RecordTypes
from parser.common_parsers import str_to_hex, domain_to_bytes_str


def insert_name_into_request(domain):
    return "aa aa 01 00 00 01 00 00 00 00 00 00 {} 00 {} 00 01".format(domain_to_bytes_str(domain), RecordTypes.ANYStr)


d = str_to_hex(insert_name_into_request("e1.ru"))


class Client:
    def __init__(self, q_name, q_type):
        self.name = q_name
        self.type = q_type
        self.address = "127.0.0.1"
        self.port = 8000
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(d, (self.address, self.port))
            data = s.recvfrom(256)
            print(data)


Client("a", "a")

