# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle_accelaration = 5 
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = float(HEIGHT / 2)
paddle2_pos = float(HEIGHT / 2)
paddle1_vel = float(0)
paddle2_vel = float(0)

""" Start of the programme"""

#function that respawns the ball
def spawn_ball(direction):
    global ball_pos, ball_vel 
    
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    
    
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 140) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60
    elif direction == LEFT:
        ball_vel[0] = - random.randrange(120, 140) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60

#function for new game and event handler for reset button
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = float(HEIGHT / 2)
    paddle2_pos = float(HEIGHT / 2)
    paddle1_vel = float(0)
    puddle2_vel = float(0)
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

#draw function
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, direction
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2 , "white", "white")
    
    #draw puddles
    canvas.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT),\
                         (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),\
                       (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT),\
                         (0, paddle1_pos + HALF_PAD_HEIGHT)], 1, "white", "white")
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT),\
                         (WIDTH, paddle2_pos - HALF_PAD_HEIGHT),\
                        (WIDTH, paddle2_pos + HALF_PAD_HEIGHT),\
                        (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)], 1, "white", "white")
    
    #draw scores
    canvas.draw_text(str(score1), [150, 80], 70, "green")
    canvas.draw_text(str(score2), [400, 80], 70, "green")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #update puddles, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and \
    paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT: 
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and \
    paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    
    #checks and bounces the ball if collides to top and bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    #checks and respawn if the ball collides to left and right gutters    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: #left wall
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += ball_vel[0] * 0.10
            ball_vel[1] += ball_vel[1] * 0.10
        else:
            score2 +=1
            spawn_ball(RIGHT)
            
            
    if ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH - 1: #right wall
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += ball_vel[0] * 0.10
            ball_vel[1] += ball_vel[1] * 0.10
        else:    
            score1 += 1
            spawn_ball(LEFT)
    
#keydown hanlder    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= paddle_accelaration
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += paddle_accelaration
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= paddle_accelaration
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += paddle_accelaration

#keyup hanlder   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game, 100)

# start frame
new_game()
frame.start()
""" End of the programe"""