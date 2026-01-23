# Number Guessing Game – Client–Server Application

This project is a two-player networked Number Guessing Game implemented in Python.  
A central TCP server pairs two clients into a game room.  
Once paired, both players begin submitting guesses until the server declares a winner.

This guide provides clear, step-by-step instructions for installing, running, and using the application.

---

## 1. Requirements

- **Python 3.10+**  
  (Project was developed and tested using Python 3.14.0)
- **Pygame: Version 2.0 or higher**


No external packages are required — everything uses the Python standard library.





The game is played by running one server and separate client instances.

---

## 2. How to Run the Server

1. Open a terminal.
2. Navigate to the project directory:


   cd numberGuessingGame 

   Start the server:

    python3 server/main.py

You should see:

Listening on 127.0.0.1:55556

The server is now waiting for players to connect.
## 3. How to Run the Client

Each player must run a client in a separate terminal window.

The client game logic is implemented in:

client/game.py

and is launched as a module.
Steps:

    Open a new terminal window.

    Navigate to the project directory:

cd numberGuessingGame

Run the client:

    python3 -m client.game

    When prompted, click into the text and notice the color
    changes to an "active" color, enter a nickname and press the return key.

Repeat the same process in a second terminal for Player 2.
The game will begin automatically when both clients are connected.
## 4. How the Game Works (User Instructions)

    Each client connects to the server and sends a nickname.

    When two players are available, the server:

        Creates a game room

        Sends each player the guessing bounds and their opponent name

        Sends the generated correct number to the clients terminal

        Sends a START message

    Both players begin submitting guesses.

    For each guess, the server responds with:

        Too Low

        Too High

        Correct

    When a player guesses correctly:

        The server declares the winner to both players

        Reveals the correct number

        Ends the game

Players may restart the clients to play another round.
## 5. Stopping the Application
Stop the Server:

CTRL + C

Stop a Client:

CTRL + C or close the window

The server safely handles disconnects and cleans up the game state.
## 6. Troubleshooting
Client cannot connect

Ensure the server is running and displays:

Listening on 127.0.0.1:55556

Port already in use

The server already allows port reuse (SO_REUSEADDR),
so simply relaunch the server:

python3 server/main.py

Game does not start

Both clients must be running.
The server pairs players only when two clients connect.
## 7. Summary

Start the server:

    python3 server/main.py

Start each client (run twice):

    python3 -m client.game

Enter nicknames

Submit guesses

Game ends when the server declares a winner

This completes all steps required to compile, run, and use the application.# Testing commit attribution
