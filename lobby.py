# IMPORTS #
import pygame
from consts import *
from utils import *
from main import *

# LOBBY #
class Lobby():
    # INIT #
    def __init__(self):
        # set screen and objects (images, rects, etc.)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.quit = Quit()
        self.quit_button = Button('Quit',Quit,150,60, (WIDTH//2 +100 ,425),6, 32)
        self.tab = Tabs(600,300,(WIDTH//2 -300 , HEIGHT//2 -150))
        self.next_arrow = Arrows(((WIDTH//2 + 320,HEIGHT//2 - 25),(WIDTH//2 + 320,HEIGHT//2 + 25),(WIDTH//2 + 350,HEIGHT//2)),(WIDTH//2 +320, HEIGHT//2 -25), TabIncrease)
        self.prev_arrow = Arrows(((WIDTH//2 - 320,HEIGHT//2 - 25),(WIDTH//2 -320,HEIGHT//2 + 25),(WIDTH//2 - 350,HEIGHT//2)),(WIDTH//2 -350, HEIGHT//2 -25), TabDecrease)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
        self.tab_index = 0
        self.red_car_image = pygame.transform.rotozoom(RED_CAR,0,2)
        self.red_car_rect = self.red_car_image.get_rect(center = (WIDTH//2-150, 300))
        self.blue_car_image = pygame.transform.rotozoom(BLUE_CAR,0,2)
        self.blue_car_rect = self.blue_car_image.get_rect(center = (WIDTH//2+150, 300))
        self.green_car_image = pygame.transform.rotozoom(GREEN_CAR,0,2)
        self.green_car_rect = self.green_car_image.get_rect(center = (WIDTH//2-150, 400))
        self.player_car = [self.red_car_image, self.red_car_rect]
        self.track_bg = pygame.Rect(WIDTH//2,250, WIDTH//5, HEIGHT//5)
        self.start_button = Button('Play',running(self.player_car[0]),150,60, (WIDTH//2 -250,425),6, 32)

    # update the values sent to run the game (car image)
    def update_buttons(self):
        self.start_button = Button('Play',running(self.player_car[0]),150,60, (WIDTH//2 -250,425),6, 32)

    # get values for highscores and create text
    def highscore_text(self,):
        self.highscore = TITLE_FONT.render('Highscore', False, '#2D6A4F')
        self.highscore_rect = self.highscore.get_rect(center =(WIDTH//2, 250))
        user_scores = get_highscore()
        # text for highscores
        self.first_user = FONT.render(f"{list(user_scores.keys())[0]} : {list(user_scores.values())[0]}", False, '#2D6A4F') #
        self.second_user = FONT.render(f"{list(user_scores.keys())[1]} : {list(user_scores.values())[1]}", False, '#2D6A4F') #
        self.third_user = FONT.render(f"{list(user_scores.keys())[2]} : {list(user_scores.values())[2]}", False, '#2D6A4F') #
        self.first_rect = self.first_user.get_rect(midleft = (WIDTH//2 -200, 300))
        self.second_rect = self.second_user.get_rect(midleft = (WIDTH//2 -200, 350))
        self.third_rect = self.third_user.get_rect(midleft = (WIDTH//2 -200, 400))
    
    def tutorial_text(self):
        self.tutorial = TITLE_FONT.render('Tutorial', False, '#2D6A4F')
        self.tutorial_rect = self.tutorial.get_rect(center =(WIDTH//2, 250))
        self.w_control = FONT.render(f"W : FORWARDS", False, '#2D6A4F') #
        self.a_control = FONT.render(f"A : LEFT", False, '#2D6A4F') #
        self.s_control = FONT.render(f"S : BACKWARDS", False, '#2D6A4F') #
        self.d_control = FONT.render(f"D : RIGHT", False, '#2D6A4F') #
        self.w_rect = self.w_control.get_rect(midleft = (WIDTH//2 -250, 300))
        self.a_rect = self.a_control.get_rect(midleft = (WIDTH//2 -250, 350))
        self.s_rect = self.s_control.get_rect(midleft = (WIDTH//2 -250, 400))
        self.d_rect = self.d_control.get_rect(midleft = (WIDTH//2 -250, 450))
        #self.desc = FONT_26.render("Drive into all the parcels",False, '#2D6A4F')
        #self.desc_rect = self.desc.get_rect(midleft = (WIDTH//2 -50, 350))


    # RUN #
    def run(self):
        self.highscore_text()
        self.tutorial_text()
        while self.running:
            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.screen.fill('#1B4332') 
            self.tab.draw(self.screen)
            # Play Tab
            if self.tab_index == 0:
                self.start_button.draw(self.screen)
                self.quit_button.draw(self.screen)
                self.screen.blit(self.player_car[0], self.red_car_rect)
                pygame.draw.rect(self.screen, (0,200,0),self.track_bg,)
                self.screen.blit(pygame.transform.rotozoom(TRACK,0,0.2),(WIDTH//2,250))
            # Customise Tab
            elif self.tab_index == 1:
                self.screen.blit(self.red_car_image, self.red_car_rect)
                self.screen.blit(self.green_car_image, self.green_car_rect)
                self.screen.blit(self.blue_car_image, self.blue_car_rect)
                self.quit_button.draw(self.screen)
                pygame.draw.rect(self.screen,(0,255,0),self.player_car[1],2)
                if self.red_car_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255,0,0),self.red_car_rect,2)
                    if pygame.mouse.get_pressed()[0]:
                        self.player_car = [self.red_car_image, self.red_car_rect]
                if self.blue_car_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255,0,0),self.blue_car_rect,2)
                    if pygame.mouse.get_pressed()[0]:
                        self.player_car = [self.blue_car_image, self.blue_car_rect]
                if self.green_car_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255,0,0),self.green_car_rect,2)
                    if pygame.mouse.get_pressed()[0]:
                        self.player_car = [self.green_car_image, self.green_car_rect]
                self.update_buttons()
            # Highscore Tab
            elif self.tab_index == 2:
                self.screen.blit(self.highscore, self.highscore_rect)
                self.screen.blit(self.first_user, self.first_rect)
                self.screen.blit(self.second_user, self.second_rect)
                self.screen.blit(self.third_user, self.third_rect)
                self.quit_button.draw(self.screen)
            # Tutorial Tab
            elif self.tab_index == 3:
                self.screen.blit(self.tutorial, self.tutorial_rect)
                self.screen.blit(self.w_control, self.w_rect)
                self.screen.blit(self.a_control, self.a_rect)
                self.screen.blit(self.s_control, self.s_rect)
                self.screen.blit(self.d_control, self.d_rect)
                self.screen.blit(self.desc, self.desc_rect)
                self.quit_button.draw(self.screen)
            # Shop Tab (PHASE TWO)
                
            # Loop tabs
            elif self.tab_index <0:
                self.tab_index = 3
                self.screen.blit(self.highscore, self.highscore_rect)
                self.quit_button.draw(self.screen)
            else:
                self.tab_index = 0
                self.start_button.draw(self.screen)
                self.quit_button.draw(self.screen)

            #print(self.tab_index)
            self.next_arrow.draw(self.screen, self.tab_index)
            self.tab_index = self.next_arrow.update_tab()
            self.prev_arrow.draw(self.screen, self.tab_index)
            self.tab_index = self.prev_arrow.update_tab()
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)

            
            
            pygame.display.flip()
            CLOCK.tick(FPS)
test = Lobby()
test.run()