# IMPORTS #
import pygame
from consts import *
from utils import *
from main import *

# HIGHSCORE #
class Highscore():
    # INIT #
    def __init__(self):
        # Sets screen and graphics objects
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.quit = Quit()
        self.tab = Tabs(600,450,(WIDTH//2 -300 , HEIGHT//2 -200))
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
        self.highscore = TITLE_FONT.render('Highscore', False, '#2D6A4F')
        self.highscore_rect = self.highscore.get_rect(center =(WIDTH//2, 200))
        self.quit_button = Button('Quit',Quit,150,60, (WIDTH//2 +100 ,525),6, 32)

    # Get Highscore #
    def get_highscore(self):
        pass

    # RUN #
    def run(self):
        # loop
        while self.running:
            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            # graphics
            self.screen.fill('#1B4332') 
            self.tab.draw(self.screen)
            self.quit_button.draw(self.screen)
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            self.screen.blit(self.highscore, self.highscore_rect)
            
            pygame.display.flip()
            CLOCK.tick(FPS)

test = Highscore()
test.run()