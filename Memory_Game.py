import pygame
from pygame.locals import *



class Memory_game:

    #Constructor
    def __init__(self):
        pygame.init()
        self.game_loop()


    def game_loop(self):
        while True:
            # code

            pygame.display.update()
            for event in pygame.event.get():
                self.quit(event)

    def quit(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit(1)


mg = Memory_game()

