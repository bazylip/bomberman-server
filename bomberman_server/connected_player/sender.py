from threading import Thread
import socket

MSGLEN = 200


class Sender(Thread):
    def __init__(self, queue, socket):
        super().__init__()
        self.queue = queue
        self.socket = socket

    def send_to_client(self, message):
        total_sent = 0
        message = message.zfill(MSGLEN)
        while total_sent < MSGLEN:
            sent = self.socket.send(message[total_sent:].encode())
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent = total_sent + sent

    def run(self):
        while True:
            message = self.queue.get()
            if message == "end server":
                break
            self.send_to_client(message)
        self.socket.close()
