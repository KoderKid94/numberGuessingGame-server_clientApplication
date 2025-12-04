import socket  # create socket object, the endpoints for communication via TCP connection
import json  # to encode/decode data transmitted through network. Sockets can only transmit bytes and so we need to
# convert/revert the data into json text and back into python dictionaries
from room import Room, GuessResult
import threading  # multiple users utilizing the server
from protocols import Protocols
import time
import traceback

class Server:
    # using this host IP to do local testing, the client and server will be hosted on my machine for testing
    def __init__(self, host="127.0.0.1", port=55556):
        self.host = host
        self.port = port
        # the server will hold a AF_INET = IPv4 addresses , SOCK_STREAM =
        # TCP (which defines the transport protocol type) socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow immediate reuse of port after crash/disconnect. After a crash/disconnect macOS holds the port
        # in TIME_WAIT for 90 seconds so this allows the server to use the port even if the TIME_WAIT exists
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self.host, self.port))
        self.server.listen()

        # dictionaries to hold game info
        # map of players names
        self.client_name = {}
        # maps each client to the room object they belong to
        self.rooms = {}
        # maps each client socket to their opponent's client socket (bidirectional pairing)
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
        while True:
            room = self.rooms.get(client)
            opponent = self.opponent.get(client)

            # if we have a room and opponent, we start the game
            if room and opponent:
                # send the correct generated number and start protocols
                self.send(Protocols.Response.CORRECT_NUMBER, room.correct_number, client)
                time.sleep(1)
                self.send(Protocols.Response.START, None, client)
                break



    # determines logic and placement for new clients joining the server
    def handle(self, client):
        self.handle_connection(client)
        self.wait_for_room(client)

        # track json error msg attempts to decide continue/break for connection
        consecutive_json_errors = 0
        max_json_errors = 5

        # buffer to correctly handle and account for all msg data
        buffer = ""

        # main game loop
        while True:
            try:
                data = client.recv(1024).decode("UTF-8")

                # if the data the client sent was empty, disconnected or an error has occurred, break loop
                if not data:
                    break
                buffer += data

                # now we process all complete messages in the buffer, split() splits on the 1st occurrence of '\n'
                # which results in two separate strings, msg_str contains data up until the newline char and
                # the remainder stays in buffer
                while '\n' in buffer:
                    msg_str, buffer = buffer.split('\n', 1)
                    message = json.loads(msg_str)
                    self.handle_received_msg(message, client)

                    # reset json errors if we receive valid data
                    consecutive_json_errors = 0
            except (ConnectionError, ConnectionResetError, BrokenPipeError) as e:
                print(f"Client {self.client_name.get(client, 'unknown')} disconnected: {e}")
                break
            except json.JSONDecodeError as e:

                # if we receive bad data, increment flag
                consecutive_json_errors += 1
                print(f"Invalid JSON from client ({consecutive_json_errors}/{max_json_errors}): {e}")

                # if we have reached sentinel value of too many attempts, disconnect
                if consecutive_json_errors >= max_json_errors:
                    print(
                        f"Client {self.client_name.get(client, 'unknown')} sending too many bad messages, disconnecting")
                    break

                # continue to attempt receiving the correct data
                continue
            except Exception as e:
                # catch unexpected errors but log them
                print(f"Unexpected error handling client: {e}")
                traceback.print_exc()
                break

        self.send_to_opponent(Protocols.Response.OPPONENT_EXITED, None, client)
        self.disconnect_client(client)

    # we need to clean up the room if a client is leaving the game
    def disconnect_client(self, client):
        opponent = self.opponent.get(client)
        # if we have an opponent and a mapping to their client, we delete their mapping
        if opponent in self.opponent:
            del self.opponent[opponent]

        # then delete mapping the other direction
        if client in self.opponent:
            del self.opponent[client]

        # delete the nicknames of client and opponent
        if client in self.client_name:
            del self.client_name[client]

        if opponent in self.client_name:
            del self.client_name[opponent]

        # also delete both players from the room object
        if client in self.rooms:
            del self.rooms[client]

        if opponent in self.rooms:
            del self.rooms[opponent]

        # try to close the socket gracefully by ending read and write between client/server
        # this way we give data the opportunity to transmit before closing the socket
        try:
            client.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"Shutdown error: {e}")
            pass

        client.close()

    # handle messages received from clients depending on which type of msg was received
    def handle_received_msg(self, message, client):
        r_type = message.get("type")
        data = message.get("data")
        room = self.rooms[client]

        if r_type != Protocols.Request.ANSWER:
            return

        result = room.verify_guess(data)

        if  result == GuessResult.GAME_OVER:
            return

        # the guess was too low
        if result == GuessResult.TOO_LOW:
            self.send(Protocols.Response.GUESS_TOO_LOW, None, client)

        # the guess was too high
        elif result == GuessResult.TOO_HIGH:
            self.send(Protocols.Response.GUESS_TOO_HIGH, None, client)

        # the guess was the correct number
        elif result == GuessResult.CORRECT:
            # get the winner and opponents name
            winners_name = self.client_name.get(client)

           # reveal winner and correct number
            self.send(Protocols.Response.GUESS_VALID, None, client)
            self.send(Protocols.Response.WINNER, winners_name, client)
            self.send_to_opponent(Protocols.Response.WINNER, winners_name, client)
            self.send_to_opponent(Protocols.Response.CORRECT_NUMBER, room.correct_number, client)

            # we need to update the database

    # consider adding a send_to_both helper function###########
    def send(self, r_type, data, client):
        try:
            message = {"type": r_type, "data": data}
            # because TCP does not hold message boundaries, we add a newline delimiter
            message = json.dumps(message).encode("UTF-8") + b"\n"
            client.send(message)
        except Exception as e:
            print(f"Error sending message to the client: {e}")
            self.disconnect_client(client)


    # to send messages to a clients opponent, EX: opponent has left game, won or lost
    def send_to_opponent(self, r_type, data, client):
        opponent = self.opponent.get(client)

        if not opponent:
            return
        self.send(r_type, data, opponent)

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
if __name__ == "__main__":
    server = Server()
    server.receive()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
