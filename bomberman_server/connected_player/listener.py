from threading import Thread
import socket

MSGLEN = 100


class Listener(Thread):
    def __init__(self, queue, address=socket.gethostbyname(), port=1500):
        self.queue = queue
        self.address = address
        self.port = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.address, self.port))
        self.server_socket = s

    def listen_from_client(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.server_socket.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def run(self):
        while True:
            self.queue.put(self.listen_from_client())
