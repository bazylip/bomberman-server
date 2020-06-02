import socket


class ListeningServer:
    def __init__(
            self,
            address="0.0.0.0",
            listening_port=15000,
            client_port=15000):
        self.address = address
        self.listening_port = listening_port
        self.client_port = client_port

    def listen_for_players(self):
        def create_listening_socket(address, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((address, port))
            s.listen()
            client, addr = s.accept()
            print(f"New connection from client: {addr}")
            return client, addr

        def create_sending_socket(address, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, port))
            self.client_socket = s
            print(f"Connected to {address} on {port}")
            return s

        listening_socket_1, addr1 = create_listening_socket(
            self.address, self.listening_port)
        sending_socket_1 = create_sending_socket(addr1[0], self.client_port)
        listening_socket_2, addr2 = create_listening_socket(
            self.address, self.listening_port)
        sending_socket_2 = create_sending_socket(addr2[0], self.client_port)

        return (listening_socket_1, sending_socket_1), \
               (listening_socket_2, sending_socket_2)
