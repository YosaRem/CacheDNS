import socket
from Parser.request_to_server import get_request


class Server:
    def __init__(self):
        self.port = 8000
        self.local = "127.0.0.1"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local, self.port))

    def start(self):
        data, sender = self.socket.recvfrom(256)
        while data is not None:
            if data:
                self.socket.sendto(b"d", sender)
                request = get_request(data)
                print(request)
            data, sender = self.socket.recvfrom(256)


s = Server()
s.start()