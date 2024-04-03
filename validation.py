import hashlib
from lobby import *
class Validation():
    def __init__(self, csv, usr_input, password):
        self.input = usr_input
        self.csv = csv
        self.password = password
        self.password_incorrect = FONT.render(f"Password Incorrect", False, '#2D6A4F')
        self.password_rect = self.password_incorrect.get_rect(center = (WIDTH//2, 200))
        self.user_incorrect = FONT.render(f"Username Not Found", False, '#2D6A4F')
        self.user_rect = self.user_incorrect.get_rect(center = (WIDTH//2, 200))
        self.incorrect_password = False
        self.incorrect_user = False
        
    def run(self):
        # loop through csv and check if user is present in file
        # if user present then check if password is correct for user
        # if not create new user with such password
        # passwords should be hashed and comparison with hashed passwords
        users_pass = {}
        f = open(self.csv, 'r')
        for i in f.readlines():
            users_pass[i.split(',')[0]] = i.split(',')[1].strip()
        #print(self.input, users_pass.keys())
        if self.input in users_pass.keys():
            #print('username found')
            #print(users_pass[self.input])
            #print(self.password)
            if users_pass[self.input] == hashlib.sha1(self.password.encode()).hexdigest():
                f = open('current_user.txt', 'w')
                f.write(self.input)
                Lobby().run()
            else: 
                self.incorrect_password = True
                self.text_update()
        else:
            self.incorrect_user = True
            self.text_update()
    
    def text_update(self):
        return self.password_incorrect, self.password_rect, self.user_incorrect, self.user_rect, self.incorrect_password, self.incorrect_user
def presence_check(input):
    # checks if some text has been input
    if input != '':
        return True
    else: return False

def len_check(input, target_length):
    # checks the length of the input
    if len(input) <= target_length:
        return True
    else: return False

def type_check(input, target_type):
    # checks the type of the input
    if type(input) == type(target_type):
        return True
    else: return False

class NewUser():
    def __init__(self, csv, username, password):
        self.csv = csv
        self.username = username
        self.password = password
        self.user_error = FONT.render(f"User Already Exists", False, '#2D6A4F')
        self.user_error_rect = self.user_error.get_rect(center = (WIDTH//2, 200))
        self.user_success = FONT.render(f"User Created", False, '#2D6A4F')
        self.user_succes_rect = self.user_success.get_rect(center = (WIDTH//2, 200))
        self.user_exists = False
        self.new_user_made = False
    def run(self):
        # checks if username is already in file
        # if not then add user to file and add hashed password
        if presence_check(self.username) and type_check(self.password, 'string'):
            f = open(self.csv, 'r')
            for i in f.readlines():
                #print(i)
                #print(self.username)
                if i.split(',')[0] == self.username:
                    self.user_exists = True
                    #print('user already exists')

            if self.user_exists == False:
                f.close()
                f = open(self.csv, 'a')
                f.write(self.username + ',' + hashlib.sha1(self.password.encode()).hexdigest() + '\n')
                f.close()
                self.new_user_made = True
                #print('user created')

    def text_update(self):
        return self.user_error,self.user_error_rect,self.user_success,self.user_succes_rect,self.user_exists, self.new_user_made
                