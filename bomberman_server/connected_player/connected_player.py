import json
from threading import Thread
from queue import Queue
from bomberman_server.connected_player.listener import Listener
from bomberman_server.connected_player.sender import Sender


class ConnectedPlayer(Thread):
    def __init__(self, id, listening_socket, sending_socket):
        super().__init__()
        self.listening_queue = Queue()
        self.sending_queue = Queue()
        self.listener = Listener(self.listening_queue, listening_socket)
        self.sender = Sender(self.sending_queue, sending_socket)
        self.id = id
        self.location = self.Coordinates(1, 1)
        self.hp = 100

    def start_communication(self):
        self.listener.start()
        self.sender.start()

    def send_message(self, message):
        self.sending_queue.put(message)

    def get_action_from_client(self):
        message = None
        if not self.listening_queue.empty():
            message = self.listening_queue.get()
        return message

    def run(self):
        self.start_communication()
        self.listener.join()
        self.sender.join()

    def change_coordinates(self, x, y):
        self.location.x = x
        self.location.y = y

    def remove_health(self, value):
        self.hp -= value

    def get_player_info(self):
        dict_info = {"id": self.id,
                     "x": self.location.x,
                     "y": self.location.y,
                     "hp": self.hp}
        return dict_info

    def get_json_player_info(self):
        return json.dumps(self.get_player_info())

    class Coordinates:
        def __init__(self, x, y):
            self.x = x
            self.y = y
