# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math
#global variables
num_range = 100
# helper function to start and restart the game
def new_game():
    global num_range, number_of_guesses, secret_number
    secret_number = random.randrange(0, num_range)
    number_of_guesses = math.ceil(math.log(num_range + 1, 2))
    print "New game: Range is 0 -",num_range
    print "You have " + str(number_of_guesses) + " guesses total"
    print
   
    
        
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range
    num_range = 100
    new_game()
   
   
    

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range
    num_range = 1000
    new_game()
   
    
def input_guess(guess):
    # main game logic goes here
    global number_of_guesses, secret_number
    victory = False
    print "Guess was " + guess
    guess = int(guess)
    number_of_guesses = number_of_guesses - 1
    print "You have ", number_of_guesses, " guesses left"
    
    if int(guess) == secret_number:
        victory = True
    elif int(guess) > secret_number:
        result = "Lower!!!"
    else:
        result = "Higher!!!"
        
    if victory:
        print "That is correct!! You Won!!"
        print
        new_game()
    elif number_of_guesses == 0:
        print "No guesses left!! You Loose!!"
        print
        new_game()
    else:
        print result
        print
#create frame
frame = simplegui.create_frame("Guess the number", 400, 200)
#register event handlers and start frame
frame.add_button("Range is [0-100)", range100, 200)
frame.add_button("Range is [0-1000)", range1000, 200)
frame.add_input("Enter guess", input_guess, 100)

frame.start()



# call new_game 
new_game()


# always remember to check your completed program against the 