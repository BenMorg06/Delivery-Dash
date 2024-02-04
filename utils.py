import pygame
from consts import *


# button class
class Button():
    def __init__(self, text, action, width, height,pos, elevation):
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
        self.text = text
        self.text_surf = FONT.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # action
        self.action = action
    
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
                    self.action.run()
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
    
# Quit Class
class Quit():
    def __init__(self):
        pass
    def run():
        quit()

# Text Box Class
class TextBox():
    def __init__(self, text, width, height, pos, elevation):
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
        self.original_text = text
        self.text = text
        self.text_surf = FONT.render(self.text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

        # validation
        self.value = ''


    # run task when clicked
    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        # this logic ensures the button is only clicked once
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
                self.text = ''
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.top_color = '#D74B4B'
                    
                    
        else:
            self.dynamic_elevation = self.elevation
            self.text = self.original_text
            self.pressed = False
            if not self.pressed:
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
        self.text_surf = FONT.render(self.text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        screen.blit(self.text_surf, self.text_rect)
        self.on_click()

def validate(csv, user, password):
    # loop through csv and check if user is present in file
    # if user present then check if password is correct for user
    # if not create new user with such password
    # passwords should be hashed and comparison with hashed passwords
