import pygame
from consts import *
from utils import Button, Quit
from main import Main
game = Main()

class LoginMenu():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.login_button = Button('Login','Login Class',300,60, (WIDTH//2 -150,250),6)
        self.quit_button = Button('quit',Quit,300,60, (WIDTH//2 -150,450),6)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
    
    def run(self):
        while self.running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.screen.fill((0,200,0)) 
            self.login_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            
            pygame.display.flip()
            CLOCK.tick(FPS)

class Login():
    def __init__(self):
        pass