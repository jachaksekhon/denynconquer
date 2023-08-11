
import pickle
import random
from socket import socket
from threading import Lock
from pprint import pprint
import threading
from Players import Player

"""
These are the default values for the server ip and port
You can reuse them in your client code
"""
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555

"""
These are the functions that you can use to send and receive messages from the server
"""

def tcp_send(socket_lock:Lock, socket: socket, message: dict[str, any]):
    # first serialize the message using pickle
    # and then send it to the server or client
    #with socket_lock:
        print(f"\033[32m[+] Sending \033[0m")
        #pprint(message.get('payload'))
        socket.send(pickle.dumps(message))


def tcp_receive(socket_lock:Lock, socket: socket) -> (str, dict[str, any]):
    # first receive the message from the server or client
    # and then deserialize it using pickle
    #with socket_lock:
    message =  pickle.loads(socket.recv(1024*100)) # 1KB is 1024 bytes
    print(f"\033[33m[+] Received \033[0m")
    payload = message.get('payload')
    if 'game_state' not in payload:
        pprint(payload)
        
    return  message.get("type"), payload

def tcp_broadcast(socket_lock:Lock, list: list[Player], message: dict[str, any]):
        print(f"\033[34m[+] Broadcasting to [\033[0m")
    #with socket_lock:
        if len(list) == 0:
            print(f"\033[34m[+]\t\033[0m no players to broadcast to")
        else:
            for p in list:
                print(f"\033[34m[+]\t\033[0m player {p.id}: ", end='')
                p.get_socket().send(pickle.dumps(message))
                print(f"{message.get('payload')}")
        print(f"\033[34m[+] ]\033[0m")


def tcp_receive_non_blocking(socket_lock:Lock, socket: socket) -> (str, dict[str, any]):
    # first receive the message from the server or client
    # and then deserialize it using pickle
    #with socket_lock:

        if socket.recv(2048).__len__() == 0:
            print("Null data being streamed...")


"""
Message Templates to send different types of messages to and from the server,
You can copy paste the templates below to send requests
"""
# requests from the client
on_connection = {}

MOUSE_DOWN = {
    "type": 'MOUSE_DOWN',
    "payload": {
        "player_id": "player_id",
        "col": "col",
        "row": "row",
    }
}
MOUSE_MOTION = {
    "type": 'MOUSE_MOTION',
    "payload": {
        "player_id": "player_id",
        "col": "col",
        "row": "row",
        "x": "x",
        "y": "y",
    }
}
MOUSE_UP = {
    "type": 'MOUSE_UP',
    "payload": {
        "player_id": 'player_id',
        "cell_x": 'cell_x',
        "cell_y": 'cell_y',
    }
}



# response from the server
on_connection = {
    "type": 'ON_CONNECTION',
    "payload": {
        "player_id": "player.id",
        "player_color": "player.color",
        "player_score": "player.score",
        "total_players": 'total_players'
    }
}
