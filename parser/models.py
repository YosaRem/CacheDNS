from bitstring import BitArray
from .constants import RequestTypes, RecordTypes
from .common_parsers import str_to_hex, domain_to_bytes_str, int_to_hex
import time
import math
from hashlib import md5


class CashRecord:
    def __init__(self, name, qtype, ttl, length, data):
        self.name = name
        self.type = qtype
        self.ttl = ttl
        self.length = length
        self.time_added = time.time()
        self.data = data

    def is_expire(self) -> bool:
        return time.time() - self.time_added > self.ttl

    def recalculate_ttl(self):
        self.ttl = math.floor(self.time_added + self.ttl - time.time())

    def __str__(self):
        return f"{self.name} {self.type} {math.floor(self.ttl)}"

    def __hash__(self):
        return int(md5(self.name.encode() + self.type.encode()).hexdigest(), 16)


class Flags:
    def __init__(self, flags: BitArray):
        self.flags = flags
        self.is_request = flags[0]
        self.type = RequestTypes.get_type(flags.bin[1:5])
        self.tc = flags[5]
        self.rd = flags[6]
        self.ra = flags[7]

    def to_bytes(self):
        return str_to_hex(self.flags.hex)

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

    def to_bytes(self):
        id_bytes = str_to_hex(self.id)
        flags_bytes = self.flags.to_bytes()
        return id_bytes + flags_bytes + int_to_hex(self.qdcount, 4) + int_to_hex(
            self.ancount, 4) + int_to_hex(self.nscount, 4) + int_to_hex(
            self.arcount, 4)

    def __str__(self):
        return f"Flags: {str(self.flags)}; req_id: {self.id}"


class Question:
    def __init__(self, domain, qtype):
        self.domain = domain
        self.type = qtype

    def to_bytes(self):
        return str_to_hex(domain_to_bytes_str(self.domain) + " 00 " +
                          RecordTypes.get_hex_str_form_str(self.type)) + b'\x00\x01'

    def __str__(self):
        return f"Domain: {self.domain}; Type: {self.type}"


class Answer:
    def __init__(self, name, qtype, ttl, length, data):
        self.name = name
        self.type = qtype
        self.ttl = ttl
        self.length = length
        self.data = data

    def to_bytes(self):
        name_bytes = str_to_hex(domain_to_bytes_str(self.name))
        type_bytes = RecordTypes.get_bytes_form_str(self.type)
        ttl_bytes = int_to_hex(self.ttl, 8)
        length_bytes = int_to_hex(self.length, 4)
        if self.type == RecordTypes.NS:
            data_bytes = str_to_hex(domain_to_bytes_str(self.data))
        elif self.type == RecordTypes.A:
            data_bytes = str_to_hex('{:02X}{:02X}{:02X}{:02X}'.format(*map(int, self.data.split("."))))
        else:
            if type(self.data) == str:
                data_bytes = str_to_hex(self.data)
            else:
                data_bytes = self.data
        return name_bytes + type_bytes + b"\x00\x01" + ttl_bytes + length_bytes + data_bytes

    def __str__(self):
        return f"Name: {self.name}, type: {self.type}, ttl: {self.ttl}, data: {self.data} \n"


class Response:
    def __init__(self, data, header, questions, answers, authority=None, additional=None):
        self.data_bytes = data
        self.header = header
        self.questions = questions
        self.answers = answers
        self.authority = [] if authority is None else authority
        self.additional = [] if additional is None else additional

    def get_all_info(self):
        return self.answers + self.authority + self.additional

    def to_bytes(self):
        header_bytes = self.header.to_bytes()
        questions_bytes = b""
        for i in self.questions:
            questions_bytes += i.to_bytes()
        answers_bytes = b""
        for i in self.answers:
            answers_bytes += i.to_bytes()
        return header_bytes + questions_bytes + answers_bytes

    def __str__(self):
        return f"Header: {{ {self.header} }}; \nQuestions:" \
               f" [{'; '.join(map(str, self.questions))}]; \nAnswers: [\n{' '.join(map(str, self.answers))}]"


class Request:
    def __init__(self, header, questions, byte_header=None):
        self.header = header
        self.byte_header = byte_header
        self.questions = questions

    def to_bytes(self):
        byte_questions = b""
        for i in self.questions:
            byte_questions += i.to_bytes() + b"\x00\x01"
        return self.byte_header + byte_questions

    def __str__(self):
        return f"Header: {{ {self.header} }}; Questions: [{'; '.join(map(str, self.questions))}]"
