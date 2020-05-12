from threading import Thread
from queue import Queue
from listener import Listener
from sender import Sender


class ConnectedPlayer(Thread):
    def __init__(self, port, id):
        super().__init__()
        self.listener_queue = Queue()
        self.sender_queue = Queue()
        self.listener = Listener(self.listener_queue, port=port)
        self.sender = Sender(self.sender_queue, port=port)
        self.id = id
        self.location = self.Coordinates(1, 1)
        self.health = 100

    def listen_for_new_player(self):
        self.listener.start()
        self.sender.start()

    def run(self):
        self.listen_for_new_player()
        self.sender_queue.put("wiadomosc")
        print(f"Listener queue: {self.listener_queue.get()}")
        self.sender_queue.put("end")
        print(f"Listener queue: {self.listener_queue.get()}")
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


if __name__ == "__main__":
    player = ConnectedPlayer(15001, 1)
    player.start()
    player.join()
