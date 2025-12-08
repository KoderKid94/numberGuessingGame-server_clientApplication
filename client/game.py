import pygame
from client.client import Client
from protocols import Protocols

class Game:
    def __init__(self, client):
        self.client = client
        client.start()

        self.font = None
        self.message_font = None
        self.input_box = pygame.Rect(50, 100, 400, 32)
        self.color_active = pygame.Color("springgreen1")
        self.color_inactive = pygame.Color("slateblue1")
        self.color = self.color_inactive

        self.text = ""
        self.done = False
        self.logged_in = False

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 24)
        self.message_font = pygame.font.SysFont("monospace", 18)

        # while the client is still playing, we use the event loop
        while not self.client.closed:
            # setting a specific frame rate for consistency on all server host machines
            clock.tick(30)
            # loop through all events
            for event in pygame.event.get():
                # if the client closes the window, the socket will close. Leading to opponents closing as well
                if event.type == pygame.QUIT:
                    self.client.close_conn()
                    pygame.quit()
                else:
                    self.handle_event(event)

            self.draw(screen)
        pygame.quit()


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.color = self.color_active
            else:
                self.color = self.color_inactive
         # if client is not pressing a key or color is inactive, do nothing
        if event.type!= pygame.KEYDOWN or self.color == self.color_inactive:
            return
        # we send the nickname to the server, set clients nickname, login=True and reset text to empty string
        if event.key == pygame.K_RETURN:
            if not self.logged_in:
                self.client.send(Protocols.Request.NICKNAME, self.text)
                self.client.nickname = self.text
                self.logged_in = True
                self.text = ""
            elif self.client.started:
                # we verify if input is an integer
                try:
                    guess = int(self.text)
                    self.client.send(Protocols.Request.GUESS, guess)
                    self.text = ""
                except ValueError:
                    self.client.add_message("Invalid input,  please enter an integer!")
                    self.text = ""

        # if the client presses backspace or typing characters, we amend text accordingly
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode

    # handle the end of the game by displaying why the game has ended
    def handle_end(self, screen):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if self.client.winner:
                text = f"{self.client.winner} has guessed the correct number!"
            else:
                text = "The opponent has left the game!"

            # display the text in the middle of the screen
            text_surface = self.font.render(text, 1, (0, 0, 0))
            screen.blit(text_surface, (10, 10))
            middle_x = (screen.get_width() / 2) - (text_surface.get_width() / 2)
            middle_y = (screen.get_height() / 2) - (text_surface.get_height() / 2)
            screen.blit(text_surface, (middle_x, middle_y))
            pygame.display.update()


    def draw(self, screen):
        screen.fill((255, 255, 255))

        # Check for game over state FIRST
        if self.client.winner or self.client.game_over:
            self.draw_game_over(screen)
        # if the client has not started the game and is not logged in
        elif not self.client.started and not self.logged_in:
            self.draw_login(screen)
        # if the client is logged in but has not started the game
        elif not self.client.started:
            self.draw_waiting(screen)
        # the client must be logged in and started the game so we draw the game screen
        else:
            self.draw_game(screen)

        # tell pycharm to update the screen we have chosen
        pygame.display.update()


    def draw_game_over(self, screen):
        """Draw the game over screen"""
        if self.client.winner:
            text = f"{self.client.winner} has won the game!"
        else:
            text = "Your opponent has left the game!"

        # Display centered text
        text_surface = self.font.render(text, 1, (0, 0, 0))
        middle_x = (screen.get_width() / 2) - (text_surface.get_width() / 2)
        middle_y = (screen.get_height() / 2) - (text_surface.get_height() / 2)
        screen.blit(text_surface, (middle_x, middle_y))

    def draw_waiting(self, screen):
        # draw text letting client know we are waiting for an opponent to join
        text = "Waiting for an opponent"
        # render our text
        text_surface = self.font.render(text, 1, (0, 0, 0))
        # decide where to place the text. (x,y), in this case we will place text in middle of the screen
        middle_x = (screen.get_width()/2)-(text_surface.get_width()/2)
        middle_y = (screen.get_height()/2)-(text_surface.get_height()/2)
        screen.blit(text_surface, (middle_x, middle_y))


    def draw_login(self, screen):
        prompt =  "Please enter the coolest nickname you can think of"
        # render our font
        prompt_surface = self.font.render(prompt, 1, (0, 0, 0))
        # decide where to place the font. (x,y)
        screen.blit(prompt_surface, (50, 50))
        self.draw_input(screen)

    # needed to draw input box for both draw_login and draw_game
    def draw_input(self, screen):
        pygame.draw.rect(screen, self.color, self.input_box, 2)
        txt_surface = self.font.render(self.text, 1, self.color)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        # set the input box to be a max of 100 or if the size of the text is larger, grow with the text + 10 as a buffer
        self.input_box.w = max(100, txt_surface.get_width() + 10)


    def draw_game(self, screen):
        # bounds for nuumber to be found
        low_bounded = self.client.lower_bound
        high_bounded = self.client.upper_bound
        text = f"Can you guess the number between {low_bounded} and {high_bounded}?"
        question_surface = self.font.render(text, 1, (0, 0, 0))
        screen.blit(question_surface, (50, 50))
        self.draw_input(screen)

        # Display opponent info
        if self.client.opponent_name:
            opponent_text = f"Opponent: {self.client.opponent_name}"
            opponent_surface = self.message_font.render(opponent_text, 1, (100, 100, 100))
            x_pos = screen.get_width() - opponent_surface.get_width() - 20
            screen.blit(opponent_surface, (50, 150))

        # Draw input box
        self.draw_input(screen)

        # Draw message feed
        self.draw_messages(screen)


    def draw_messages(self, screen):
        # y-offset to display messages under input_box
        y_offset = 200
        #opp_name_surface = self.client.opponent_name.render(self.client.opponent.name, 1, (0, 0, 0))
        #screen.blit(opp_name_surface, (50, 100))
        for i, message in enumerate(self.client.messages):
            msg_surface = self.message_font.render(message, 1, (50, 50, 50))
            screen.blit(msg_surface, (50, y_offset + (i * 25)))


if __name__ == "__main__":
    game = Game(Client())
    game.run()
    pygame.quit()







