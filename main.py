# Imports
import pygame, os, math, random
from consts import *
from pathfinding.core.grid import Grid # imports libraries needed for AI pathfinding
from pathfinding.finder.a_star import AStarFinder
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

# Create AI class
class Pathfinder:
    def __init__(self, matrix,parcels):
        # setup
        self.matrix = matrix # matrix of available squares the car can move to
        self.parcels = parcels
        
        self.path = []

        # AI Car
        self.car = AICar(3,1, self.empty_path)
    
    def empty_path(self): # clears the path 
        self.path = []
    
    def get_closest_parcel(self): # returns the closest parcel to the current position of AI car
        shortest_dist = 10000000
        for parcel in self.parcels:
            dist = abs((self.car.pos[0] - parcel.x)+(self.car.pos[1] - parcel.y))
            if dist < shortest_dist:
                shortest_dist = dist
                closest_parcel = parcel
            else:
                pass

        return closest_parcel
    
    def get_start(self):
        # start 
        return (int(self.car.pos[0]//48), int(self.car.pos[1]//48)) # gets the start row and column of the car
        

    def get_end(self):
        # end
        closest_parcel = self.get_closest_parcel() # get the closest parcel to the car's current position
        return (int(closest_parcel.x//48), int(closest_parcel.y//48)) # selects the closest parcel to be the end point of the path
    
    def create_path(self):
        self.path = self.bfs()
    def bfs(self):
        start = self.get_start()
        end = self.get_end()
        print(start,end)
        queue = [[start]]
        visited = set()

        while queue:
            path = queue.pop(0)
            vertex = path[-1]

            if vertex == end:
                return path
            elif vertex not in visited:
                row, col = vertex
                for i in range(4):
                    if i == 0:  # Up
                        newRow = row - 1
                        newCol = col
                    elif i == 1:  # Down
                        newRow = row + 1
                        newCol = col
                    elif i == 2:  # Left
                        newRow = row
                        newCol = col - 1
                    elif i == 3:  # Right
                        newRow = row
                        newCol = col + 1
                    if 0 <= newRow < 14 and 0 <= newCol < 25 and TRACK_GRID[newRow][newCol] == 1:
                        new_vertex = (newRow, newCol)
                        new_path = list(path)
                        new_path.append(new_vertex)
                        queue.append(new_path)
                visited.add(vertex)

    def draw_path(self): # draws a line that shows the path the AI car should follow
        if self.path:
            points = []
            for point in self.path:
                x = (point[0]*48)+24
                y = (point[1]*48)+24
                points.append((x,y))

            pygame.draw.lines(SCREEN, '#4a4a4a', False, points, 5)
    
    def update(self):
        self.draw_path()

        # car
        self.car.update()
        self.car.draw(SCREEN)

class AICar(AbsractCar):
    IMG = YELLOW_CAR
    START_POS = 23,24

    def __init__(self, max_vel, rotation_vel ,empty_path):
        super().__init__(max_vel, rotation_vel) # initiates the parent class - Abstract Car
        # print('Initialized'); testing

        # movement
        self.rect = self.img.get_rect(center = (self.x,self.y)) # creates a rectangle with center self.x and self.y
        self.pos = self.rect.center
        self.direction = pygame.math.Vector2(0,0) # sets the initial direction to a vector of (0,0) so it is not moving and has no direction

        # path
        # creates necessary variables for pathfinding 
        self.path = []
        self.collision_rects = []
        self.empty_path = empty_path
        self.haspath = False

    def get_coords(self): # returns the column and row that the AI Car is currently in
        col = self.rect.centerx // 48
        row = self.rect.centery //48
        return col, row
    
    def set_path(self, path): # sets the path equal to the path found by the algorithm
        self.path = path
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
        self.angle = math.degrees(math.atan2(abs(self.direction.y), self.direction.x) )-90
        return self.angle
    def draw(self, win):# draw the ai car on the screen
        self.calculate_angle()
        blit_rotate_centre(win,self.img, (self.pos), self.angle)
    
    def deliver_parcel(self,parcel, parcels): 
        if self.rect.colliderect(parcel): #Checks for collision between car rectangle and parcel rectangle
            parcels.remove(parcel) # removes collided parcel from sprite group
            self.points +=1 # increments player points by 1
            self.haspath = False
            print(parcels)
            if not parcels:
                # handle case when all parcels have been delivered
                ...
    
    def update(self):
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

    def draw(self, screen):
        screen.blit(self.image,(self.x,self.y)) # draws the parcel to the screen

    def update(self):
        self.rect.center = (self.x,self.y) # updates the centre of the rectangle with new coords

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

    def create_parcels(self):
        track_mask = pygame.mask.from_surface(TRACK)

        while len(self.parcels) != 5: # THis could be done inside the parcels class to encapsulate the code.
            row = random.randint(1,13)
            col = random.randint(1,24)
            if TRACK_GRID[row][col] ==1:
                parcel = Parcel(row*48,col*48)
                parcel_mask = pygame.mask.from_surface(PARCEL)
                offset = (parcel.x , parcel.y) 
                if track_mask.overlap(parcel_mask, offset):
                    TRACK_GRID[row][col] = 2
                    self.parcels.add(parcel)
                else: pass
            else:pass
        '''
        for i in range(13):
            for j in range(24):
                if Track_Grid[i][j] == 2:
                    print(Track_Grid[i][j])
        '''

    # Main Loop
    def run(self):
        self.create_parcels()
        self.pathfinder = Pathfinder(TRACK_GRID,self.parcels)
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
            if self.player_car.collide(TRACK_BORDER_MASK) != None: #When the car is not touching the road this if occurs
                self.player_car.bounce()

            if self.player_car.x <= 0 or self.player_car.y <= 0 or self.player_car.x >= WIDTH or self.player_car.y >= HEIGHT:
                self.player_car.bounce()
            
            for parcel in self.parcels:
                self.player_car.deliver_parcel(parcel,self.parcels)
                self.pathfinder.car.deliver_parcel(parcel,self.parcels)


            SCREEN.fill((0,200,0))
            SCREEN.blit(TRACK,(0,0))
            #SCREEN.blit(PARCEL,(30,90))
            self.player_car.draw(SCREEN)

            for parcel in self.parcels:
                parcel.draw(SCREEN)
                parcel.update()

            if len(self.parcels)>0 and self.pathfinder.car.haspath == False:
                self.pathfinder.create_path()
                self.pathfinder.car.haspath= True

            self.player_car.update()
            self.pathfinder.update()
            if self.player_car.points == 5:
                text = FONT.render(f"Score: {self.player_car.points}, Player Wins!", False, "#ffffff", (0,200,0))
            else:
                text = FONT.render(f"Score: {self.player_car.points}", False, "#ffffff", (0,200,0))
            SCREEN.blit(text, self.textRect)
            pygame.display.update()

main = Main()
main.run()