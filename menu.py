import pygame, os, math, random
from consts import *
from main import Main
game = Main()

class Menu():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.start_button = Button('Start',BLUE_BUTTON,'starting',WIDTH//2,HEIGHT//2-96)
        self.quit_button = Button('Quit',BLUE_BUTTON,'quitting',WIDTH//2,HEIGHT//2+96)
        self.high_score_button = Button('High Score', BLUE_BUTTON,'high score',WIDTH//2,HEIGHT//2)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))

    def run(self):
        # main menu loop
        while self.running:
            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                # Clicking the buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.start_button.rect.collidepoint(x,y):
                        self.start_button.on_click()
                    if self.quit_button.rect.collidepoint(x,y):
                        self.quit_button.on_click()
                    if self.high_score_button.rect.collidepoint(x,y):
                        self.high_score_button.on_click()
            # draw the buttons
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            self.high_score_button.draw(self.screen)
            # draw the title
            self.screen.blit(self.title, self.title_rect)
            
            pygame.display.update()
# button class
class Button():
    def __init__(self, text, img, action,x,y):
        self.img = img
        self.text = FONT.render(text, False, "#ffffff") # text for button
        self.action = action
        self.x, self.y = x, y
        self.text_rect = self.text.get_rect(center = (self.x, self.y)) # rectangles to center the text and buttons
        self.rect = self.img.get_rect(center = (self.x,self.y))
    
    # run task when clicked
    def on_click(self):
        if self.action == 'starting':
            game.run()
        else:
            print(self.action)
    
    # draw the buttons
    def draw(self, screen):
        screen.blit(self.img, self.rect)
        screen.blit(self.text, self.text_rect)
    

menu = Menu()
menu.run()

