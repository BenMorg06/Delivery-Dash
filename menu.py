import pygame, os, math, random
from consts import *
from main import Main
game = Main()
class Menu():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.start_button = Button('Start',300,60, (WIDTH//2 -150,250),6)
        self.quit_button = Button('Quit',300,60, (WIDTH//2 -150,450),6)
        self.highscore_button = Button('Highscore',300,60, (WIDTH//2 -150,350),6)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))

    def run(self):
        # main menu loop
        while self.running:
            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.screen.fill((0,200,0)) 
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.highscore_button.draw(self.screen)
        
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            
            pygame.display.flip()
            CLOCK.tick(FPS)

# button class
class Button():
    def __init__(self, text, width, height,pos, elevation):
        # core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rect
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'

        # bottom rect
        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = '#354B5E'

        # text
        self.action = text
        self.text_surf = FONT.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    # run task when clicked
    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        # this logic ensures the button is only clicked once
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    if self.action == 'Start':
                        game.run()
                    elif self.action == 'Quit':
                        quit()
                    elif self.action == 'Highscore':
                        pass
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'

    # draw the buttons
    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen,self.bottom_color,self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.on_click()
    

menu = Menu()
menu.run()

