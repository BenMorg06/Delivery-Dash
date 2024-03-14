##################################
############ IMPORTS #############
##################################
import pygame.display, pygame.font, math, copy, random
pygame.display.init()
pygame.font.init()
from consts import *
from collections import deque
from utils import *

##################################
############ SCREEN ##############
##################################
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF) # sets dimensions of window
pygame.display.set_caption("Delivery Dash") # sets name of window

##################################
######### MATHS UTILITY ##########
##################################
def round(number):
    number = abs(number)
    decimal_part = number - int(number)
    #print(decimal_part)
    if decimal_part >= 0.5 or decimal_part <= -0.5:
        return math.ceil(number)
    else:
        return math.floor(number)

##################################
########### CAR CLASS ############
##################################
class AbsractCar():
    # INIT #
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0 #car starts stationary
        self.rotation_vel = rotation_vel
        self.angle = 0 # car starts unrotated
        self.x, self.y = self.START_POS
        self.acceleration = 0.1 # every frame the velocity increases by 0.1 pixels
        self.rect = self.img.get_rect(center = (self.x,self.y))
        self.points = 0

    # ROTATE #
    def rotate(self, left=False, right=False):
        # rotates the car depending on keys pressed
        if left:
            self.angle+= 90
        elif right:
            self.angle-= 90

    # MOVE FORWARDS #
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) # self.vel becoems equal to vel + acceleration if that is lower than the max velocity
        # if that is greater than the max then self.vel is set to equal the max velocity
        self.move()

    # MOVE BACKWARDS #
    def move_backward(self):
        # move backwards the max velocity is half forward max velocity
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    # MOVE #
    def move(self):
        # cmoves the car at the angle of rotation multiplied by the velocity
        radians = math.radians(self.angle)
        vertical = math.cos(radians)*self.vel
        horizontal = math.sin(radians)*self.vel
        self.y += vertical
        self.x += horizontal

    # REDUCE SPEED #
    def reduce_speed(self):
        #picks the max value between 0 and velocity - acceleration as it slows down the car
        self.vel = max(self.vel-self.acceleration/2, 0)
        self.move()

    # DRAW #
    def draw(self, win):
        # draws the car using the blit rotate function
        blit_rotate_centre(win,self.img, (self.x,self.y), self.angle)

    # COLLIDE #
    def collide(self, mask, x=0, y=0):
        # creates a mask for the car and uses pygame library for collision detection
        car_mask = pygame.mask.from_surface(self.img)
        offset = (self.x -x, self.y-y) 
        poi = mask.overlap(car_mask, offset)
        return poi # returns point of intersection if there is one, if not returns False

    # BOUNCE #
    def bounce(self):
        # car bounces off collisions
        self.vel = -self.vel/2
        self.move()

    # DELIVER PARCELS #
    def deliver_parcel(self,parcel, parcels): 
        if self.rect.colliderect(parcel): #Checks for collision between car rectangle and parcel rectangle
            parcels.remove(parcel) # removes collided parcel from sprite group
            self.points +=1 # increments player points by 1
            

##################################
######## PLAYER CAR CLASS ########
##################################
class PlayerCar(AbsractCar):
    START_POS = 13,24
    def __init__(self,max_vel,max_rotation,car_img):
        self.img = pygame.transform.rotozoom(car_img,0,0.5)
        super().__init__(max_vel,max_rotation)

    # UPDATE #
    def update(self):
        # sets the rectangle center to new x and y values
        self.rect.center = (self.x,self.y)

##################################
####### PATHFINDING CLASS ########
##################################
class Pathfinder:
    # INIT #
    def __init__(self, matrix,parcels):
        # setup
        self.matrix = matrix # matrix of available squares the car can move to
        self.parcels = parcels
        
        self.path = []

        # AI Car
        self.car = AICar(1,3, self.empty_path)
    
    # EMPTY PATH #
    def empty_path(self): # clears the path 
        self.path = []
    
    # GET CLOSEST PARCEL #
    def get_closest_parcel(self, parcels): # returns the closest parcel to the current position of AI car
        shortest_dist = 10000000
        for parcel in parcels:
            dist = abs((self.car.pos[0] - parcel.x)+(self.car.pos[1] - parcel.y)) # takes horizontal and vertical distance and adds the positive sum
            if dist < shortest_dist:
                shortest_dist = dist
                closest_parcel = parcel # parcel with shortest distance is the closest
            else:
                pass

        return closest_parcel
    
    # GET START #
    def get_start(self):
        # start
        return (int(self.car.pos[0] // 48), int(self.car.pos[1] // 48))  # gets the start column and row of the car

    # GET END #
    def get_end(self, parcels):
        # end
        closest_parcel = self.get_closest_parcel(parcels)  # get the closest parcel to the car's current position
        point = (int(closest_parcel.pos[0] // 48), int(closest_parcel.pos[1] // 48))  # selects the closest parcel to be the end point of the path
        return point
    
    # CREATE PATH #
    def create_path(self):
        start = self.get_start()
        end = self.get_end()
        self.path = self.shortest_path_binary_matrix(TRACK_GRID, start, end)
        #print(self.path)

    # SHORTEST PATH #
    def shortest_path_binary_matrix(self,matrix1, start, target):
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
                    #print(queue)

        # If the queue is empty and destination is not reached, there is no path
        return []

    # DRAW PATH # # TEST FUNCTION #
    def draw_path(self): # draws a line that shows the path the AI car should follow
        if self.path:
            points = []
            for point in self.path:
                x = (point[0]*48)+24
                y = (point[1]*48)+24
                points.append((x,y))

            #pygame.draw.lines(SCREEN, '#4a4a4a', False, points, 5)
    
    # UPDATE #
    def update(self):
        self.draw_path()

        # car
        self.car.update()
        self.car.draw(SCREEN)

##################################
############ AI CAR ##############
##################################
class AICar(AbsractCar):
    IMG = YELLOW_CAR
    START_POS = 23,24

    # INIT #
    def __init__(self, max_vel, rotation_vel ,empty_path):
        self.img = self.IMG
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

    # GET COORDS #
    def get_coords(self): # returns the column and row that the AI Car is currently in
        col = self.rect.centerx // 48
        row = self.rect.centery //48
        return col, row
    
    # SET PATH #
    def set_path(self, path): # sets the path equal to the path found by the algorithm
        self.path = path
        self.create_collision_rects() 
        self.get_direction()
    
    # CREATE COLLISION RECTS #
    # creates a list of rectangles to check the AI car is moving in the correct location #
    def create_collision_rects(self): 
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point[0] *48) +24
                y = (point[1] *48) +24
                rect = pygame.Rect((x-2,y-2),(4,4))
                self.collision_rects.append(rect)
    
    # GET DIRECTION #
    # sets the cars direction to head towards the next collision rectangle #
    def get_direction(self): 
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
            
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []
 
    # CHECK COLLISIONS #
    # checks that the car collides with the next collisions rectangle #
    def check_collisions(self): 
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.empty_path
    
    # CALCULATE ANGLE #
    # this will ensure the car rotates and looks like the player car when moving #
    def calculate_angle(self): 
        # print(self.direction[0],self.direction[1])
        # print(round(self.direction[0]),round(self.direction[1]))
        self.angle = math.degrees   (math.atan2(self.direction[0],self.direction[1]))
        return self.angle
    
    # DRAW #
    # draw the ai car on the screen #
    def draw(self, win):
        self.calculate_angle()
        blit_rotate_centre(win,self.img, (self.pos), self.angle)
    
    # DELIVER PARCEL #
    def deliver_parcel(self,parcel, parcels): 
        if self.rect.colliderect(parcel): #Checks for collision between car rectangle and parcel rectangle
            parcels.remove(parcel) # removes collided parcel from sprite group
            self.points +=1 # increments player points by 1
            self.haspath = False
            print(parcels)
            if not parcels:
                # handle case when all parcels have been delivered
                ...
    
    # UPDATE #
    def update(self):
        self.pos += self.direction
        self.check_collisions()
        self.rect.center = self.pos

##################################
########## PARCEL CLASS ##########
##################################
class Parcel(pygame.sprite.Sprite):
    
    # INIT #
    def __init__(self, x,y):
        super().__init__()
        self.image = PARCEL
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.pos = self.rect.center

    # DRAW #
    def draw(self, screen):
        screen.blit(self.image,(self.x,self.y)) # draws the parcel to the screen

    # UPDATE #
    def update(self):
        self.rect.center = (self.x,self.y) # updates the centre of the rectangle with new coords
        self.pos = self.rect.center  # updates the centre of the rectangle with new coords

##################################
########### MAIN CLASS ###########
##################################
class Main():
    # INIT #
    def __init__(self,car_img):
        #print(Track_Grid)
        # setting up the loop
        self.running = True

        # Instantiating player car
        self.player_car = PlayerCar(1,2,car_img)

        # Create Text
        self.text = FONT.render(f"Score: {self.player_car.points}", False, "#ffffff", (0,200,0)) # 
        self.textRect = self.text.get_rect()
        self.text2 = FONT.render(f'Score: {self.player_car.points}', False, "#ffffff", (0,200,0)) #
        self.textRect2 = self.text2.get_rect()
        # Set the center of the rectangular object.
        self.textRect.center = (600,650)
        self.textRect2.center = (600, 675)

        # creating parcels list
        self.parcels = pygame.sprite.Group()

        # pausing the game
        self.pause = False
        self.options_menu = False
        self.volume = game_volume
        self.sfx_volume = sfx_volume

        pygame.mixer.init()
        pygame.mixer.music.load(MENU_MUSIC)  # Replace with your audio file path
        # Set the volume (0.0 to 1.0)
        pygame.mixer.music.set_volume(game_volume)
        # Play the music on loop
        pygame.mixer.music.play(-1)

    # PAUSE GAME #
    def pause_game(self):
        # Set pause state True for the while loop
        self.pause = True
        # Create buttons
        self.resume_button = Button('Resume',self,300,60, (WIDTH//2 -150,250),6, 32)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,450),6, 32)
        # options button
        self.pressed = False
        self.elevation = 6
        self.dynamic_elevation = 6
        self.original_y_pos = 350
            # top rect
        self.top_rect = pygame.Rect((WIDTH//2 -150, 350),(300,60))
        self.top_color = '#52B788'
            # bottom rect
        self.bottom_rect = pygame.Rect((WIDTH//2 -150, 350),(300,6))
        self.bottom_color = '#2D6A4F'
            # text
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.text_surf = font.render('Options',True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

		# Create pause loop
        while self.pause:
			# Account For Hitting Escape to unPause
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = False
				# Account for clicking the X to quit
                if event.type == pygame.QUIT:
                    self.pause = False
                    self.running = False
                    pygame.quit()
                
            mouse_pos = pygame.mouse.get_pos()
            # this logic ensures the button is only clicked once
            if self.top_rect.collidepoint(mouse_pos):
                self.top_color = '#D74B4B'
                if pygame.mouse.get_pressed()[0]:
                    self.dynamic_elevation = 0
                    self.pressed = True
                else:
                    self.dynamic_elevation = self.elevation
                    if self.pressed == True:
                        self.pressed = False
                        self.pause = False
                        CLICK.play()
                        self.options()
            else:
                self.dynamic_elevation = self.elevation
                self.top_color = '#52B788'


            # DRAW #
            SCREEN.fill((0,200,0))
            SCREEN.blit(TRACK,(0,0))
            self.player_car.draw(SCREEN)
            self.pathfinder.car.draw(SCREEN)
            for parcel in self.parcels:
                parcel.draw(SCREEN)
            # Draw Buttons
            self.resume_button.draw(SCREEN)
            self.quit_button.draw(SCREEN)
            self.top_rect.y = self.original_y_pos - self.dynamic_elevation
            self.text_rect.center = self.top_rect.center
            self.bottom_rect.midtop = self.top_rect.midtop
            self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
            pygame.draw.rect(SCREEN,self.bottom_color,self.bottom_rect, border_radius=12)
            pygame.draw.rect(SCREEN, self.top_color, self.top_rect, border_radius=12)
            SCREEN.blit(self.text_surf, self.text_rect)


            pygame.display.flip()
    # Options Menu
    def options(self):
        #print('options')
        self.options_menu = True
        self.resume_button = Button('Resume',self,300,60, (50,600),6, 32)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH-350,600),6, 32)
        self.increase_vol_arrow = OptionsArrows(((WIDTH//2 + 320,HEIGHT//2 - 25),(WIDTH//2 + 320,HEIGHT//2 + 25),(WIDTH//2 + 350,HEIGHT//2)),(WIDTH//2 +320, HEIGHT//2 -25), IncreaseVol)
        self.decrease_vol_arrow = OptionsArrows(((WIDTH//2 - 320,HEIGHT//2 - 25),(WIDTH//2 -320,HEIGHT//2 + 25),(WIDTH//2 - 350,HEIGHT//2)),(WIDTH//2 -350, HEIGHT//2 -25), DecreaseVol)
        self.increase_sfx_arrow = OptionsArrows(((WIDTH//2 + 320,HEIGHT//2 - 125),(WIDTH//2 + 320,HEIGHT//2  -75),(WIDTH//2 + 350,HEIGHT//2-100)),(WIDTH//2 +320, HEIGHT//2 -125), IncreaseVol)
        self.decrease_sfx_arrow = OptionsArrows(((WIDTH//2 - 320,HEIGHT//2 - 125),(WIDTH//2 -320,HEIGHT//2  - 75),(WIDTH//2 - 350,HEIGHT//2-100)),(WIDTH//2 -350, HEIGHT//2 -125), DecreaseVol)
        self.optionsTitle = TITLE_FONT.render('Options', False, '#ffffff')
        self.optionsRect = self.optionsTitle.get_rect(center = (WIDTH//2, 150))
        while self.options_menu:
            #print('looping')
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = True
                        self.pause_game()
                if event.type == pygame.QUIT:
                    self.pause = False
                    self.running = False
                    quit()


            SCREEN.fill('#1B4332')
            SCREEN.blit(self.optionsTitle,self.optionsRect)
            # draw buttons
            self.increase_vol_arrow.draw(SCREEN, self.volume)
            self.volume = self.increase_vol_arrow.update_vol()
            self.decrease_vol_arrow.draw(SCREEN, self.volume)
            self.volume = self.decrease_vol_arrow.update_vol()
            self.increase_sfx_arrow.draw(SCREEN, self.sfx_volume)
            self.sfx_volume = self.increase_sfx_arrow.update_vol()
            self.decrease_sfx_arrow.draw(SCREEN, self.sfx_volume)
            self.sfx_volume = self.decrease_sfx_arrow.update_vol()
            pygame.mixer.music.set_volume(self.volume)
            CLICK.set_volume(self.sfx_volume)
            CARS_SFX.set_volume(self.sfx_volume)
            self.resume_button.draw(SCREEN)
            self.quit_button.draw(SCREEN)    
            # f string for volume
            self.volumeText = FONT.render(f"Music Volume: {math.trunc(100*(self.volume))}%", False, "#2D6A4F") #
            self.volumeRect = self.volumeText.get_rect(center = (WIDTH//2,350))
            self.sfxText = FONT.render(f"SFX Volume: {math.trunc(100*(self.sfx_volume))}%", False, "#2D6A4F") #
            self.sfxRect = self.volumeText.get_rect(center = (WIDTH//2,250))
            SCREEN.blit(self.volumeText, self.volumeRect)
            SCREEN.blit(self.sfxText, self.sfxRect)
            pygame.display.flip()

    # WIN #
    def win(self, winner):
        # Import Lobby class
        from lobby import Lobby
        # Check if winner is the player
        if winner == 'PLAYER':
            current_points = 0
            # Get the current users name
            f = open('current_user.csv', 'r')
            current_user = f.read()
            f.close()
            user_scores = {}
            # get the users current number of wins from the highscore.csv file
            f = open('highscores.csv', 'r')
            for line in f:
                user_scores[line.split(',')[0]] = line.split(',')[1].strip()
                if line.split(',')[0] == current_user:
                    current_points = line.split(',')[1]
                else:pass
            # increases the score of the current user by 1 in the dictionary
            user_scores[current_user] = str(int(current_points) + 1)
            # writes over the highscores file
            os.remove('highscores.csv')
            f = open('highscores.csv', 'w')
            for user in user_scores:
                f.write(user + ',' + user_scores[user] + '\n')
            f.close()

        # set up for the win screen
        self.winning = True
        self.title = TITLE_FONT.render('Delivery Dash', False, '#ffffff')
        self.title_rect = self.title.get_rect(center = (WIDTH//2, 68))
        self.lobby_button = Button('Lobby',Lobby(),300,60, (WIDTH//2 -150,400),6, 32)
        self.quit_button = Button('Quit',Quit,300,60, (WIDTH//2 -150,500),6,32)
        self.tab = Tabs(600,450,(WIDTH//2 -300, HEIGHT//2 -200))
        self.text = FONT.render(f"{winner} Won!", False, "#2D6A4F") #
        self.textRect = self.text.get_rect()
        self.textRect.center = (WIDTH//2,250)
        while self.winning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.winning = False
                    self.running = False
                    pygame.quit()
            # graphics
            SCREEN.fill('#1B4332')
            self.tab.draw(SCREEN)
            self.lobby_button.draw(SCREEN)
            self.quit_button.draw(SCREEN)
            SCREEN.blit(self.title, self.title_rect)
            SCREEN.blit(self.text, self.textRect)

            pygame.display.flip()
    # unPauses the game #
    def run(self):
        self.pause = False
        self.options_menu = False

    # CREATE PARCELS #
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
            else: pass

    # RUN GAME #
    def play(self):
        self.create_parcels()
        self.pathfinder = Pathfinder(TRACK_GRID,self.parcels)
        CARS_SFX.play(-1)

        # MAIN LOOP #
        while self.running:
            CLICK.set_volume(self.sfx_volume)
            CARS_SFX.set_volume(self.sfx_volume)
            # EVENT LOOP #
            event = pygame.event.poll()

            # QUIT #
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause:
                        self.pause = False
                    else:
                        CARS_SFX.stop()
                        CLICK.play()
                        self.pause_game()
                else: CARS_SFX.play(-1)
            
                if event.key == pygame.K_a:
                    self.player_car.rotate(left=True)
                else: pass
                if event.key == pygame.K_d:
                    self.player_car.rotate(right=True)
                else: pass
            
            
            # KEY PRESSES #
            keys = pygame.key.get_pressed()
            moved = False
            if keys[pygame.K_w]:
                moved = True
                self.player_car.move_forward()
            if keys[pygame.K_s]:
                moved = True
                self.player_car.move_backward()
            if not moved:
                self.player_car.reduce_speed()

            # COLLISIONS #
            if self.player_car.collide(TRACK_BORDER_MASK) != None: #When the car is not touching the road this if occurs
                self.player_car.bounce()

            if self.player_car.x <= 0 or self.player_car.y <= 0 or self.player_car.x >= WIDTH or self.player_car.y >= HEIGHT:
                self.player_car.bounce()
            
            for parcel in self.parcels:
                self.player_car.deliver_parcel(parcel,self.parcels)
                self.pathfinder.car.deliver_parcel(parcel,self.parcels)

            # DRAW #
            SCREEN.fill((0,200,0))
            SCREEN.blit(TRACK,(0,0))
            self.player_car.draw(SCREEN)


            # UPDATES #
            self.player_car.update()
            self.pathfinder.update()
            for parcel in self.parcels:
                parcel.draw(SCREEN)
                parcel.update()
            
            # FIND PATH #
            if not self.pathfinder.car.haspath and self.parcels:
                # AI car doesn't have a path, calculate the new path
                start = self.pathfinder.get_start()
                target = self.pathfinder.get_end(self.parcels)
                #print(start, target)
                shortest_path = self.pathfinder.shortest_path_binary_matrix(list(TRACK_GRID),start, target)
                self.pathfinder.path = shortest_path
                #print(shortest_path)
                self.pathfinder.car.set_path(shortest_path)
                self.pathfinder.car.haspath = True
                if self.pathfinder.car.pos == (target[1],target[0]):
                    self.pathfinder.car.haspath = False
                else: pass
                #print(TRACK_GRID)

            # TEXT #
            if self.player_car.points > self.pathfinder.car.points and self.player_car.points + self.pathfinder.car.points == 5:
                self.win('PLAYER')
            elif self.player_car.points < self.pathfinder.car.points and self.player_car.points + self.pathfinder.car.points == 5:
                self.win('AI')
            
            text = FONT.render(f"Score: {self.player_car.points}", False, "#ffffff", (0,200,0))
            text2 = FONT.render(f"Score: {self.pathfinder.car.points}", False, "#ffffff", (0,200,0))
            SCREEN.blit(text, self.textRect)
            SCREEN.blit(text2, self.textRect2)

            # UPDATE SCREEN #
            CLOCK.tick(FPS) # limit fps 
            pygame.display.flip()   

## RUN GAME ##
class running():
    def __init__(self, car_img):
        self.car_img = car_img
    
    # created so that the game can be played by running a button
    # solved a circular import issue
    def run(self):
        game = Main(self.car_img)
        game.play()

running(RED_CAR).run()
