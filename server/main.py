import socket  # create socket object, the endpoints for communication via TCP connection
import json  # to encode/decode data transmitted through network. Sockets can only transmit bytes and so we need to
# convert/revert the data into json text and back into python dictionaries
from room import Room
import threading  # multiple users utilizing the server
from protocols import Protocols

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
        # below will be used to store the address of a client that is awaiting an opponent
        self.waiting_for_opponent = None

    def handle_connection(self, client):
        # using While true for multithreaded server allows each client to have its own loop to continue
        # processing messages
        while True:
            # we first send a message to get the clients NICKNAME. Is this the first handshake made by the server
            # ??????????????????????????
            self.send(Protocols.Response.NICKNAME, None, client)
            message = json.loads(client.recv(1024).decode("UTF-8"))
            r_type = message.get("type")
            nickname = message.get("data")

            # verify that the client sent the correct message type containing their nickname and if so assign
            # the name to the client socket object
            if r_type == Protocols.Request.NICKNAME:
                self.client_name[client] = nickname
            # else we continue to repeatedly ask for the correct info
            else:
                continue

            # check to see if we are waiting for an opponent, if no one is waiting for a pair, we will be the first
            # to wait for another player, and so we wait for a room
            if not self.waiting_for_opponent:
                self.waiting_for_opponent = client
                print("Waiting for a room")
            # else we are the second player, and so we create the room to join the first player already waiting
            else:
                self.create_room(client)
            # we have handled the connection so we break from While loop
            break



    # store the two clients that are playing the game
    def create_room(self, client):
        print("Creating a room")
        # create a room with the two players
        room = Room(client, self.waiting_for_opponent)
        # now we need to store each client's opponent in the dictionary, the client and the person who was waiting
        # for their opponent
        self.opponent[client] = self.waiting_for_opponent
        self.opponent[self.waiting_for_opponent] = client
        # notify each player of their opponents nickname
        self.send(Protocols.Response.OPPONENT, self.opponent[client], self.waiting_for_opponent)
        self.send(Protocols.Response.OPPONENT, self.opponent[self.waiting_for_opponent], client)
        # now we store these players in the room dictionary
        self.rooms[client] = room
        self.rooms[self.waiting_for_opponent] = room
        # now that we have paired the person that was waiting for a room into one,
        self.waiting_for_opponent = None







    # client waiting for an opponent
    def wait_for_room(self, client):
        pass

    # determines logic and placement for new clients joining the server
    def handle(self, client):
        self.handle_connection(client)
        self.wait_for_room(client)

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
            # new thread object, pass the handle function and the client as the parameter. We set up a new thread for
            # each new client connecting so that we can continue listening for new clients to accept()
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()




# safeguard needed to prevent the server from starting if script is imported, adds modularity to the class
if __name__ == '__main__':
    game_server = Server()
    server = Server()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
