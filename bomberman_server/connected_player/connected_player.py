from threading import Thread
from queue import Queue
from bomberman_server.connected_player.listener import Listener
from bomberman_server.connected_player.sender import Sender


class ConnectedPlayer(Thread):
    def __init__(self, id, listening_socket, sending_socket):
        super().__init__()
        self.listener_queue = Queue()
        self.sender_queue = Queue()
        self.listener = Listener(self.listener_queue, listening_socket)
        self.sender = Sender(self.sender_queue, sending_socket)
        self.id = id
        self.location = self.Coordinates(1, 1)
        self.hp = 100

    def start_communication(self):
        self.listener.start()
        self.sender.start()

    def send_message(self, message):
        self.sender_queue.put(message)

    def run(self):
        self.start_communication()
        self.listener.join()
        self.sender.join()

    def change_coordinates(self, x, y):
        self.location.x = x
        self.location.y = y

    def change_health(self, hp):
        self.hp = hp

    class Coordinates:
        def __init__(self, x, y):
            self.x = x
            self.y = y
