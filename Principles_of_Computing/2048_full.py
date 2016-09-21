"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result_list = [0] * len(line)
    medium_list = []
    zero = 0
    
    for non_zero in range(len(line)):
        if line[non_zero] > 0:
            medium_list.append(line[non_zero])
    
    for position in range(len(medium_list)):
        result_list.pop(position)
        result_list.insert(position, medium_list[position])
    
    
    for tile in range(len(result_list)):
        if tile + 1 > len(result_list) -1:
            break
        if result_list[tile] == result_list[tile + 1]:
            result_list[tile] *= 2
            result_list[tile+1] = 0
    
    
    while zero in result_list:
        result_list.remove(zero)              
    
   
    while len(result_list) != len(line):
        result_list.append(zero)
    
    
    return result_list

def get_initial_indices(width, height):
    """
    Helper function that gets the initial indices of
    a given board of a game
    """
    initial_indices = {}
    keys = [UP, DOWN, LEFT, RIGHT]
    up_indices = []
    down_indices = []
    left_indices = []
    right_indices = []
    
    for direction in keys:
        if direction == UP:
            for tile in range(width):
                up_indices.append((0, tile))
                initial_indices[direction] = up_indices
        elif direction == DOWN:
            for tile in range(width):
                down_indices.append((height-1, tile))
                initial_indices[direction] = down_indices
        elif direction == LEFT:
            for tile in range(height):
                left_indices.append((tile, 0))
                initial_indices[direction] = left_indices
        else:
            for tile in range(height):
                right_indices.append((tile, width-1))
                initial_indices[direction] = right_indices
    return initial_indices


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        __init__ method
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial_indices = get_initial_indices(self._grid_width, self._grid_height)
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._cells = [ [0 for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height) ]
        
        
        self.new_tile()
        self.new_tile()
        

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        #return "The 2048 board is " + str(self._cells)
        string = ""
        for row in range(self._grid_height):
            for column in range(self._grid_width):
                if column == self._grid_width -1:
                    string += str(self._cells[row][column]) + "\n"
                else:
                    string += str(self._cells[row][column]) +", "
        return "The 2048 board is "+ str(self._grid_height) + "x" + str(self._grid_width) + " and contains: " + "\n" + string
                

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        tiles_changed = False
        
        #create a list for the values of the initial tile
        #depending the direction
        if direction == UP or direction == DOWN:
            num_steps = self._grid_height
        else:
            num_steps = self._grid_width
        
        #iterate through the cells depending the direction
        for each_cell in self._initial_indices[direction]:
            
            cell_value_list = []
            #take the values of the cells
            for step in range(num_steps):
                row = each_cell[0] + step * OFFSETS[direction][0]
                col = each_cell[1] + step * OFFSETS[direction][1]
                cell_value_list.append(self._cells[row][col])
            
            #merge the list created above
            merged_list = merge(cell_value_list)
            
            #check if the values have changed
            if merged_list != cell_value_list:
                tiles_changed = True
            
            #put the merged list int the grid    
            for step in range(num_steps):
                row = each_cell[0] + step * OFFSETS[direction][0]
                col = each_cell[1] + step * OFFSETS[direction][1]
                self.set_tile(row, col, merged_list[step])
                
        if tiles_changed:
            self.new_tile()
                
             
                                                      
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        random_row = random.randrange(0, self._grid_height)
        random_col = random.randrange(0, self._grid_width)
        random_choice = random.choice([2]*90 + [4] * 10)
        
        if 0 in [num for elem in self._cells for num in elem]:            
            if self._cells[random_row][random_col] == 0:
                self._cells[random_row][random_col] = random_choice                
            else:
                self.new_tile()
        else:
            pass
            
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        
        return self._cells[row][col]




poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


