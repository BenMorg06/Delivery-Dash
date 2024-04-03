import pygame
from consts import *
from utils import *
from validation import *

class Login():
    # LOGIN #
    def __init__(self):
        # Set up Objects
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.username_box = TextBox('Username',300,60, (WIDTH//2 -150, 250), 6, 32)
        self.password_box = TextBox('Password',300,60, (WIDTH//2 -150, 350), 6, 32)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,550),6, 32)
        self.validate = Validation('users_pass.csv',self.username_box.value, self.password_box.value)
        self.new_user_validation = NewUser('users_pass.csv',self.username_box.value, self.password_box.value)
        self.login_button = Button('Login',self.validate,140,60, (WIDTH//2 -150,450),6, 26)
        self.new_user_button = Button('New User',self.new_user_validation,140,60, (WIDTH//2 +10,450),6, 26)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
    
    # UPDATE BUTTONS #
    def update_buttons(self):
        #print(self.password_box.value)
        # updates the values sent to validation and new user classes
        self.validate = Validation('users_pass.csv',self.username_box.value, self.password_box.value)
        self.new_user_validation = NewUser('users_pass.csv',self.username_box.value, self.password_box.value)
        self.login_button = Button('Login',self.validate,140,60, (WIDTH//2 -150,450),6, 26)
        self.new_user_button = Button('New User',self.new_user_validation,140,60, (WIDTH//2 +10,450),6, 26)
    # RUN #
    def run(self):
        while self.running: 
            for event in pygame.event.get():
                # Check for quits
                if event.type == pygame.QUIT:
                    quit()
                # Take input for username box
                if event.type == pygame.KEYDOWN and self.username_box.pressed: 
                    #Check for backspace 
                    if event.key == pygame.K_BACKSPACE: 
                        # get text input from 0 to -1  
                        self.username_box.text = self.username_box.text[:-1] 
                        self.username_box.value = self.username_box.value[:-1]
                    # Unicode standard is used for string 
                    
                    # Checks for enter being pressed
                    elif event.key == pygame.K_RETURN:
                        # key validation checks
                        if presence_check(self.username_box.text) and type_check(self.username_box.text, 'string') and len_check(self.username_box.text, 16):
                            self.username_box.original_text = self.username_box.text
                            self.update_buttons()
                    # adds the letter pressed to the strings
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
                    else: 
                        self.password_box.value += event.unicode
                        self.password_box.text += '*'
                    # repeated code for password box could be made into a function instead
                        
            login_texts = self.validate.text_update() 
            user_texts = self.new_user_validation.text_update()
            #print(self.password_box.value)
            # graphics
            self.screen.fill('#1B4332') 
            self.username_box.draw(self.screen)
            self.password_box.draw(self.screen)
            self.login_button.draw(self.screen)
            self.new_user_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            # Write Error messages
            if login_texts[4]:
                self.screen.blit(login_texts[0], login_texts[1])

            elif login_texts[5]:
                self.screen.blit(login_texts[2], login_texts[3])
            
            if user_texts[4]:
                self.screen.blit(user_texts[0], user_texts[1])

            elif user_texts[5]:
                self.screen.blit(user_texts[2], user_texts[3])
            
            
            
            pygame.display.flip()
            CLOCK.tick(FPS)
