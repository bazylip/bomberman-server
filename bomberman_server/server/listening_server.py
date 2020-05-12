import socket


class ListeningServer:
    def __init__(self, address="0.0.0.0", port_range=[15000, 15001]):
        self.address = address
        self.port_range = port_range

    def listen_for_players(self):
        def create_listening_socket(address, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((address, port))
            s.listen()
            client, addr = s.accept()
            print(f"New connection from client: {addr}")
            return s, client

        def create_sending_socket(address, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.address, self.port))
            self.client_socket = s
            print(f"Connected to {address} on {port}")
            return s

        listening_socket_1, client_1 = create_listening_socket(
            self.address, self.port_range[0])
        listening_socket_2, client_2 = create_listening_socket(
            self.address, self.port_range[1])

        sending_socket_1 = create_sending_socket(
            self.address, self.port_range[0])
        sending_socket_2 = create_sending_socket(
            self.address, self.port_range[1])

        return (listening_socket_1, client_1,
                sending_socket_1), (listening_socket_2, client_2, sending_socket_2)
