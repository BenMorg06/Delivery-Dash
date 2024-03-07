# IMPORTS #
import pygame
from consts import *
from utils import *

# OPTIONS #
class Options():
    # INIT #
    def __init__(self, game):
        # Set up objects #
        self.running = True
        self.quit = Quit()
        self.resume_button = Button('Resume',game,300,60, (WIDTH//2 -150,250),6, 32)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,450),6, 32)
        self.highscore_button = Button('Highscore','HighScore class',300,60, (WIDTH//2 -150,350),6, 32)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
    
    # RUN #
    def run(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        while self.running:
            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            # graphics
            self.screen.fill((34, 40, 49)) 
            self.resume_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.highscore_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            pygame.display.flip()
            CLOCK.tick(FPS)