"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10      # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player
    by making random moves, alternating between players. 
    The function should return when the game is over. 
    The modified board will contain the state of the game, 
    so the function does not return anything. 
    In other words, the function should modify the board input.
    """
    
    empty_squares = board.get_empty_squares()
    
    while empty_squares:
        
        #randomly pick an empty square and assign it to player provided
        square_to_assign = random.choice(empty_squares)
        
        board.move(square_to_assign[0], square_to_assign[1], player)
        
        empty_squares.remove(square_to_assign)
        
        #checks if the game is in progress
        if board.check_win():            
            break
        
        player = provided.switch_player(player)
        
    
def mc_update_scores(scores, board, player):
    """
     This function takes a grid of scores (a list of lists)
     with the same dimensions as the Tic-Tac-Toe board, 
     a board from a completed game, 
     and which player the machine player is. 
     The function should score the completed board and update the scores grid. 
     As the function updates the scores grid directly, 
     it does not return anything,
    """
    winner = board.check_win()
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            player = board.square(row, col)
            if player == provided.PLAYERX:
                if winner == provided.PLAYERX:
                    scores[row][col] += SCORE_CURRENT
                elif winner == provided.PLAYERO:
                    scores[row][col] += -SCORE_OTHER
            elif player == provided.PLAYERO:
                if winner == provided.PLAYERX:
                    scores[row][col] += -SCORE_OTHER
                elif winner == provided.PLAYERO:
                    scores[row][col] += SCORE_CURRENT
            else:
                # the rest is 0 value, don't care as it has no effect on score
                pass
            
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with the 
    maximum score and randomly return one of them as a (row, column) tuple. 
    It is an error to call this function with a board that has 
    no empty squares (there is no possible next move), 
    so your function may do whatever it wants in that case. 
    The case where the board is full will not be tested.
    """
    empty_squares = board.get_empty_squares()
    
    if len(empty_squares) == 0:
        print "error no empty squares"
    
    best_score = None
    best_move = None
    
    for square in empty_squares:
        if best_move == None or scores[square[0]][square[1]] > best_score:
            best_move = square
            best_score = scores[square[0]][square[1]]
    return best_move

def mc_move(board, player, trials):
    """
    This function takes a current board,
    which player the machine player is,
    and the number of trials to run.
    The function should return a move for the machine player
    in the form of a (row, column) tuple.
    """
    initial_scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]

    for dummy_trial in range(trials):
        cloned = board.clone()
        mc_trial(cloned, player)
        mc_update_scores(initial_scores, cloned, player)
        
    return get_best_move(board, initial_scores)

        
        
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
