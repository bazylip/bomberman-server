import time

from bomberman_server.server.listening_server import ListeningServer
from bomberman_server.server.game_mechanics import GameMechanics
from bomberman_server.connected_player.connected_player import ConnectedPlayer


class Server(GameMechanics):
    def __init__(self):
        super().__init__()
        self.listening_server = ListeningServer()

    def start_server(self):
        self.reset()
        listening_server = ListeningServer()
        print(f"Waiting for players on {listening_server.address}, "
              f"listening port: {listening_server.listening_port}")
        client1, client2 = listening_server.listen_for_players()
        self.player1 = ConnectedPlayer(1, client1[0], client1[1])
        self.player2 = ConnectedPlayer(2, client2[0], client2[1])
        self.player1.start()
        self.player2.start()
        self.create_board()
        print(f"Players connected \n{client1}\n{client2}")

    def send_info_to_player(self, id, message):
        self.player1.send_message(message) if id == 1 else self.player2.send_message(message)

    def send_info_to_both_players(self, message):
        self.send_info_to_player(1, message)
        self.send_info_to_player(2, message)

    def send_initial_info(self):
        self.send_info_to_player(id=1, message=self.player1.get_json_player_info())
        self.send_info_to_player(id=2, message=self.player2.get_json_player_info())

    def close_connection_with_players(self):
        print("Closing connection with players")
        self.send_info_to_both_players("end client")

    def shutdown(self):
        print("Shutting down...")
        self.send_info_to_both_players("end server")

    def get_actions_from_players(self):
        message_client1 = self.player1.get_action_from_client()
        message_client2 = self.player2.get_action_from_client()
        return message_client1, message_client2

    def game_loop(self):
        while True:
            self.start_server()
            self.send_initial_info()
            print_tick = 0
            while True:
                action_client1, action_client2 = self.get_actions_from_players()
                if not self.player1.is_alive() or not self.player2.is_alive():
                    break
                self.execute_mechanics(action_client1, action_client2)
                game_ended = self.check_if_player_died()
                if game_ended is not None:
                    player_won = 1 if game_ended == 2 else 2
                    print(f"Game ended, player {player_won} has won")
                    self.send_info_to_both_players(f"game over {player_won}")
                    break
                self.send_info_to_both_players(self.json_board())
                print_tick += 1
                if print_tick == 20:
                    print(self.json_board())
                    print_tick = 0
                time.sleep(0.03)
            self.close_connection_with_players()
        time.sleep(1)
        self.shutdown()

