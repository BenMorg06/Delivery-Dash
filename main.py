# Imports
import pygame, os, math, sys

# Setup Pygame Window
WIDTH, HEIGHT = 1244, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
Track = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets", "Picture 1.png")), 0, 2.4)

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    SCREEN.fill((0,200,0))
    SCREEN.blit(Track, (-20,-20))

    pygame.display.update()