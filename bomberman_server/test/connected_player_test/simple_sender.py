import socket
import threading
import time


MSGLEN = 100
MESSAGE = "Test message".zfill(MSGLEN)

class SimpleSender(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.address = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.client_socket.connect((socket.gethostbyname(socket.gethostname()), self.port))

    def send_message(self, message):
        total_sent = 0
        while total_sent < MSGLEN:
            sent = self.client_socket.send(message[total_sent:].encode())
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent = total_sent + sent

    def run(self):
        time.sleep(1)
        self.connect_to_server()
        self.send_message(MESSAGE)
