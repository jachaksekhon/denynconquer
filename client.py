# importing the required libraries
import socket
import threading
import pygame as pg
import sys
import time
from pygame.locals import *

from Connection import SERVER_IP, SERVER_PORT, tcp_receive, tcp_send, tcp_receive_non_blocking
import Colors

from GameState import GameState

# storing the winner's value at
# any instant of code
winner = None
draw = None
width = 600
height = 600
banner_height = 100
num_rows = 10
client_socket_lock = threading.Lock()


game_state = None
playerData = None
game_state_checker = None

# Player Specific Variables
player_id, player_color, player_score, total_players = 0, 0, 0, 0

# Pygame Stuff
pg.init()
fps = 30
# this method is used to build the infrastructure of the display
screen: pg.Surface = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Deny and Conquer")


# Define a function to convert the string representation of color to a tuple
def color_string_to_tuple(color_string):
    color_values = color_string.strip('()').split(', ')
    return tuple(map(int, color_values))


def drawGrid():
    for i in range(0, num_rows):
        pg.draw.line(screen, Colors.BLACK, (width / num_rows * (i + 1), 0), (width / num_rows * (i + 1), height), 4)

    for i in range(0, num_rows):
        pg.draw.line(screen, Colors.BLACK, (0, height / num_rows * (i + 1)), (width, height / num_rows * (i + 1)), 4)


def game_initiating_window(player_id):
    pg.display.update()
    screen.fill(Colors.WHITE)

    drawGrid()

    font = pg.font.Font(None, 30)

    # setting the font properties like color and width of the text
    text = font.render(f"Welcome Player {player_id}", 1, (255, 255, 255))

    # copy the rendered message onto the board
    # creating a small block at the bottom of the main display
    screen.fill(Colors.BLACK, (0, height, width, banner_height))
    rect = text.get_rect()
    rect.center = (width / 2, height + banner_height / 2)
    screen.blit(text, rect)
    pg.display.update()


def check_win():
    None


def get_cell_clicked(x: float, y: float) -> tuple[int, int]:
    # out of the 10 * 10 board find the coordinates of the cell
    if x < width / num_rows:
        col = 0
    elif x < width / num_rows * 2:
        col = 1
    elif x < width / num_rows * 3:
        col = 2
    elif x < width / num_rows * 4:
        col = 3
    elif x < width / num_rows * 5:
        col = 4
    elif x < width / num_rows * 6:
        col = 5
    elif x < width / num_rows * 7:
        col = 6
    elif x < width / num_rows * 8:
        col = 7
    elif x < width / num_rows * 9:
        col = 8
    elif x < width / num_rows * 10:
        col = 9
    else:
        col = -1

    if y < width / num_rows:
        row = 0
    elif y < width / num_rows * 2:
        row = 1
    elif y < width / num_rows * 3:
        row = 2
    elif y < width / num_rows * 4:
        row = 3
    elif y < width / num_rows * 5:
        row = 4
    elif y < width / num_rows * 6:
        row = 5
    elif y < width / num_rows * 7:
        row = 6
    elif y < width / num_rows * 8:
        row = 7
    elif y < width / num_rows * 9:
        row = 8
    elif y < width / num_rows * 10:
        row = 9
    else:
        row = -1

    if col < 0 or row < 0:
        print("You clicked out of the board")
        return
    return col, row


def get_cell_boundaries(col: int, row: int):
    cell_width = width / num_rows
    cell_height = height / num_rows

    left = col * cell_width
    right = (col + 1) * cell_width
    top = row * cell_height
    bottom = (row + 1) * cell_height

    return top, right, bottom, left


def reset_game():
    None


def get_cell(col, row):
    global game_state_checker
    return game_state_checker['board'][col][row]


def is_occupied(col, row):
    return get_cell(col, row)['is_occupied']


def is_filled(col, row):
    return get_cell(col, row)['is_filled']


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_IP, SERVER_PORT))

    # Once you connect to the server, you will receive a player ID
    type, message = tcp_receive(client_socket_lock, server_socket)

    server_socket.setblocking(0)
    server_socket.settimeout(0.001)

    
    player_score = message.get('player').get('score')
    player_id = message.get('player').get('id')
    player_color = color_string_to_tuple(message.get('player').get('color'))

    global game_state
    game_state = message.get('game_state')

    game_initiating_window(player_id)

    # this is used to track time
    CLOCK = pg.time.Clock()
    row, col = 0, 0
    x, y = 0, 0  # coordinates of the cell clicked
    top, right, bottom, left = 0, 0, 0, 0  # boundaries of the cell clicked

    strokes = []
    drawing = False

    while (True):
        pg.display.update()
        CLOCK.tick(fps)

        try:
            data = tcp_receive(client_socket_lock, server_socket)

            global playerData
            mouseAction, playerData = data

            global game_state_checker
            game_state_checker = playerData['game_state']

            if (mouseAction == "MOUSE_MOTION"):
                opp_player_id = playerData['player_id']
                opp_player_x = playerData['x']
                opp_player_y = playerData['y']

                opp_player_color_str = playerData['player_color']
                opp_player_color = color_string_to_tuple(opp_player_color_str)
                opp_last_drawn_pixel = pg.Rect(opp_player_x, opp_player_y, 3, 3)
                pg.draw.rect(screen, opp_player_color, opp_last_drawn_pixel)
                drawGrid()

            elif (mouseAction == "MOUSE_DOWN"):
                opp_player_id = playerData['player_id']

            elif (mouseAction == "MOUSE_UP"):
                opp_player_id = playerData['player_id']
                opp_player_left = playerData['pixel_left']
                opp_player_top = playerData['pixel_top']
                opp_player_isSquareFilled = playerData['player_square_filled']

                opp_player_color_str = playerData['player_color']
                opp_player_color = color_string_to_tuple(opp_player_color_str)

                opp_areaToBeFilled = (opp_player_left, opp_player_top, 58, 58)

                if (opp_player_isSquareFilled == True):
                    pg.draw.rect(screen, opp_player_color, opp_areaToBeFilled)
                    drawGrid()
                else:
                    pg.draw.rect(screen, (255, 255, 255), opp_areaToBeFilled)
                    drawGrid()
        except TimeoutError:
            pass

        if game_state_checker is None:
            game_state_checker = game_state
        else:
            pass


        for event in pg.event.get():

            if event.type == QUIT:
                pg.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()

                if x < width and y < height:
                    col, row = get_cell_clicked(x, y)
                    top, right, bottom, left = get_cell_boundaries(col, row)

                    if game_state_checker is None:
                        pass
                    else:
                        if game_state_checker['board'][col][row]['is_filled']:
                            continue
                        elif game_state_checker['board'][col][row]['is_occupied']:
                            if game_state_checker['board'][col][row]['player_id'] != player_id:
                                continue

                    drawing = True
                    with client_socket_lock:
                        get_cell(col, row)['is_occupied'] = True
                        
                    tcp_send(client_socket_lock, server_socket, {
                        "type": 'MOUSE_DOWN',
                        "payload": {
                            "player_id": player_id,
                            "player_color": player_color.__str__(),
                            "col": col,
                            "row": row,
                            "game_state": game_state_checker
                        }
                    })

            elif event.type == MOUSEMOTION and drawing:
                x, y = pg.mouse.get_pos()

                if left < x < right and top < y < bottom:
                    temp_rect = pg.Rect(x, y, 3, 3)
                    pg.draw.rect(screen, player_color, temp_rect)
                    drawGrid()  # so that the dots are not on the lines
                    strokes.append(temp_rect)

                    get_cell(col, row)["is_occupied"] = True
                    get_cell(col, row)["player_id"] = player_id
                    get_cell(col, row)["color"] = player_color

                    tcp_send(client_socket_lock, server_socket, {
                        "type": 'MOUSE_MOTION',
                        "payload": {
                            "player_id": player_id,
                            "player_color": player_color.__str__(),
                            "col": col,
                            "row": row,
                            "x": x,
                            "y": y,
                            "game_state": game_state_checker
                        }
                    })

                # Update the display with each tick
                pg.display.update()
                CLOCK.tick(fps)

            elif event.type == MOUSEBUTTONUP:

                # josh-debug
                if game_state_checker is None:
                    pass
                else:
                    if game_state_checker['board'][col][row]['is_filled']:
                        continue
                    elif game_state_checker['board'][col][row]['is_occupied']:
                        if game_state_checker['board'][col][row]['player_id'] != player_id:
                            continue

                areaToBeFilled = (left + 1, top + 1, 58, 58)
                areaColor = (255, 255, 255)
                isSquareFilled = False
                drawing = False
                get_cell(col, row)["is_occupied"] = False

                if len(strokes) >= 15:
                    areaColor = player_color
                    isSquareFilled = True
                    get_cell(col, row)["is_filled"] = True

                    # Changes the cell of the board in the GameState
                    get_cell(col, row)["player_id"] = player_id
                    get_cell(col, row)["color"] = player_color
                else:
                    get_cell(col, row)["is_filled"] = False

                pg.draw.rect(screen, areaColor, areaToBeFilled)

                tcp_send(client_socket_lock, server_socket, {
                    "type": 'MOUSE_UP',
                    "payload": {
                        "player_id": player_id,
                        "player_square_filled": isSquareFilled,
                        "player_color": player_color.__str__(),
                        "col": col,
                        "row": row,
                        "x": x,
                        "y": y,
                        "pixel_left": left + 1,
                        "pixel_top": top + 1,
                        "game_state": game_state_checker
                    }
                })

                row, col = 0, 0
                x, y = 0, 0  # coordinates of the cell clicked
                top, right, bottom, left = 0, 0, 0, 0  #
                strokes = []
                drawGrid()


main()
