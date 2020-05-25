import json

from bomberman_server.connected_player.connected_player import ConnectedPlayer

BOARD_DIMENSION_Y = 9
BOARD_DIMENSION_X = 15
BOMB_TICKS_THRESHOLD = 300000

class GameMechanics:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board_state = None

    def create_board(self):
        self.board_state = {"player1": self.get_player_info(id=1),
                            "player2": self.get_player_info(id=2),
                            "bombs": []}

    def json_board(self):
        return json.dumps(self.board_state)

    def get_player_info(self, id):
        player = self.player1 if id == 1 else self.player2
        return player.get_player_info()

    def add_bomb(self, x, y):
        self.board_state["bombs"].append({"x": x, "y": y, "ticks": 0})

    def _update_board_state(self):
        new_players_positions = {"player1": self.get_player_info(id=1),
                                   "player2": self.get_player_info(id=2)}
        self.board_state.update(new_players_positions)

    def execute_mechanics(self, action_client1, action_client2):
        self._process_user_action(action_client1, action_client2)
        self._increase_bomb_ticks()
        self._explode_bombs()
        # Placeholder: execute mechanics
        self._update_board_state()
        self.update_players()

    def _process_user_action(self, action_client1, action_client2):
        for action_dict, player in zip([action_client1, action_client2], [self.player1, self.player2]):
            if action_dict is not None:
                action = eval(action_dict).get("action")
                if action == "b":
                    self.add_bomb(player.location.x, player.location.y)
                else:
                    player = self._valid_location(player, action)

    def _increase_bomb_ticks(self):
        for bomb in self.board_state.get("bombs"):
            bomb["ticks"] += 1

    def _explode_bombs(self):
        for bomb in self.board_state.get("bombs"):
            if bomb["ticks"] == BOMB_TICKS_THRESHOLD:
                #TODO: add bomb explosion
                self.board_state["bombs"].remove(bomb)

    def _valid_location(self, player, action):
        if action == "up":
            if not player.location.x % 2 == 0 and not player.location.y == BOARD_DIMENSION_Y:
                player.location.y += 1
        elif action == "down":
            if not player.location.x % 2 == 0 and not player.location.y == 1:
                player.location.y -= 1
        elif action == "right":
            if not player.location.y % 2 == 0 and not player.location.x == BOARD_DIMENSION_X:
                player.location.x += 1
        elif action == "left":
            if not player.location.y % 2 == 0 and not player.location.x == 1:
                player.location.x -= 1
        return player

    def update_players(self):
        pass