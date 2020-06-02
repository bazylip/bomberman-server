import json


BOARD_DIMENSION_X = 15
BOARD_DIMENSION_Y = 9
BOMB_TICKS_THRESHOLD = 30
BOMB_EXPLOSION_RANGE = 4
HEALTH_PER_EXPLOSION = 25

class GameMechanics:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.board_state = None

    def reset(self):
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

    def _update_board_state(self):
        new_players_positions = {"player1": self.get_player_info(id=1),
                                   "player2": self.get_player_info(id=2)}
        self.board_state.update(new_players_positions)

    def execute_mechanics(self, action_client1, action_client2):
        self._process_user_action(action_client1, action_client2)
        self._increase_bomb_ticks()
        self._explode_bombs()
        self._update_board_state()
        self.update_players()

    def _process_user_action(self, action_client1, action_client2):
        for action_dict, players in zip([action_client1, action_client2], [(self.player1, self.player2),
                                                                          (self.player2, self.player1)]):
            player, other_player = players[0], players[1]
            if action_dict is not None:
                action = eval(action_dict).get("action")
                if action == "b":
                    self._add_bomb(player.location.x, player.location.y, player.id)
                else:
                    player = self._valid_location(player, other_player, action)

    def _increase_bomb_ticks(self):
        for bomb in self.board_state.get("bombs"):
            bomb["ticks"] += 1

    def _add_bomb(self, x, y, id):
        if id == 1:
            if x != self.player2.location.x or y != self.player2.location.y:
                self.board_state["bombs"].append({"x": x, "y": y, "ticks": 0})
        else:
            if x != self.player1.location.x or y != self.player1.location.y:
                self.board_state["bombs"].append({"x": x, "y": y, "ticks": 0})

    def _explode_bombs(self):
        for bomb in self.board_state.get("bombs"):
            if bomb["ticks"] == BOMB_TICKS_THRESHOLD:
                self._explode_bomb(bomb)

    def _explode_bomb(self, bomb):
        bomb_x, bomb_y = bomb.get("x"), bomb.get("y")
        if bomb_x % 2 == 0:
            y_exploded_fields = range(bomb_y, bomb_y+1)
        else:
            y_exploded_fields = range(bomb_y-BOMB_EXPLOSION_RANGE, bomb_y+BOMB_EXPLOSION_RANGE)
        if bomb_y % 2 == 0:
            x_exploded_fields = range(bomb_x, bomb_x+1)
        else:
            x_exploded_fields = range(bomb_x - BOMB_EXPLOSION_RANGE, bomb_x + BOMB_EXPLOSION_RANGE)

        for players in [self.player1, self.player2]:
            print(f"x_exploded: {x_exploded_fields}, y_exploded: {y_exploded_fields}")
            if (players.location.x == bomb_x and players.location.y in y_exploded_fields) or \
                (players.location.y == bomb_y and players.location.x in x_exploded_fields):
                players.remove_health(HEALTH_PER_EXPLOSION)

        self.board_state["bombs"].remove(bomb)

    def _valid_location(self, player, other_player, action):
        def is_other_player(other_player, x, y):
            return x == other_player.location.x and y == other_player.location.y
        if action == "up":
            if not player.location.x % 2 == 0 and \
                    not player.location.y == BOARD_DIMENSION_Y and \
                    not is_other_player(other_player, player.location.x, player.location.y + 1):
                player.location.y += 1
        elif action == "down":
            if not player.location.x % 2 == 0 and \
                    not player.location.y == 1 and \
                    not is_other_player(other_player, player.location.x, player.location.y - 1):
                player.location.y -= 1
        elif action == "right":
            if not player.location.y % 2 == 0 and \
                    not player.location.x == BOARD_DIMENSION_X and \
                    not is_other_player(other_player, player.location.x + 1, player.location.y):
                player.location.x += 1
        elif action == "left":
            if not player.location.y % 2 == 0 and \
                    not player.location.x == 1 and \
                    not is_other_player(other_player, player.location.x - 1, player.location.y):
                player.location.x -= 1
        return player

    def update_players(self):
        pass

    def check_if_player_died(self):
        if self.player1.hp <= 0:
            return 1
        elif self.player2.hp <= 0:
            return 2
        return None
