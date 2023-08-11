import socket
from Players import Player
from Board import Board


class GameState(object):
    def __init__(self):
        self.Players: list[Player] = []
        self.Board = Board()
        
    def as_dict(self):
        return {
            "players": [p.as_dict() for p in self.Players],
            "board": self.Board.as_dict()
        }

    def join(self, player: Player):
        self.Players.append(player)
        return

    def leave(self, player: Player):
        self.Players.remove(player)

    def get_board(self) -> Board:
        return self.Board

    def get_player(self, id: int) -> Player | None:
        for player in self.Players:
            if player.get_id() == id:
                return player
        return None

    def get_all_players(self) -> list[Player]:
        return self.Players

    def get_all_players_socket(self) -> list[socket.socket]:
        list_sockets = []
        for p in self.Players:
            list_sockets.append(p.socket)

        return list_sockets
