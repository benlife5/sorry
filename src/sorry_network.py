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


class Network:
    """
    A class for networking the game Sorry!
    Attributes:
        client: (socket.socket) A socket object.
        server: (str) The IP address.
        port: (int) The port number.
        addr: (tuple) The (server, port) tuple.
    Methods:
        .connect(): Create a connection to the server.
        .send(data): Send data to the server and get a reply.
        .check_for_update(): Check for any updates from the server.
    """
    def __init__(self, server, port):
        """
        Creates a Network object.
        :param server: (str) The IP address.
        :param port: (int) The port number.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)

    def connect(self):
        """
        Create a connection to a server.
        :return: The server's connection message.
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        """
        Send data to the server and receive a reply.
        :param data: The data to be sent to the server.
        :return: The server's reply.
        """
        try:
            # print("Sending:", data)
            self.client.send(str.encode(str(data)))
            return self.client.recv(2048).decode("utf-8")
        except socket.error as e:
            print(e)

    def check_for_update(self):
        """
        Check if the server has any updates.
        :return: The server's update (or None).
        """
        try:
            self.client.send(str.encode("CHECK_FOR_UPDATE"))  # Request a check from the server
            update = self.client.recv(2048).decode("utf-8")  # NO_UPDATE, or update
            if update == "NO_UPDATE":
                return None
            elif update == "UPDATE":
                response = self.client.recv(2048).decode("utf-8")
                coords = response.split(',')
                return int(coords[0]), int(coords[1])
        except socket.error as e:
            print(e)
