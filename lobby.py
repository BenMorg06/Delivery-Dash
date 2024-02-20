import pygame
from consts import *
from utils import *
from main import *
game = running()
class Lobby():
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.quit = Quit()
        self.start_button = Button('Play',game,150,60, (WIDTH//2 -200,425),6, 32)
        self.quit_button = Button('Quit',Quit,150,60, (WIDTH//2 +50 ,425),6, 32)
        self.tab = Tabs(600,300,(WIDTH//2 -300 , HEIGHT//2 -150))
        self.next_arrow = Arrows(((WIDTH//2 + 320,HEIGHT//2 - 25),(WIDTH//2 + 320,HEIGHT//2 + 25),(WIDTH//2 + 350,HEIGHT//2)),(WIDTH//2 +320, HEIGHT//2 -25), TabIncrease)
        self.prev_arrow = Arrows(((WIDTH//2 - 320,HEIGHT//2 - 25),(WIDTH//2 -320,HEIGHT//2 + 25),(WIDTH//2 - 350,HEIGHT//2)),(WIDTH//2 -350, HEIGHT//2 -25), TabDecrease)
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
        self.tab_index = 0

    def run(self):
        while self.running:
            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.screen.fill('#1B4332') 
            self.tab.draw(self.screen)
            if self.tab_index == 0:
                self.start_button.draw(self.screen)
                self.quit_button.draw(self.screen)
            if self.tab_index == 1:
                self.start_button.draw(self.screen)
            else:pass
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