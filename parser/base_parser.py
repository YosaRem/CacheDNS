from bitstring import BitArray
from .models import Flags, Header
from .constants import RecordTypes


def parse_headers(data: bytes) -> Header:
    bit_data = BitArray(data)
    request_id = bit_data.hex[0:4]
    flags = Flags(BitArray(bit_data.bytes[4:8]))
    qdc = int(bit_data.hex[8:12])
    anc = int(bit_data.hex[12:16])
    nsc = int(bit_data.hex[16:20])
    rdc = int(bit_data.hex[20:24])
    return Header(request_id, flags, qdc, anc, nsc, rdc)


def parse_domain(data: bytes, s_position, end=None) -> (str, int):
    def get_part(part_data):
        part_domain = BitArray(part_data)
        start = 0
        if part_domain.hex[start: start + 2] == "c0":
            return parse_domain_link(data, part_data[1])
        else:
            count = int(part_domain.hex[start: start + 2], 16)
            name = bytes.fromhex(part_domain.hex[2:count * 2 + 2]).decode("ascii")
            return count, name
    position = s_position
    names = []
    while True:
        if position == end:
            break
        new_count, part_name = get_part(data[position:])
        if new_count == 0:
            break
        names.append(part_name)
        position += new_count + 1
    return ".".join(names), position + 1


def parse_ip(data):
    res = []
    for i in data:
        res.append(str(int(i)))
    return ".".join(res)


def parse_domain_link(data: bytes, position):
    domain, count = parse_domain(data, position)
    return 1, domain


def parse_type(data):
    RecordTypes.get_type_from_bytes(data)
