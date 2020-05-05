from threading import Thread
import socket

MSGLEN = 100


class Listener(Thread):
    def __init__(self, queue, address="0.0.0.0", port=15000):
        super().__init__()
        self.queue = queue
        self.address = address
        self.port = port
        self.client = None
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        self.server_socket = s

    def listen_for_client(self):
        self.server_socket.listen()
        conn, addr = self.server_socket.accept()
        self.client = conn
        print(f"New connection from client: {addr}")
        return conn, addr

    def receive_message(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.client.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def run(self):
        while True:
            self.queue.put(self.receive_message().decode())
            return
