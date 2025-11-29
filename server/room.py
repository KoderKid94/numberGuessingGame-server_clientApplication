import random

class Room:
    def __init__(self, client1, client2):
        self.correct_number = self.generate_number()
        self.game_over = False

    # generate random integer between given values
    def generate_number(self):
        return random.randomint(1, 500)

    def verify_guess(self, client, guess):
        # if the game is over, there should be no guess submissions
        if self.game_over:
            return False

        # verify if the clients guess is correct or not
        correct = (self.correct_number == guess)

        if correct:
            self.game_over = True

        return correct

