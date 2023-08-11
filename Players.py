from socket import socket as Socket
import Colors
from Board import Cell


class Player(object):
    # This keeps track of the number of players
    id: int = 0

    def __init__(self, socket: Socket | None = None):
        self.id = Player.id
        Player.id += 1

        self.color = Colors.random_color()
        self.colored_cells: list[Cell] = []
        self.coloring_now: Cell | None = None

        self.score: int = 0
        self.socket: Socket = socket

    def __eq__(self: 'Player', other: 'Player'):
        return self.id == other.id
    
    def as_dict(self):
        return {
            "id": self.id,
            "color": self.color,
            "score": self.score,
            "cells": [cell.as_dict() for cell in self.colored_cells]
        }
        
    def __str__(self) -> str:
        return "id: {}, color: {}, score: {}, cells: []".format(self.id, self.color, self.score, self.colored_cells)

    def get_color(self):
        return self.color

    def get_id(self):
        return self.id

    def get_history(self):
        return self.colored_cells

    def add_history(self, cell: Cell):
        self.colored_cells.append(cell)

    def get_coloring_now(self):
        return self.coloring_now

    def get_socket(self) -> Socket:
        return self.socket

    def set_coloring_now(self, cell: Cell | None):
        self.coloring_now = cell


