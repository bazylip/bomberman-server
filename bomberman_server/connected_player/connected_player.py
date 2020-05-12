from threading import Thread
from queue import Queue
from listener import Listener
from sender import Sender


class ConnectedPlayer(Thread):
    def __init__(self, id, listening_socket, client, sending_socket):
        super().__init__()
        self.listener_queue = Queue()
        self.sender_queue = Queue()
        self.listener = Listener(self.listener_queue, listening_socket, client)
        self.sender = Sender(self.sender_queue, sending_socket)
        self.id = id
        self.location = self.Coordinates(1, 1)
        self.health = 100

    def start_communication(self):
        self.listener.start()
        self.sender.start()

    def run(self):
        self.start_communication()
        self.listener.join()
        self.sender.join()

    def change_coordinates(self, x, y):
        self.location.x = x
        self.location.y = y

    def change_health(self, health):
        self.health = health

    class Coordinates:
        def __init__(self, x, y):
            self.x = x
            self.y = y
