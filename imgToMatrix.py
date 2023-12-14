import pygame
import cv2
import numpy as np
import sys

pygame.init()

# Load the image using OpenCV
image_path = 'bnw.png'  # Replace with the path to your image
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded successfully
if image is None:
    print(f"Error: Unable to load the image at {image_path}")
    sys.exit()

# Get the image dimensions
image_height, image_width = image.shape

# Pygame initialization
screen_width, screen_height = image_width, image_height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Array from Black and White Image")

# Initialize a 2D array to represent the image
image_array = np.zeros((image_height, image_width), dtype=int)

# Convert the OpenCV image to Pygame surface
image_surface = pygame.surfarray.make_surface(image)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the image on the screen
    screen.blit(image_surface, (0, 0))

    # Convert Pygame surface to a 2D array with 1's for black and 0's for white
    image_array = np.where(pygame.surfarray.array2d(image_surface) > 0, 1, 0)

    # Optional: Print the 2D array (values will be either 0 or 1)
    print(image_array)

    pygame.display.flip()

pygame.quit()
