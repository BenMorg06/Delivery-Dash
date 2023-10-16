# Imports
import pygame, os, math, sys

# Setup Pygame Window
# Define constants
WIDTH, HEIGHT = 1244, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Define image
TRACK = pygame.image.load(os.path.join("Assets","city map 1.png"))

# Define matrix


# Track collisions
# I will no longer be using a mask for the track collisions because it will be more efficient for time and ease of code.
# These collisions will be added once the car is created

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    SCREEN.fill((0,200,0))
    SCREEN.blit(TRACK,(0,0))

    pygame.display.update()