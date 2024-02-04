import pygame
from consts import *
from utils import Button, Quit, TextBox
from main import Main
game = Main()

class LoginMenu():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.login = Login()
        self.login_button = Button('Login',self.login,300,60, (WIDTH//2 -150,250),6)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,450),6)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
    
    def run(self):
        while self.running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.screen.fill((34, 40, 49)) 
            self.login_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            
            pygame.display.flip()
            CLOCK.tick(FPS)

class Login():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.login_button = Button('Login',game,300,60, (WIDTH//2 -150,450),6)
        self.username_box = TextBox('Username',300,60, (WIDTH//2 -150, 250), 6)
        self.password_box = TextBox('Password',300,60, (WIDTH//2 -150, 350), 6)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,550),6)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
    
    def run(self):
        while self.running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN and self.username_box.pressed: 
  
                    #Check for backspace 
                    if event.key == pygame.K_BACKSPACE: 
    
                        # get text input from 0 to -1 i.e. end. 
                        self.username_box.text = self.username_box.text[:-1] 
  
                    # Unicode standard is used for string 
                    # formation 
                    elif event.key == pygame.K_RETURN:
                        self.username_box.original_text = self.username_box.text


                    else: 
                        self.username_box.text += event.unicode
                        self.username_box.value += event.unicode

                    

                if event.type == pygame.KEYDOWN and self.password_box.pressed: 
  
                    #Check for backspace 
                    if event.key == pygame.K_BACKSPACE: 
    
                        # get text input from 0 to -1 i.e. end. 
                        self.password_box.text = self.password_box.text[:-1] 
                        
                    elif event.key == pygame.K_RETURN:
                        self.password_box.original_text = self.password_box.text
                    # Unicode standard is used for string 
                    # formation 
                    else: 
                        self.password_box.value += event.unicode
                        self.password_box.text += '*'
                    

            self.screen.fill((34, 40, 49)) 
            self.username_box.draw(self.screen)
            self.password_box.draw(self.screen)
            self.login_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            
            pygame.display.flip()
            CLOCK.tick(FPS)