import pygame
from consts import *

##################################
######### IMAGE UTILITY ##########
##################################
def blit_rotate_centre(win, img, top_left, angle):
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft=top_left).center)
    # here we rotate the original image
    # we create a new rectangle to remove the offset from the original rotation
    # making it appear like we rotated around the center of the original image
    win.blit(rotated_img, new_rect.topleft)


# button class
class Button():
    def __init__(self, text, action, width, height,pos, elevation, font_size):
        # core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rect
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#52B788'

        # bottom rect
        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = '#2D6A4F'

        # text
        self.text = text
        font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text_surf = font.render(text,True,'#FFFFFF')
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
                    self.pressed = False
                    self.action.run()
                    
                    
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#52B788'

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
    def __init__(self, text, width, height, pos, elevation, font_size):
        # core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rect
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#52B788'

        # bottom rect
        self.bottom_rect = pygame.Rect(pos,(width,elevation))
        self.bottom_color = '#2D6A4F'

        # text
        self.original_text = text
        self.text = text
        font = pygame.font.Font('freesansbold.ttf', font_size)
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
                self.value = ''
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.top_color = '#D74B4B'
                    
                    
        else:
            self.dynamic_elevation = self.elevation
            self.text = self.original_text
            self.pressed = False
            if not self.pressed:
                self.top_color = '#52B788'

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
    
class Tabs():
    def __init__(self, width, height,pos):
        # top rect
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#D8F3DC'

        # bottom rect
        self.border_rect = pygame.Rect((pos[0]-7.5,pos[1]-7.5),(width+15,height+15))
        self.border_color = '#B7E4C7'
    
    # draw
    def draw(self, screen):
        pygame.draw.rect(screen,self.border_color,self.border_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)

class Arrows():
    def __init__(self,points,pos,action):

        # top rect
        self.points = points
        self.polygon_rect = pygame.Rect(pos,(abs(points[0][0]-points[2][0]), abs(points[0][1]-points[1][1])))
        self.top_color = '#52B788'

        # action
        self.action = action
        self.pressed = False    
    
    # run task when clicked
    def on_click(self):
        mouse_pos = pygame.mouse.get_pos()
        # this logic ensures the button is only clicked once
        if self.polygon_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
                    self.tab_index = self.action.run(self.tab_index)
        else:
            self.top_color = '#52B788'
    
    def update_tab(self):
        return self.tab_index
    # draw the buttons
    def draw(self, screen, tab_index):
        pygame.draw.polygon(screen,self.top_color, self.points)
        self.tab_index = tab_index
        self.on_click()
        #pygame.draw.rect(screen, self.top_color, self.polygon_rect)

class TabIncrease():
    def __init__():
        pass
    def run(tab_index):
        return tab_index+1
class TabDecrease():
    def __init__():
        pass
    def run(tab_index):
        return tab_index-1
    
def get_highscore():
        f = open('highscores.csv','r')
        scores = f.readlines()
        user_scores = {}
        # sorts highscores into a dictionary
        while len(user_scores) != len(scores):
            highscore = 0
            user = ''
            for i in scores:
                # makes sure the next entry in the dictionary is the highest score from a user not already there
                if highscore < int(i.split(',')[1]) and i.split(',')[0] not in user_scores:
                    highscore = int(i.split(',')[1])
                    user = i.split(',')[0]
                else: pass
            user_scores[user] = int(highscore)
        return user_scores