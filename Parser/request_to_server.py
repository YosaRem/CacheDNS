from .base_parser import parse_headers, parse_domain
from .constants import RecordTypes
from .models import Question, Request


def get_request(data: bytes):
    header = parse_headers(data)
    questions = []
    start = 12
    for i in range(header.qdcount):
        domain, position = parse_domain(data[start:])
        qtype = RecordTypes.get_type_from_bytes(data[position + start: position + start + 2])
        questions.append(Question(domain, qtype))
        start += position + 4
    return Request(header, questions)

