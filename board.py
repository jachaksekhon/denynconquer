
import Colors


class Cell(object):
    height = 50
    width = 50

    def __init__(self, x: int, y: int):
        self.x = x  # x from [0, 9]
        self.y = y  # y from [0, 9]
        self.color = Colors.WHITE
        self.player_id  = -1
        self.isFilled: bool = False
        self.isOccupied: bool = False
        return
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
    def as_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "player_id": self.player_id,
            "is_filled": self.isFilled,
            "is_occupied": self.isOccupied
        }

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_coords(self):
        return (self.x, self.y)

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def get_isFilled(self):
        return self.isFilled

    def set_isFilled(self, isFilled):
        self.isFilled = isFilled

class Board(object):
    def __init__(self):
        self.cells = [[Cell for i in range(10)] for j in range(10)]
        for x in range(10):
            for y in range(10):
                self.cells[x][y] = Cell(x, y)

    def __getitem__(self, key: tuple[int, int]):
        return self.cells[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value):
        self.cells[key[1]][key[0]].set_color(value)
        
    def as_dict(self):
        return [ [Cell(x, y).as_dict() for x in range(10)] for y in range(10)]
    
    def __str__(self):
        string = ""
        for row in self.cells:
            for cell in row:
                string += str(cell) + " "
            string += "\n"
        return string
