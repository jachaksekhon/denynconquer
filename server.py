import socket
from _thread import *
import threading
from GameState import GameState
from Players import Player
from Connection import SERVER_IP, SERVER_PORT, tcp_broadcast, tcp_receive, tcp_send
from Board import Board

# 'game' contain the Board and the list of players playing the game
game = GameState()
server_socket_lock = threading.Lock()

def run_server(IP, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind((IP, PORT))
        except socket.error as e:
            print(str(e))

        server_socket.listen()
        print(f"[+] Listenting on {IP}:{PORT}")

        while True:  # Loop and wait for incoming connections
            client_socket, client_address = server_socket.accept()

            #joshua debug
            client_socket.setblocking(0)
            client_socket.settimeout(0.001)

            print(f"[+] Accepted connection from {client_address}")

            # Make a new player and send it to the client
            # Every player stores its own socket (used in multithreading)
            player = Player(client_socket)
            game.join(player)
            
            

            print(f"[+] Player {player.id} has joined the game")
            
            tcp_send(server_socket_lock, client_socket, {
                "type": 'ON_CONNECTION',
                "payload": {
                    "game_state": game.as_dict(),
                    "player": {
                        "id": player.id,
                        "color": player.color.__str__(),
                        "score": player.score,
                    },
                }
            })

            # Start a new thread that will listen for incoming messages from the client
            start_new_thread(on_message, (client_socket, player))


def on_message(client_socket: socket.socket, player: Player):
    # Since all the threads are sharing a server socket, we need to lock it
    

    while True:
        print("[=] Waiting for a message...")

        try:
            type, message = tcp_receive(server_socket_lock, client_socket)
            if not message:
                game.leave(player)
                print(f"[-] Player {player.id} has left the game")
                break
            else:
                send_to = list(filter(lambda p: p.id != player.id, game.get_all_players()))

                match type:

                    case 'NO_ACTION':
                        tcp_broadcast(server_socket_lock, send_to, {
                            "type": "NO_ACTION",
                            "payload": message
                        })
                        continue

                    case 'MOUSE_DOWN':
                        print(f"[+] {player.id} is broadcasting MOUSE_DOWN")
                        tcp_broadcast(server_socket_lock, send_to, {
                            "type": "MOUSE_DOWN",
                            "payload": message
                        })

                        continue

                    case 'MOUSE_MOTION':
                        print(f"[+] {player.id} is broadcasting MOUSE_MOTION")
                        tcp_broadcast(server_socket_lock, send_to, {
                            "type": "MOUSE_MOTION",
                            "payload": message,
                        })

                        continue

                    case 'MOUSE_UP':
                        print(f"[+] {player.id} is broadcasting MOUSE_UP")
                        tcp_broadcast(server_socket_lock, send_to, {
                            "type": "MOUSE_UP",
                            "payload": message
                        })
                        continue

                    case 'ABORT_COLORING':
                        break
        except TimeoutError:
            print("No players are currently drawing...")

    print(f"[-] {player.id} has lost connection")
    game.leave(player)
    
    client_socket.close()

if __name__ == '__main__':
    # This might need to be changed, depending on the machine this program is being run
    run_server(SERVER_IP, SERVER_PORT)
