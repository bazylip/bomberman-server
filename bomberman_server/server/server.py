from bomberman_server.server.listening_server import ListeningServer
from bomberman_server.server.game_mechanics import GameMechanics
from bomberman_server.connected_player.connected_player import ConnectedPlayer


class Server(GameMechanics):
    def __init__(self):
        super().__init__()
        self.listening_server = ListeningServer()

    def run_server(self):
        listening_server = ListeningServer()
        print(f"Waiting for players on {listening_server.address}, "
              f"port range: {listening_server.listening_port}")
        client1, client2 = listening_server.listen_for_players()
        self.player1 = ConnectedPlayer(1, client1[0], client1[1])
        self.player2 = ConnectedPlayer(2, client2[0], client2[1])
        self.player1.start()
        self.player2.start()
        print(f"Players connected \n{client1}\n{client2}")

    def send_info_to_player(self, id, message):
        self.player1.send_message(message) if id == 1 else self.player2.send_message(message)

    def send_info_to_both_players(self, message):
        self.send_info_to_player(id=1, message=message)
        self.send_info_to_player(id=2, message=message)

    def close_connection_with_players(self):
        self.send_info_to_both_players("end client")

if __name__ == "__main__":
    server = Server()
    server.run_server()
    server.send_info_to_player(id=1, message=server.get_player_info(id=1))
    server.send_info_to_player(id=2, message=server.get_player_info(id=2))
    server.close_connection_with_players()