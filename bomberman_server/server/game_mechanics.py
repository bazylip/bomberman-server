import json

from bomberman_server.connected_player.connected_player import ConnectedPlayer


class GameMechanics:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board_state = None

    def create_board(self):
        self.board_state = {"player1": self.get_player_info(id=1),
                            "player2": self.get_player_info(id=2),
                            "bombs": {}}

    def json_board(self):
        return json.dumps(self.board_state)

    def get_player_info(self, id):
        player = self.player1 if id == 1 else self.player2
        return player.get_player_info()

    def add_bomb(self, x, y):
        self.board_state["bombs"]["id"] = {"x": x, "y": y}

    def _update_board_state(self):
        new_players_positions = {"player1": self.get_player_info(id=1),
                                   "player2": self.get_player_info(id=2)}
        self.board_state.update(new_players_positions)

    def execute_mechanics(self, action_client1, action_client2):
        for action_dict, player in zip([action_client1, action_client2], [self.player1, self.player2]):
            if action_dict is not None:
                action = eval(action_dict).get("action")
                if action == "up":
                    player.location.y += 1
                elif action == "down":
                    player.location.y -= 1
                elif action == "right":
                    player.location.x += 1
                elif action == "left":
                    player.location.x -= 1
                elif action == "b":
                    self.add_bomb(player.location.x, player.location.y)
        # Placeholder: execute mechanics
        self._update_board_state()
        self.update_players()

    def update_players(self):
        pass