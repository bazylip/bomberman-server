from listening_server import ListeningServer
from game_mechanics import GameMechanics


class Server(GameMechanics):
    def __init__(self):
        super().__init__()
        self.listening_server = ListeningServer()

    def run_server(self):
        listening_server = ListeningServer()
        print(f"Waiting for players on {listening_server.address}, "
                f"port range: {listening_server.port_range}")
        client1, client2 = listening_server.listen_for_players()
        print(f"Players connected \n{client1}\n{client2}")


if __name__ == "__main__":
    server = Server()
    server.run_server()
