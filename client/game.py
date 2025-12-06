import pygame
from client.client import Client
from protocols import Protocols

class Game:
    def __init__(self, client):
        self.client = client
        client.start()

        self.font = None
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

        # while the client is still playing, we use the event loop
        while not self.client.closed:
            # setting a specific frame rate for consistency on all server host machines
            clock.tick(30)
            # loop through all events
            for event in pygame.event.get():
                # if the client clicks the stop button, the socket will close. Leading to opponents closing as well
                if event.type == pygame.QUIT:
                    self.client.close_conn()
                    pygame.quit()
                else:
                    self.handle_event(event)

            self.draw(screen)


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
                self.client.send(Protocols.Request.GUESS, int(self.text))
                self.text = ""

        # if the client presses backspace or typing characters, we amend text accordingly
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode

    def draw(self, screen):
        screen.fill((255, 255, 255))
        # if the client has not started the game and is not logged in
        if not self.client.started and not self.logged_in:
            self.draw_login(screen)
        # if the client is logged in but has not started the game
        elif not self.client.started:
            self.draw_waiting(screen)
        # the client must be logged in and started the game so we draw the game screen
        else:
            self.draw_game(screen)

        # tell pycharm to update the screen we have chosen
        pygame.display.update()


    def draw_login(self, screen):
        prompt =  "Please enter the coolest nickname you can think of"
        # render our font
        prompt_surface = self.font.render(prompt, 1, (0, 0, 0))
        # decide where to place the font. (x,y)
        screen.blit(prompt_surface, (50, 50))

        pygame.draw.rect(screen, self.color, self.input_box, 2)
        txt_surface = self.font.render(self.text, 1, self.color)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        # set the input box to be a max of 100 or if the size of the text is larger, grow with the text + 10 as a buffer
        self.input_box.w = max(100, txt_surface.get_width() + 10)



if __name__ == "__main__":
    game = Game(Client())
    game.run()
    pygame.quit()







