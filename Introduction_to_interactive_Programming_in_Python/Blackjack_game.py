# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
player_score = 0
dealer_score = 0
player_choise = ""
who_won = ""
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_cards = []	# create Hand object

    def __str__(self):# return a string representation of a hand
        hand_print = ""
        for i in range(len(self.hand_cards)):
            hand_print += " " + str(self.hand_cards[i])
        return "Hand contains: " + hand_print
                  
    def add_card(self, card):
        self.hand_cards.append(card) # add a card object to a hand

    def get_value(self):
        
        hand_value = 0
        ace = False
        
        for card in self.hand_cards:
            rank = card.get_rank()
            hand_value += VALUES[rank]
            if rank == "A":
                ace = True
            
        if not ace:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
    def draw(self, canvas, pos):# draw a hand on the canvas, use the draw method for cards
        for card in self.hand_cards:
            card.draw(canvas, pos)
            pos[0] += 100
 
        
# define deck class 
class Deck:
    def __init__(self):# create a Deck object
        self.deck_cards = []
        for s in SUITS:
            for r in RANKS:
                self.deck_cards.append(Card(s,r))
    
    def shuffle(self):
        return random.shuffle(self.deck_cards)

    def deal_card(self):
        return self.deck_cards.pop()
    
    def __str__(self):
        deck_print = ""
        for i in range(len(self.deck_cards)):
            deck_print += " " + str(self.deck_cards[i])
        return "Deck contains: " + deck_print


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, outcome, player_choise, dealer_score, who_won
    if in_play:
        outcome = "New deal?"
        who_won = "Dealer wins!!"
        dealer_score += 1
        in_play = False
    else:
        deck = Deck()
        deck.shuffle()
    
        player = Hand()
        dealer = Hand()
    
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
    
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        
        in_play = True
        outcome = "Hit or stand? " + "Hand: " + str(player.get_value())
        player_choise = ""
        who_won = ""
    

def hit():
    global in_play, outcome, dealer_score, player_choise, who_won
    
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            player_choise = "Player hitted!"
            outcome = "Hit or stand? " + "Hand: " + str(player.get_value())
            
    
        if  player.get_value() > 21:
            in_play = False
            outcome = "New deal?"
            who_won = "Busted!! Dealer wins!!"
            player_choise = ""
            dealer_score += 1
       
def stand():
    global in_play, outcome, player_score, dealer_score, player_choise, who_won
            
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
        
    if in_play:
        if dealer.get_value() > 21:        
            outcome = "New deal?"
            who_won = "Dealer busted! You win!!"
            player_choise = ""
            player_score += 1
        else:
            if dealer.get_value() >= player.get_value() or player.get_value() > 21:            
                outcome = "New deal?"
                who_won = "Dealer wins!!"
                player_choise = ""
                dealer_score += 1
            else:            
                outcome = "New deal??"
                who_won = "Player wins!!"
                player_choise = ""
                player_score += 1
    
    in_play = False 

# draw handler    
def draw(canvas):
    global outcome, dealer_score, player_score, player_choise, who_won
    
    canvas.draw_text("Blackjack", (50, 70), 40, "cyan") #draws the blackjack message
    
    canvas.draw_text("Dealer", (50, 120), 25, "black") #draws player's label
    canvas.draw_text("Player", (50, 380), 25, "black") #draws dealer's label
    
    canvas.draw_text("Score: " + str(dealer_score), (200, 120), 25, "red") #draws dealer's score
    canvas.draw_text("Score: " + str(player_score), (200, 380), 25, "red") #draws player's score
    
    canvas.draw_text(outcome, (50, 420), 25, "black") #draws player's choice
    canvas.draw_text(player_choise, (400, 420), 25, "black")
    canvas.draw_text(who_won, (50, 290), 30, "red" )
    
                     
    player.draw(canvas, [50, 450]) #draw player cards
    dealer.draw(canvas, [50, 150]) #draw dealer cards
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (86,198), CARD_BACK_SIZE)
    else:    
        canvas.draw_text("Player hand: " + str(player.get_value()), (380,320), 25, "blue")
        canvas.draw_text("Dealer hand: " + str(dealer.get_value()), (380,350), 25, "blue")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
