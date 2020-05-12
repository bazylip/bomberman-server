from threading import Thread
import socket

MSGLEN = 100


class Sender(Thread):
    def __init__(self, queue, address=socket.gethostbyname(socket.gethostname()), port=1500):
        super().__init__()
        self.queue = queue
        self.address = address
        self.port = port

    def connect_to_client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))
        self.client_socket = s
        print(f"Connected to {self.address} on {self.port}")

    def send_to_client(self, message):
        total_sent = 0
        message = message.zfill(MSGLEN)
        while total_sent < MSGLEN:
            sent = self.client_socket.send(message[total_sent:].encode())
            print(f"Sent: {sent}")
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent = total_sent + sent

    def run(self):
        self.connect_to_client()
        while True:
            message = self.queue.get()
            self.send_to_client(message)
            if message == "end":
                break
        self.client_socket.close()