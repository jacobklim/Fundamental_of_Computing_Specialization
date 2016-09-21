# implementation of card game - Memory

import simplegui
import random

list1 = range(8)
list2 = range(8)
list_of_cards = list1 + list2
turns = 0

# helper function to initialize globals
def new_game():
    global list_of_cards, exposed, state, card_index1, card_index2, turns
    random.shuffle(list_of_cards)
    exposed = [False]*16
    state = 0
    card_index1 = 0
    card_index2 = 0
    turns = 0
# define event handlers
def mouseclick(pos):
    global state, card_index1, card_index2, turns
    for i in range(16):
        if not exposed[i]:
            if pos[0] > i *50 and pos[0] < (i+1)*50:
                if state == 0:            
                    exposed[i] = True
                    card_index1 = i
                    print "card_index1", card_index1
                    print list_of_cards[card_index1]
                    state = 1
                    print "state", state
                elif state == 1:
                    if pos[0] > i *50 and pos[0] < (i+1)*50:
                        exposed[i] = True
                        card_index2 = i
                        print "card_index2", card_index2
                        print list_of_cards[card_index2]
                        state = 2
                        print "state", state
                        turns += 1
                        label.set_text("Turns: " + str(turns))
                else:
                    if list_of_cards[card_index1] != list_of_cards[card_index2]:
                        exposed[card_index1] = False
                        exposed[card_index2] = False
                        card_index1 = 0
                        card_index2 = 0           
                    exposed[i] = True
                    card_index1 = i
                    print "card_index1",card_index1
                    state = 1
                    print "state", state
            
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    for i in range(16):
        if exposed[i]:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "black", "white")
            canvas.draw_text(str(list_of_cards[i]), [i*50 +20, 50], 30, "black")
        else:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "black", "green")
    label.set_text("Turns: " + str(turns))        
    

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns: " + str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric