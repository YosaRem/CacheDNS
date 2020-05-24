from .base_parser import parse_headers, parse_domain
from .constants import RecordTypes


def get_request(data: bytes):
    header = parse_headers(data)
    start = 12
    for i in range(header.qdcount):
        domain, position = parse_domain(data[start:])
        print(header)
        print(domain)
        print(RecordTypes.get_type_from_bytes(data[position + start: position + start + 2]))
        start += position + 4


