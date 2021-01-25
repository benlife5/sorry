# Ben Life
# Copyright 2021
# Licensed under GNU GPLv3 (see COPYING.txt)
#
#  ▄█▀▀▀▄█
#  ██▄▄  ▀    ▄▄▄   ▄▄▄ ▄▄  ▄▄▄ ▄▄   ▄▄▄▄ ▄▄▄
#   ▀▀███▄  ▄█  ▀█▄  ██▀ ▀▀  ██▀ ▀▀   ▀█▄  █
# ▄     ▀██ ██   ██  ██      ██        ▀█▄█
# █▀▄▄▄▄█▀   ▀█▄▄█▀ ▄██▄    ▄██▄        ▀█
#                                    ▄▄ █
#                                     ▀▀
#              VERSION 2.0 BETA
#                  NETWORK

import socket
from _thread import start_new_thread
from random import randint

# Declare IP and Port
HOST = input("Host/IP: ")  # "127.0.0.1"
PORT = int(input("Port: "))  # 65432

# Setup Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print("Sorry Server Active (version 2.0)")

# Server variables
updates = [[], [], [], [], []]
player_num = -1
SEED = randint(0, 1000000)


def threaded_client(conn, player):
    """
    Creates a dedicated server thread for each client.
    :param conn: (socket.socket) The connection to the client.
    :param player: (int) The player ID (1, 2, 3, or 4).
    """
    conn.send(str.encode("Connected: Player " + str(player)))
    print("Started Thread (Player " + str(player) + ")")
    while True:
        # Accept and decode message from client
        data = conn.recv(1024)
        client_message = data.decode("utf-8")

        if not data:  # there is no message
            print("Client Disconnected (Player " + str(player) + ")")
            break
        else:  # there is a message
            # Check which type of message it is
            if client_message == "CHECK_FOR_UPDATE":
                if len(updates[player]) != 0:  # there are available updates
                    conn.send(b"UPDATE")
                    update_to_send = str(updates[player][0][0]) + "," + str(updates[player][0][1])
                    conn.send(str.encode(update_to_send))
                    del updates[player][0]
                else:  # there are no updates
                    conn.send(str.encode("NO_UPDATE"))
            elif client_message == "CLICK":
                conn.send(b"CLICK_ACKNOWLEDGED")
                coord_string = conn.recv(1024).decode("utf-8")  # ask for coordinates
                coords = tuple(coord_string.split(','))
                conn.send(b"COORDS_RECEIVED")
                for player_list in updates:  # update each player
                    player_list.append(coords)
            elif client_message == "SEED":
                conn.send(str.encode(str(SEED)))

    print("Connection Lost (Player " + str(player) + ")")
    print("Game log (all clicks):", updates[-1])
    conn.close()


while True:
    connection, addr = s.accept()  # accept new connections
    print("New Connection:", addr)
    player_num += 1
    if player_num == 4:
        player_num = 0
    start_new_thread(threaded_client, (connection, player_num))
