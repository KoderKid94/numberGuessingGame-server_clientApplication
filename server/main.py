import socket  # create socket object, the endpoints for communication via TCP connection
import json  # to encode/decode data transmitted through network. Sockets can only transmit bytes and so we need to
# convert/revert the data into json text and back into python dictionaries

import threading  # multiple users utilizing the server


class Server:
    # using this host IP to do local testing, the client and server will be hosted on my machine for testing
    def __init__(self, host="127.0.0.1", port="55555"):
        self.host = host
        self.port = port
        # the server will hold a AF_INET = IPv4 addresses , SOCK_STREAM =
        # TCP (which defines the transport protocol type) socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.host, self.port)
        self.server.listen()

        # dictionaries to hold game info
        self.client_name = {}
        self.rooms = {}
        self.opponent = {}
        # dictionary below will be used to store the address of a client that is awaiting an opponent
        self.waiting_for_opponent = None

    def handle_connection(self):
        pass

    # store the two clients that are playing the game
    def create_room(self, client):
        pass

    # client waiting for an opponent
    def wait_for_room(self, client):
        pass

    # determines logic and placement for new clients joining the server
    def handle(self, client):
        pass

    def disconnect_client(self, client):
        pass

    # handle messages received from clients
    def handle_received_msg(self, message, client):
        pass

    # r_type = request type
    def send(self, r_type, data, client):
        pass

    # to send messages to a clients opponent, EX: opponent has left game, won or lost
    def send_to_opponent(self, r_type, data, client):
        pass

    # because we have one thread listening for new clients, we use this method to allow new client requests to
    # connect to the server by being passed to handle()
    def receive(self):
        while True:
            # wait until we get a connection before proceeding
            client, address = self.server.accept()
            # print address that has connected
            print(f"Connected with {address}")
            # new thread object, pass the handle function and the client as the parameter. The comma is necessary to
            # send a single parameter as tuple. We set up a new thread for each new client connecting so that we can
            # continue listening for new clients to accept()
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()




# safeguard needed to prevent the server from starting if script is imported, adds modularity to the class
if __name__ == '__main__':
    game_server = Server()
    server = Server()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
