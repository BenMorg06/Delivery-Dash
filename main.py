# Imports
import pygame, os, math, sys

# Setup Pygame Window
# Define constants
WIDTH, HEIGHT = 1244, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Define images
TRACK = pygame.image.load(os.path.join("Assets","city map 1.png"))
TRACK_BORDER = pygame.image.load(os.path.join("Assets", "map_grass.png"))
RED_CAR = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets","car_red_small_4.png")), 180, 0.5)
SMALLER_CAR = pygame.transform.rotozoom(pygame.image.load(os.path.join("Assets","car_red_small_4.png")), 180, 0.4)
# Define matrix
# 1 means that the car can use that tile to travel
# 0 means that the car cannot use that square
Track_Grid = [[1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],#
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

# Track collisions
# I will no longer be using a mask for the track collisions because it will be more efficient for time and ease of code.
# These collisions will be added once the car is created
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER) # after re-evluating the solution i decided that a mask would be the best solution for car and track collisions.


# img utils
def blit_rotate_centre(win, img, top_left, angle):
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft=top_left).center)
    # here we rotate the original image
    # we create a new rectangle to remove the offset from the original rotation
    # making it appear like we rotated around the center of the original image
    win.blit(rotated_img, new_rect.topleft)

# Generic Car Class
class AbsractCar():
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0 #car starts stationary
        self.rotation_vel = rotation_vel
        self.angle = 0 # car starts unrotated
        self.x, self.y = self.START_POS
        self.acceleration = 0.1 # every frame the velocity increases by 0.1 pixels
        self.rect = self.img.get_rect()


    def rotate(self, left=False, right=False):
        if left:
            self.angle+=self.rotation_vel
        elif right:
            self.angle-=self.rotation_vel

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) # self.vel becoems equal to vel + acceleration if that is lower than the max velocity
        # if that is greater than the max then self.vel is set to equal the max velocity
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians)*self.vel
        horizontal = math.sin(radians)*self.vel
        self.y += vertical
        self.x += horizontal

    def reduce_speed(self):
        self.vel = max(self.vel-self.acceleration/2, 0)
        self.move()

    def draw(self, win):
        blit_rotate_centre(win,self.img, (self.x,self.y), self.angle)

    def collide(self, mask, x=0, y=-0):
        car_mask = pygame.mask.from_surface(SMALLER_CAR)
        offset = (self.x -x, self.y-y) 
        poi = mask.overlap(car_mask, offset)
        return poi

    def bounce(self):
        self.vel = -self.vel/2
        self.move()

class PlayerCar(AbsractCar):
    IMG = RED_CAR
    START_POS = 20,20

#print(Track_Grid)
# Main loop
run = True
player_car = PlayerCar(1,3)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    if not moved:
        player_car.reduce_speed()

    # collisions
    if player_car.collide(TRACK_BORDER_MASK) != None: #When the car is not touching the road this if occurs
        player_car.bounce()

    if player_car.x <= 0 or player_car.y <= 0 or player_car.x >= WIDTH or player_car.y >= HEIGHT:
        player_car.bounce()
    

    SCREEN.fill((0,200,0))
    SCREEN.blit(TRACK,(0,0))
    player_car.draw(SCREEN)

    pygame.display.update()