from threading import Thread
import socket

MSGLEN = 100


class Sender(Thread):
    def __init__(self, queue, address=socket.gethostbyname(), port=1500):
        self.queue = queue
        self.address = address
        self.port = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))
        self.client_socket = s

    def send_to_client(self, message):
        total_sent = 0
        while total_sent < MSGLEN:
            sent = self.sock.send(message[total_sent:].encode())
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent = total_sent + sent

    def run(self):
        while True:
            self.send_to_client(self.queue.get())
