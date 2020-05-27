from threading import Thread
import socket

MSGLEN = 500


class Listener(Thread):
    def __init__(self, queue, socket):
        super().__init__()
        self.queue = queue
        self.socket = socket

    def receive_message(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.socket.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        message = b''.join(chunks)
        message = message.decode().lstrip("0")
        return message

    def run(self):
        while True:
            try:
                message = self.receive_message()
                self.queue.put(message)
            except:
                print("Client has disconnected")
                self.socket.close()
                break