import hashlib
from lobby import *
class Validation():
    def __init__(self, csv, usr_input, password):
        self.input = usr_input
        self.csv = csv
        self.password = password
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
            else: pass#print('password incorrect')
        else: pass#print('username not found')
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
    def run(self):
        # checks if username is already in file
        # if not then add user to file and add hashed password
        f = open(self.csv, 'r')
        for i in f.readlines():
            if i.split(',')[0] == self.username:
                print('user already exists')
            else:
                f.close()
                f = open(self.csv, 'a')
                f.write(self.username + ',' + hashlib.sha1(self.password.encode()).hexdigest() + '\n')
                f.close()
                print('user created')
                break