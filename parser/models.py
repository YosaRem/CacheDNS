from bitstring import BitArray
from .constants import RequestTypes, RecordTypes
from .common_parsers import str_to_hex, domain_to_bytes_str
from hashlib import md5


class Record:
    def __init__(self, domain, ip, qtype, ttl):
        self.ip = ip
        self.type = qtype
        self.domain = domain
        self.ttl = ttl

    def __hash__(self):
        return md5(self.ip + self.domain + self.type).digest()


class Flags:
    def __init__(self, flags: BitArray):
        self.is_request = not flags[0]
        self.type = RequestTypes.get_type(flags.bin[1:5])
        self.tc = flags[5]
        self.rd = flags[6]
        self.ra = flags[7]

    def __str__(self):
        return f"Is request: {self.is_request}; type: {self.type}"


class Header:
    def __init__(self, request_id, flags: Flags, qdc, anc, nsc, arc):
        self.id = request_id
        self.flags = flags
        self.qdcount = qdc
        self.ancount = anc
        self.nscount = nsc
        self.arcount = arc

    def __str__(self):
        return f"Flags: {str(self.flags)}; req_id: {self.id}"


class Question:
    def __init__(self, domain, qtype):
        self.domain = domain
        self.type = qtype

    def to_bytes(self):
        return str_to_hex(domain_to_bytes_str(self.domain) + " 00 " + RecordTypes.get_hex_str_form_str(self.type))

    def __str__(self):
        return f"Domain: {self.domain}; Type: {self.type}"


class Answer:
    def __init__(self, name, qtype, ttl, length, data):
        self.name = name
        self.type = qtype
        self.ttl = ttl
        self.length = length
        self.data = data

    def __str__(self):
        return f"Name: {self.name}, type: {self.type}, ttl: {self.ttl}, data: {self.data}"


class Response:
    def __init__(self, header, questions, answers, authority=None, additional=None):
        self.header = header
        self.questions = questions
        self.answers = answers
        self.authority = [] if authority is None else authority
        self.additional = [] if additional is None else additional

    def __str__(self):
        return f"Header: {{ {self.header} }}; Questions:" \
               f" [{'; '.join(map(str, self.questions))}]; Answers: [{'; '.join(map(str, self.answers))}"


class Request:
    def __init__(self, header, questions, byte_header=None):
        self.header = header
        self.byte_header = byte_header
        self.questions = questions

    def to_bytes(self):
        byte_questions = b""
        for i in self.questions:
            byte_questions += i.to_bytes()
        return self.byte_header + byte_questions + b"\x00\x01"

    def __str__(self):
        return f"Header: {{ {self.header} }}; Questions: [{'; '.join(map(str, self.questions))}]"