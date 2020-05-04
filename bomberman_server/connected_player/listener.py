from threading import Thread
import socket

MSGLEN = 100


class Listener(Thread):
    def __init__(self, port, queue):
        self.port = port
        self.queue = queue
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((socket.gethostbyname(), self.port))
        self.server_socket = sock

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
