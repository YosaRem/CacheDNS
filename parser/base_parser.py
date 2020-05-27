from bitstring import BitArray
from .models import Flags, Header
from .constants import RecordTypes


def parse_headers(data: bytes) -> Header:
    bit_data = BitArray(data)
    request_id = bit_data.hex[0:4]
    flags = Flags(BitArray(bit_data.bytes[4:6]))
    qdc = int(bit_data.hex[8:12], 16)
    anc = int(bit_data.hex[12:16], 16)
    nsc = int(bit_data.hex[16:20], 16)
    rdc = int(bit_data.hex[20:24], 16)
    return Header(request_id, flags, qdc, anc, nsc, rdc)


def parse_domain(data: bytes, s_position, end=None) -> (str, int):
    def get_part(part_data):
        part_domain = BitArray(part_data)
        start = 0
        if part_domain.hex[start: start + 2] == "c0" or part_domain.hex[start: start + 2] == "c1":
            return parse_domain_link(data, part_data[0: 2])
        else:
            count = int(part_domain.hex[start: start + 2], 16)
            name = bytes.fromhex(part_domain.hex[2:count * 2 + 2]).decode("ascii")
            return count, name
    position = s_position
    names = []
    if end is None:
        end = -1
    while True:
        if position == int(end) + 1:
            position += 1
            break
        new_count, part_name = get_part(data[position:])
        if new_count == 0:
            break
        names.append(part_name)
        position += new_count + 1
        if new_count == 1:
            break
    return ".".join(names), position + 1


def parse_ip(data):
    res = []
    for i in data:
        res.append(str(int(i)))
    return ".".join(res)


def parse_domain_link(data: bytes, position: bytes):
    length = int(BitArray(position).bin[2:], 2)
    domain, count = parse_domain(data, length)
    return 1, domain


def parse_type(data):
    RecordTypes.get_type_from_bytes(data)
