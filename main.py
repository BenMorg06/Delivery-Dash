# Imports
import pygame, os, math, sys

# Setup Pygame Window
WIDTH, HEIGHT = 1244, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
Track = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets", "Picture 1.png")), 0, 2.4)

# Car 
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets", "car.png")), 90, 0.1)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(700,600)) 
    
car= (pygame.sprite.GroupSingle(PlayerCar()))

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    SCREEN.fill((0,200,0))
    SCREEN.blit(Track, (-20,-20))
    car.draw(SCREEN)

    pygame.display.update()