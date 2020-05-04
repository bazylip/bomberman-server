from threading import Thread


class Sender(Thread):
    def __init__(self, port):
        self.port = port

    def send_to_client(self):
        pass

    def run(self):
        pass