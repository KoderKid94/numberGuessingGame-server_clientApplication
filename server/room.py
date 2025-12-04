import random
from enum import Enum

class GuessResult(Enum):
    CORRECT = 0
    TOO_LOW = 1
    TOO_HIGH = 2
    GAME_OVER = 3

class Room:
    def __init__(self, client1, client2):
        self.correct_number = self.generate_number()
        self.game_over = False

    # generate random integer between given values, helper method so we make it static
    @staticmethod
    def generate_number():
        return random.randint(1, 500)

    def verify_guess(self, guess):
        # if the game is over, there should be no guess submissions
        if self.game_over:
            return GuessResult.GAME_OVER

        # verify if the clients guess is correct, too low/high.
        if self.correct_number == guess:
            self.game_over = True
            return GuessResult.CORRECT

        if self.correct_number > guess:
            return GuessResult.TOO_LOW

        return GuessResult.TOO_HIGH









