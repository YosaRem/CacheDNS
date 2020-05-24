import socket
from parser.request_to_server import get_request


class Server:
    def __init__(self):
        self.port_listener = 8000
        self.address_listener = "127.0.0.1"
        self.socket_listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_listener.bind((self.address_listener, self.port_listener))
        self.port_resolver = 53
        self.address_resolver = "77.88.8.7"  # yandex family
        self.socket_resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        data, sender = self.socket_listener.recvfrom(256)
        while data is not None:
            if data:
                self.socket_listener.sendto(b"d", sender)
                request = get_request(data)

            data, sender = self.socket_listener.recvfrom(256)


s = Server()
s.start()