# Imports
import pygame, os, math, sys

# Setup Pygame Window
WIDTH, HEIGHT = 1244, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
Track = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets", "Picture 1.png")), 0, 2.4)
# Add an ICON Later on

# Car 
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()# initiate Sprite
        # Load correct sized image
        self.original_image = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets", "car.png")), 90, 0.1)
        self.image = self.original_image
        # Create rectangle
        self.rect = self.image.get_rect(center=(700,600)) 
        # car default velocity
        self.vel_vector = pygame.math.Vector2(0,-0.5)
        # car drive state
        self.drive_state = False

    def drive(self):
        if self.drive_state:
            self.rect.center += self.vel_vector *6
            
    def update(self): 
        self.drive()

car= (pygame.sprite.GroupSingle(PlayerCar()))

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    #user input
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <=1:
            car.sprite.drive_state = False
            car.sprite.direction = 0
                

        #drive
        if user_input[pygame.K_UP]:
            car.sprite.drive_state = True
        if user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1
        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1

    # Drawing the objects
    SCREEN.fill((0,200,0))
    SCREEN.blit(Track, (-20,-20))
    car.draw(SCREEN)
    # Updating the Car
    car.update()

    pygame.display.update()