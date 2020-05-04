from threading import Thread
from queue import Queue
from listener import Listener
from sender import Sender


class ConnectedPlayer(Thread):
    def __init__(self):
        self.sender_queue = Queue()
        self.listener_queue = Queue()
        self.sender = Sender(self.sender_queue)
        self.listener = Listener(self.listener_queue)

    def run(self):
        pass
