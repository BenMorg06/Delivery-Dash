# IMPORTS #
import pygame
from consts import *
from utils import Button, Quit
from login import Login
from highscore import Highscore

# MENU #
class Menu():
    # INIT #
    def __init__(self):
        # sets up objects
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.login = Login()
        self.quit = Quit()
        self.start_button = Button('Start',self.login,300,60, (WIDTH//2 -150,250),6, 32)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,450),6, 32)
        self.highscore_button = Button('Highscore',Highscore(),300,60, (WIDTH//2 -150,350),6, 32)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
        pygame.mixer.init()
        pygame.mixer.music.load(MENU_MUSIC)  # Replace with your audio file path
        # Set the volume (0.0 to 1.0)
        pygame.mixer.music.set_volume(volume)
        # Play the music on loop
        pygame.mixer.music.play(-1)

    # RUN #
    def run(self):
        # main menu loop
        while self.running:
            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            # graphics
            self.screen.fill('#1B4332') 
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.highscore_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            pygame.display.flip()
            CLOCK.tick(FPS)

class Return:
    def __init__():
        pass
    def run():
        Menu().run
# start up menu for the game
menu = Menu()
menu.run()