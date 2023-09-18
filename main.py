# Imports
import pygame, os, math, sys

# Setup Pygame Window
WIDTH, HEIGHT = 1244, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    SCREEN.fill((0,200,0))

    pygame.display.update()