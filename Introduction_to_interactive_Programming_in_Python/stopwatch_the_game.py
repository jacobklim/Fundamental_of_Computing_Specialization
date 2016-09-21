# template for "Stopwatch: The Game"
import simplegui

# global variables
time = 0
width = 400
height =180
x = 0
y = 0
stop = False

#helper functions 

#converts time
#in tenths of seconds into formatted string A:BC.D
def format(t):
    global d
    whole_seconds = time // 10
    amount_of_seconds = whole_seconds % 60
    a = t // 600
    b = amount_of_seconds // 10
    c = amount_of_seconds % 10
    d = t % 10
    return str(a)+":"+str(b)+str(c)+"."+str(d)

#function that returns the score    
def score():
    return str(x)+"/"+str(y)
     
    
#event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    global stop
    timer.start()
    stop = True

def stop_button():
    global x, y, d, stop
    timer.stop()
    if stop:
        y += 1
        if d == 0:
            x += 1
    stop = False
    
    
def reset_button():
    global time, x, y
    timer.stop()
    time = 0
    x = 0
    y = 0

#event handler for timer with 0.1 sec interval
def timer_handler():
    global time
    time +=1
    

#draw handler
def draw_handler(canvas):
    global time
    #draws the timer
    canvas.draw_text(format(time), [width - 250, height/ 2], 36, "Red")
    #draws the score
    canvas.draw_text(score(), [340, 30], 28, "green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", width, height)
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start_button, 100)
frame.add_button("Stop", stop_button, 100)
frame.add_button("Reset", reset_button, 100)
# register event handlers
timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()



