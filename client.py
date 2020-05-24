import socket


req = ["aa aa 01 00 00 02 00 00 00 00 00 00",
        "03 77 77 77 06 67 6f 6f 67 6c 65 03 63 6f 6d 00 00 01 00 01",
       "03 77 77 77 06 67 6f 6f 67 6c 65 03 63 6f 6d 00 00 01 00 01"]


def c():
    res = b""
    for i in req:
        res += bytearray.fromhex(i)
    return res

d = c()

print(d)

class Client:
    def __init__(self, q_name, q_type):
        self.name = q_name
        self.type = q_type
        self.address = "127.0.0.1"
        self.port = 8000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.sendto(d, (self.address, self.port))
        data = self.socket.recvfrom(256)
        print(data)


Client("a", "a")
