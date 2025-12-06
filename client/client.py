import socket
import threading
import json
from protocols import Protocols
import traceback

class Client:
    def __init__(self, host = "127.0.0.1", port = 55556):
        self.nickname = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

        self.closed = False
        self.started = False
        self.opponent_name = None
        self.winner = None
        self.correct_number = None
        self.game_over = False

    def start(self):
        # we want to receive all data on a separate thread for each client
        recv_thread = threading.Thread(target=self.receive)
        recv_thread.start()

    def send(self, request, message):
        data = {"type": request, "data": message}
        self.server.send((json.dumps(data) + "\n").encode("UTF-8"))

    def receive(self):
        # because we use the newline char for better readability when receiving messages from the server, we need to
        # use a buffer to handle this on the client side because we may receive more/less than 1024 bytes and will
        # parse the data from that buffer
        buffer = ""
        while not self.closed:
            try:
                data = self.server.recv(1024).decode("UTF-8")
                # we may need to close the connection gracefully
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    self.handle_response(json.loads(message))
            except (ConnectionError, ConnectionResetError, BrokenPipeError):
                    print("Lost connection to server")
                    break
            except json.JSONDecodeError as e:
                print(f"Received invalid data: {e}")
                # we continue because we can still recover if valid data arrives
                continue
            except UnicodeDecodeError as e:
                print(f"Received non-UTF8 data: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                traceback.print_exc()
                break

        # if we break out of loop we close
        self.close_conn()


    def close_conn(self):
        self.closed = True
        try:
            self.server.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.server.close()

    def handle_response(self, response):
        r_type = response.get("type")
        data = response.get("data")

        if r_type == Protocols.Response.GUESS_TOO_LOW:
            print("Your guess was too low.")

        elif r_type == Protocols.Response.GUESS_TOO_HIGH:
            print("Your guess was too high.")

        elif r_type == Protocols.Response.GUESS_VALID:
            print("Your guess was correct!")

        elif r_type == Protocols.Response.WINNER:
            print(f"You win! Winner: {data}")

        elif r_type == Protocols.Response.OPPONENT:
            self.opponent_name = data
            print(f"Your opponents name: {self.opponent_name}")

        elif r_type == Protocols.Response.OPPONENT_EXITED:
            self.closed = True
            print(f"Your opponent has exited the game!")

        elif r_type == Protocols.Response.CORRECT_NUMBER:
            self.correct_number = data
            print(f"Correct number was: {data}")

        elif r_type == Protocols.Response.START:
            self.started = True
            print(f"Let the game begin!")








