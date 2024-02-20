import pygame
from consts import *
from utils import *
from validation import *
from main import Main

class Login():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.username_box = TextBox('Username',300,60, (WIDTH//2 -150, 250), 6, 32)
        self.password_box = TextBox('Password',300,60, (WIDTH//2 -150, 350), 6, 32)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,550),6, 32)
        self.login_button = Button('Login',Validation('users_pass.csv',self.username_box.value, self.password_box.value),140,60, (WIDTH//2 -150,450),6, 26)
        self.new_user_button = Button('New User',NewUser('users_pass.csv',self.username_box.value, self.password_box.value),140,60, (WIDTH//2 +10,450),6, 26)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
    def update_buttons(self):
        #print(self.password_box.value)
        self.login_button = Button('Login',Validation('users_pass.csv',self.username_box.value, self.password_box.value),140,60, (WIDTH//2 -150,450),6, 26)
        self.new_user_button = Button('New User',NewUser('users_pass.csv',self.username_box.value, self.password_box.value),140,60, (WIDTH//2 +10,450),6, 26)

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
                        self.username_box.value = self.username_box.value[:-1]
  
                    # Unicode standard is used for string 
                    # formation 
                    elif event.key == pygame.K_RETURN:
                        if presence_check(self.username_box.text) and type_check(self.username_box.text, 'string') and len_check(self.username_box.text, 16):
                            self.username_box.original_text = self.username_box.text
                            self.update_buttons()


                    else: 
                        self.username_box.text += event.unicode
                        self.username_box.value += event.unicode

                    

                if event.type == pygame.KEYDOWN and self.password_box.pressed: 
  
                    #Check for backspace 
                    if event.key == pygame.K_BACKSPACE: 
    
                        # get text input from 0 to -1 i.e. end. 
                        self.password_box.text = self.password_box.text[:-1] 
                        self.password_box.value = self.password_box.value[:-1]
                        
                    elif event.key == pygame.K_RETURN:
                        if presence_check(self.password_box.value) and type_check(self.password_box.value, 'string') and len_check(self.password_box.value, 16):
                            self.password_box.original_text = self.password_box.text
                            self.update_buttons()
                    # Unicode standard is used for string 
                    # formation 
                    else: 
                        self.password_box.value += event.unicode
                        self.password_box.text += '*'
                        
                    
            #print(self.password_box.value)
            self.screen.fill('#1B4332') 
            self.username_box.draw(self.screen)
            self.password_box.draw(self.screen)
            self.login_button.draw(self.screen)
            self.new_user_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            
            pygame.display.flip()
            CLOCK.tick(FPS)
