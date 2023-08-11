import random

def random_color():
    return random.choice([
        RED,
        GREEN,
        BLUE,
        CYAN,
        MAGENTA,
        ORANGE,
        VIOLET,
        PINK
    ])


# -----------------------------------------------------------------------

# Some predefined Color objects:

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)

RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)

CYAN = (0, 255, 255)
MAGENTA = (255,   0, 255)

GRAY = (128, 128, 128)

ORANGE = (255, 200,   0)
VIOLET = (238, 130, 238)
PINK = (255, 175, 175)
