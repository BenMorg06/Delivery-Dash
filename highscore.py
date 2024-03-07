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
        f = open('highscores.csv','r')
        scores = f.readlines()
        user_scores = {}
        while len(user_scores) != len(scores):
            highscore = 0
            user = ''
            for i in scores:
                if highscore < int(i.split(',')[1]) and i.split(',')[0] not in user_scores:
                    highscore = int(i.split(',')[1])
                    user = i.split(',')[0]
                else: pass
            user_scores[user] = int(highscore)
        self.first_user = FONT.render(f"{list(user_scores.keys())[0]} : {list(user_scores.values())[0]}", False, '#2D6A4F') #
        self.second_user = FONT.render(f"{list(user_scores.keys())[1]} : {list(user_scores.values())[1]}", False, '#2D6A4F') #
        self.third_user = FONT.render(f"{list(user_scores.keys())[2]} : {list(user_scores.values())[2]}", False, '#2D6A4F') #
        self.first_rect = self.first_user.get_rect(midleft = (WIDTH//2 -200, 300))
        self.second_rect = self.second_user.get_rect(midleft = (WIDTH//2 -200, 350))
        self.third_rect = self.third_user.get_rect(midleft = (WIDTH//2 -200, 400))

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
            self.screen.blit(self.first_user, self.first_rect)
            self.screen.blit(self.second_user, self.second_rect)
            self.screen.blit(self.third_user, self.third_rect)
            
            pygame.display.flip()
            CLOCK.tick(FPS)

test = Highscore()
test.get_highscore()
test.run()