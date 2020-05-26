from .base_parser import parse_headers, parse_domain, parse_ip
from .constants import RecordTypes
from .models import Question, Request, Answer, Response


def parse_queries(data: bytes, count):
    questions = []
    position = 12
    for i in range(count):
        domain, position = parse_domain(data, position)
        qtype = RecordTypes.get_type_from_bytes(data[position: position + 2])
        questions.append(Question(domain, qtype))
        position += 4
    return questions, position


def parse_answer(data: bytes, position, count):
    answers = []
    start = position
    for i in range(count):
        domain, position = parse_domain(data, start)
        start = position - 1
        print(data[position:])
        qtype = RecordTypes.get_type_from_bytes(data[start:start + 2])
        start += 4
        ttl = int.from_bytes(data[start: start + 4], "big")
        start += 4
        length = int.from_bytes(data[start: start + 2], "big")
        start += 2
        if qtype == RecordTypes.NS:
            answer_data, position = parse_domain(data, start, start + length)
            answers.append(Answer(domain, qtype, ttl, length, answer_data))
        if qtype == RecordTypes.A:
            ip = parse_ip(data[start:start + 4])
            print(ip)
            answers.append(Answer(domain, qtype, ttl, length, ip))
        else:
            answers.append(Answer(domain, qtype, ttl, length, data[start: start + length]))
        start += length
    return answers, start


def parse_request(data: bytes) -> Request:
    header = parse_headers(data)
    queries, position = parse_queries(data, header.qdcount)
    return Request(header, queries, data[:12])


def parse_answers(data: bytes):
    header = parse_headers(data)
    queries, position = parse_queries(data, header.qdcount)
    answers, position = parse_answer(data, position, header.ancount)
    return Response(header, queries, answers)

