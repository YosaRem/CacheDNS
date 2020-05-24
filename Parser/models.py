from bitstring import BitArray
from .constants import RequestTypes


class ServerInfo:
    def __init__(self, qtype, qname, ip):
        self.ip = ip
        self.type = qtype
        self.name = qname


class Flags:
    def __init__(self, flags: BitArray):
        self.is_request = not flags[0]
        self.type = RequestTypes.get_type(flags.bin[1:5])
        self.tc = flags[5]
        self.rd = flags[6]
        self.ra = flags[7]

    def __str__(self):
        return f"is request: {self.is_request}; type: {self.type}"


class Header:
    def __init__(self, request_id, flags: Flags, qdc, anc, nsc, arc):
        self.id = request_id
        self.flags = flags
        self.qdcount = qdc
        self.ancount = anc
        self.nscount = nsc
        self.arcount = arc

    def __str__(self):
        return f"flags: {str(self.flags)}; req_id: {self.id}"


class Question:
    def __init__(self, domain, qtype):
        self.domain = domain
        self.type = qtype


class Request:
    def __init__(self, header, questions):
        self.header = header
        self.questions = questions
