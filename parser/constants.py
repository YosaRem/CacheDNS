class RequestTypes:
    STANDARD = "standard"
    INVERSE = "inverse"
    STATUS_REQUEST = "status"
    UNKNOWN = "unknown"

    @staticmethod
    def get_type(data):
        if data == "0000":
            return RequestTypes.STANDARD
        if data == "0001":
            return RequestTypes.INVERSE
        if data == "0010":
            return RequestTypes.STATUS_REQUEST
        return RequestTypes.UNKNOWN

    @staticmethod
    def get_byte_type(data: str) -> bytes:
        if data == RequestTypes.STANDARD:
            return b"\x00\x00"
        if data == RequestTypes.INVERSE:
            return b"\x00\x01"
        if data == RequestTypes.STATUS_REQUEST:
            return b"\x00\x10"
        return b"\x00\x00"


class RecordTypes:
    A = "A"
    AAAA = "AAAA"
    MX = "MX"
    NS = "NS"
    CNAME = "CNAME"
    PTR = "PTR"
    ANY = "ANY"
    SOA = "SOA"
    TXT = "TXT"

    ValidRequestType = [A, MX, TXT]

    ABytes = b"\x00\x01"
    AAAABytes = b"\x00\x1c"
    MXBytes = b"\x00\x0f"
    NSBytes = b"\x00\x02"
    CNAMEBytes = b"\x00\x05"
    PTRBytes = b"\x00\x0c"
    ANYBytes = b"\x00\xff"
    SOABytes = b"\x00\x06"
    TXTBytes = b"\x00\x10"

    AStr = "00 01"
    AAAAStr = "00 1c"
    MXStr = "00 0f"
    NSStr = "00 02"
    CNAMEStr = "00 05"
    PTRStr = "00 0c"
    ANYStr = "00 ff"
    SOAStr = "00 06"
    TXTStr = "00 10"

    @staticmethod
    def get_hex_str_form_str(data: str) -> str:
        if data == RecordTypes.A:
            return RecordTypes.AStr
        if data == RecordTypes.AAAA:
            return RecordTypes.AAAAStr
        if data == RecordTypes.MX:
            return RecordTypes.MXStr
        if data == RecordTypes.NS:
            return RecordTypes.NSStr
        if data == RecordTypes.CNAME:
            return RecordTypes.CNAMEStr
        if data == RecordTypes.PTR:
            return RecordTypes.PTRStr
        if data == RecordTypes.ANY:
            return RecordTypes.ANYStr
        if data == RecordTypes.TXT:
            return RecordTypes.TXTStr
        if data == RecordTypes.SOA:
            return RecordTypes.SOAStr

    @staticmethod
    def get_type_from_bytes(data: bytes) -> str:
        if data == RecordTypes.ABytes:
            return RecordTypes.A
        if data == RecordTypes.AAAABytes:
            return RecordTypes.AAAA
        if data == RecordTypes.MXBytes:
            return RecordTypes.MX
        if data == RecordTypes.NSBytes:
            return RecordTypes.NS
        if data == RecordTypes.CNAMEBytes:
            return RecordTypes.CNAME
        if data == RecordTypes.PTRBytes:
            return RecordTypes.PTR
        if data == RecordTypes.ANYBytes:
            return RecordTypes.ANY
        if data == RecordTypes.TXTBytes:
            return RecordTypes.TXT
        if data == RecordTypes.SOABytes:
            return RecordTypes.SOA

    @staticmethod
    def get_bytes_form_str(data: str) -> bytes:
        if data == RecordTypes.A:
            return RecordTypes.ABytes
        if data == RecordTypes.AAAA:
            return RecordTypes.AAAABytes
        if data == RecordTypes.MX:
            return RecordTypes.MXBytes
        if data == RecordTypes.NS:
            return RecordTypes.NSBytes
        if data == RecordTypes.CNAME:
            return RecordTypes.CNAMEBytes
        if data == RecordTypes.PTR:
            return RecordTypes.PTRBytes
        if data == RecordTypes.ANY:
            return RecordTypes.ANYBytes
        if data == RecordTypes.SOA:
            return RecordTypes.SOABytes
        if data == RecordTypes.TXT:
            return RecordTypes.TXTBytes

