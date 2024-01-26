# Imports
import pygame, os, math, random, copy
from consts import *
from collections import deque
pygame.init() #initiates pygame library

# Setup Pygame Window
pygame.display.set_caption("Delivery Dash") # sets name of window
# Define Screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # sets dimensions of window


# calculate optimal time
# bronze, silver, gold medals if close enough to time
# Each element of the matrix represents a 48x48 tile on the screen

# img utils
def blit_rotate_centre(win, img, top_left, angle):
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft=top_left).center)
    # here we rotate the original image
    # we create a new rectangle to remove the offset from the original rotation
    # making it appear like we rotated around the center of the original image
    win.blit(rotated_img, new_rect.topleft)

def shortest_path_binary_matrix(matrix1, start, target):
    # Make a copy of TRACK_GRID
    matrix= copy.deepcopy(matrix1) # ensures that the original constant is not edited

    if not matrix or not matrix[0] or matrix[start[1]][start[0]] == 0 or matrix[target[1]][target[0]] == 0:
        # Invalid matrix or starting/ending point blocked
        return []

    rows, cols = len(matrix), len(matrix[0]) # gets the number of rows and columns

    # Directions for moving up, down, left, and right (no diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize the queue with the starting point and path
    queue = deque([(start[0], start[1], [(start[0], start[1])])])  # (col, row, current path)
    #queue = ([(0,0 [(0,0)])])
    # the queue is able to store multiple current points and paths
    # meaning it can test all possibilities during one loop

    while queue:
        current_col, current_row, current_path = queue.popleft()
        # adds to the queue the current point the algorithm is at
        # and the path to that point

        # Check if reached the destination
        # if the current point is the target point
        if current_row == target[1] and current_col == target[0]:
            return current_path # return the path currently saved in queue

        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc

            # Check if the neighbor is within bounds and is an open cell (1)
            if 0 <= new_row < rows and 0 <= new_col < cols and matrix[new_row][new_col] == 1:
                # Mark the cell as visited by setting it to 0
                matrix[new_row][new_col] = 0
                # Add the neighbor to the queue with an updated path
                queue.append((new_col, new_row, current_path + [(new_col, new_row)]))
                print(queue)

    # If the queue is empty and destination is not reached, there is no path
    return []

class AbsractCar():
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0 #car starts stationary
        self.rotation_vel = rotation_vel
        self.angle = 0 # car starts unrotated
        self.x, self.y = self.START_POS
        self.acceleration = 0.1 # every frame the velocity increases by 0.1 pixels
        self.rect = self.img.get_rect(center = (self.x,self.y))
        self.points = 0

    def rotate(self, left=False, right=False):
        # rotates the car depending on keys pressed
        if left:
            self.angle+=self.rotation_vel
        elif right:
            self.angle-=self.rotation_vel

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) # self.vel becoems equal to vel + acceleration if that is lower than the max velocity
        # if that is greater than the max then self.vel is set to equal the max velocity
        self.move()

    def move_backward(self):
        # move backwards the max velocity is half forward max velocity
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        # cmoves the car at the angle of rotation multiplied by the velocity
        radians = math.radians(self.angle)
        vertical = math.cos(radians)*self.vel
        horizontal = math.sin(radians)*self.vel
        self.y += vertical
        self.x += horizontal

    def reduce_speed(self):
        #picks the max value between 0 and velocity - acceleration as it slows down the car
        self.vel = max(self.vel-self.acceleration/2, 0)
        self.move()

    def draw(self, win):
        # draws the car using the blit rotate function
        blit_rotate_centre(win,self.img, (self.x,self.y), self.angle)

    def collide(self, mask, x=0, y=0):
        # creates a mask for the car and uses pygame library for collision detection
        car_mask = pygame.mask.from_surface(self.img)
        offset = (self.x -x, self.y-y) 
        poi = mask.overlap(car_mask, offset)
        return poi # returns point of intersection if there is one, if not returns False

    def bounce(self):
        # car bounces off collisions
        self.vel = -self.vel/2
        self.move()

    def deliver_parcel(self,parcel, parcels): 
        if self.rect.colliderect(parcel): #Checks for collision between car rectangle and parcel rectangle
            parcels.remove(parcel) # removes collided parcel from sprite group
            self.points +=1 # increments player points by 1
            

# Create player car class
class PlayerCar(AbsractCar):
    IMG = RED_CAR
    START_POS = 13,24

    def update(self):
        # sets the rectangle center to new x and y values
        self.rect.center = (self.x,self.y)


class AICar(AbsractCar):
    IMG = YELLOW_CAR
    START_POS = 23,24

    def __init__(self, max_vel, rotation_vel,parcels):
        super().__init__(max_vel, rotation_vel) # initiates the parent class - Abstract Car
        # print('Initialized'); testing

        # movement
        self.rect = self.img.get_rect(center = (self.x,self.y)) # creates a rectangle with center self.x and self.y
        self.pos = self.rect.center
        self.direction = pygame.math.Vector2(0,0) # sets the initial direction to a vector of (0,0) so it is not moving and has no direction

        self.parcels = parcels
        # path
        # creates necessary variables for pathfinding 
        self.path = []
        self.collision_rects = []
        self.empty_path = []
        self.haspath = False
    
    def get_closest_parcel(self): # returns the closest parcel to the current position of AI car
        shortest_dist = 10000000
        for parcel in self.parcels:
            dist = abs((self.pos[0] - parcel.x)+(self.pos[1] - parcel.y))
            if dist < shortest_dist:
                shortest_dist = dist
                closest_parcel = parcel
            else:
                pass

        return closest_parcel

    def get_coords(self): # returns the column and row that the AI Car is currently in
        col = self.rect.centerx // 48
        row = self.rect.centery //48
        return col, row
    
    def get_start(self):
        # start
        return (int(self.pos[0] // 48), int(self.pos[1] // 48))  # gets the start column and row of the car

    def get_end(self):
        # end
        closest_parcel = self.get_closest_parcel()  # get the closest parcel to the car's current position
        point = (int(closest_parcel.pos[0] // 48), int(closest_parcel.pos[1] // 48))  # selects the closest parcel to be the end point of the path
        return point
    
    def set_path(self): # sets the path equal to the path found by the algorithm
        self.create_collision_rects() 
        self.get_direction()

    def create_collision_rects(self): # creates a list of rectangles to check the AI car is moving in the correct location
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] *48) +24
                y = (point[1] *48) +24
                rect = pygame.Rect((x-2,y-2),(4,4))
                self.collision_rects.append(rect)
    
    def get_direction(self): # sets the cars direction to head towards the next collision rectangle
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
            
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []
 
    def check_collisions(self): # checks that the car collides with the next collisions rectangle
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.empty_path
    
    def calculate_angle(self): # this will ensure the car rotates and looks like the player car when moving
        self.angle = math.degrees(math.atan2(abs(self.direction.y), self.direction.x))
        return self.angle
    def draw(self, win):# draw the ai car on the screen
        self.calculate_angle()
        blit_rotate_centre(win,self.img, (self.pos), self.angle)
    
    def deliver_parcel(self,parcel, parcels): 
        if self.rect.colliderect(parcel): #Checks for collision between car rectangle and parcel rectangle
            parcels.remove(parcel) # removes collided parcel from sprite group
            self.points +=1 # increments player points by 1
            self.haspath = False
            self.path = []
            if not parcels:
                # handle case when all parcels have been delivered
                ...
            
    def update(self):
        #print(f"AI Car Position: {self.pos[0]//48,self.pos[1]//48}, Direction: {self.direction}")
        self.pos += self.direction * 2
        self.check_collisions()
        self.rect.center = self.pos


class Parcel(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = PARCEL
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.pos = self.rect.center

    def draw(self, screen):
        screen.blit(self.image,(self.x,self.y)) # draws the parcel to the screen

    def update(self):
        self.rect.center = (self.x, self.y)
        self.pos = self.rect.center  # updates the centre of the rectangle with new coords

class Main():
    def __init__(self):
        #print(Track_Grid)
        # setting up the loop
        self.running = True

        # Instantiating player car
        self.player_car = PlayerCar(1,3)


        # Create Text
        self.text = FONT.render(f"Score: {self.player_car.points}", False, "#ffffff", (0,200,0)) # 
        self.textRect = self.text.get_rect()
        # Set the center of the rectangular object.
        self.textRect.center = (600,650)

        # creating parcels list
        self.parcels = pygame.sprite.Group()
        self.deliveries = 3

        self.ai_car=AICar(1,3,self.parcels)

    def create_parcels(self):
        track_mask = pygame.mask.from_surface(TRACK)

        while len(self.parcels) != 5: # THis could be done inside the parcels class to encapsulate the code.
            visited = []
            row = random.randint(1,13)
            col = random.randint(1,24)
            if TRACK_GRID[row][col] ==1 and (row,col) not in visited:
                parcel = Parcel(row*48,col*48)
                parcel_mask = pygame.mask.from_surface(PARCEL)
                offset = (parcel.x , parcel.y) 
                if track_mask.overlap(parcel_mask, offset):
                    visited.append((row,col))
                    self.parcels.add(parcel)
                else: pass
            else:pass
            print(TRACK_GRID)
        

    # Main Loop

    def run(self):
        self.create_parcels()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()
            moved = False

            if keys[pygame.K_a]:
                self.player_car.rotate(left=True)
            if keys[pygame.K_d]:
                self.player_car.rotate(right=True)
            if keys[pygame.K_w]:
                moved = True
                self.player_car.move_forward()
            if keys[pygame.K_s]:
                moved = True
                self.player_car.move_backward()
            if not moved:
                self.player_car.reduce_speed()

            # collisions
            if self.player_car.collide(TRACK_BORDER_MASK) is not None:
                self.player_car.bounce()

            if (
                self.player_car.x <= 0
                or self.player_car.y <= 0
                or self.player_car.x >= WIDTH
                or self.player_car.y >= HEIGHT
            ):
                self.player_car.bounce()

            for parcel in self.parcels:
                self.player_car.deliver_parcel(parcel, self.parcels)
                self.ai_car.deliver_parcel(parcel, self.parcels)

            SCREEN.fill((0, 200, 0))
            SCREEN.blit(TRACK, (0, 0))

            self.player_car.draw(SCREEN)
            self.ai_car.draw(SCREEN)

            for parcel in self.parcels:
                parcel.draw(SCREEN)
                parcel.update()

            if not self.ai_car.haspath:
                # AI car doesn't have a path, calculate the new path
                start = self.ai_car.get_start()
                target = self.ai_car.get_end()
                print(start, target)
                shortest_path = shortest_path_binary_matrix(list(TRACK_GRID),start, target)
                self.ai_car.path = shortest_path
                print(shortest_path)
                self.ai_car.set_path()
                self.ai_car.haspath = True
                #print(TRACK_GRID)

            self.player_car.update()
            self.ai_car.update()

            if self.player_car.points == 5:
                text = FONT.render(
                    f"Score: {self.player_car.points}, Player Wins!",
                    False,
                    "#ffffff",
                    (0, 200, 0),
                )
            else:
                text = FONT.render(
                    f"Score: {self.player_car.points}",
                    False,
                    "#ffffff",
                    (0, 200, 0),
                )

            SCREEN.blit(text, self.textRect)
            pygame.display.update()

# Instantiate and run the main loop
print(TRACK_GRID)
main = Main()
main.run()