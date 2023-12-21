import pygame, os
pygame.init()
# Define constants in separate file for easy access and consistency

# Screen constants
HEIGHT, WIDTH = 700, 1244

# Image constants
TRACK = pygame.image.load(os.path.join("Assets","city map 1.png"))
TRACK_BORDER = pygame.image.load(os.path.join("Assets", "map_grass.png")) # draw with rectangles potentially
RED_CAR = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets","car_red_small_4.png")), 180, 0.5) # scales images to the correct size
YELLOW_CAR = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets","car_yellow_small_4.png")), 180, 0.5)
PARCEL = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets","parcel.png")), 0, 0.1)

# Text constants
FONT = pygame.font.Font('freesansbold.ttf', 32) # sets font for text

# Game constants
# Define matrix
# 1 means that the car can use that tile to travel
# 0 means that the car cannot use that square
TRACK_GRID = [[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],#
              [1,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1],#
              [1,1,1,0,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1],#
              [1,0,1,1,1,1,0,0,0,0,1,0,0,1,1,1,0,0,0,1,0,0,1,0,1],#
              [1,0,1,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1],#
              [1,0,1,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1],#
              [1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,1,0,1],#
              [1,0,0,0,0,1,0,1,0,0,1,1,1,1,0,1,1,1,1,0,1,1,1,0,1],#
              [1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,0,0,1,1,1,0,1,0,1],#
              [1,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1],#
              [1,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,1,1,1,0,0,0,1,0,1],#
              [1,1,1,1,1,0,0,1,0,1,0,0,0,1,0,0,1,0,1,0,0,0,1,1,1],#
              [0,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,1],#
              [0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],#
              ] 
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER) # mask for collisions
# After re-evluating the solution i decided that a mask would be the best solution for car and track collisions.