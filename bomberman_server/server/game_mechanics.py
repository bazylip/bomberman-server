import json

from bomberman_server.connected_player.connected_player import ConnectedPlayer


class GameMechanics:
    def __init__(self):
        self.player1 = None
        self.player2 = None

    def get_player_info(self, id):
        player = self.player1 if id == 1 else self.player2
        dict_info = {"id": id,
                "x": player.location.x,
                "y": player.location.y,
                "hp": player.hp}
        json_info = json.dumps(dict_info)
        return json_info