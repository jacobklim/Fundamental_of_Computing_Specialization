"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) == 0:
            ##check if all tiles in rows i+1 or below are positioned 
            ##at their solved location 
            if target_row + 1 == self.get_height():
                return True
            else:
                for column in range(0, self.get_width()):
                    if not self.current_position(target_row + 1, column) == (target_row + 1, column):
                        return False
            ##check if all tiles in row i to the right of position (i,j) 
            ##are positioned at their solved location
            if target_col + 1 == self.get_width():
                return True
            else:                
                for right_tile in range(target_col + 1, self.get_width()):
                    if not self.current_position(target_row, right_tile) == (target_row, right_tile):
                        return False          
            return True
        else:
            return False
        
    def position_tile(self, target_row, target_col, row, column):
        '''
        place a tile at target position;
        target tile's current position must be either above the target position
        (k < i) or on the same row to the left (i = k and l < j);
        returns a move string
        '''
        move_string = ''
        combo = 'druld'

        # calculate deltas
        column_delta = target_col - column
        row_delta = target_row - row

        # always move up at first
        move_string += row_delta * 'u'
        # simplest case, both tiles in the same column, combo 'ld' shall go first
        if column_delta == 0:
            move_string += 'ld' + (row_delta - 1) * combo
        else:
            # tile is on the left form target, specific move first
            if column_delta > 0:
                move_string += column_delta * 'l'
                if row == 0:
                    move_string += (abs(column_delta) - 1) * 'drrul'
                else:
                    move_string += (abs(column_delta) - 1) * 'urrdl'
            # tile is on the right from target, specific move first
            elif column_delta < 0:
                move_string += (abs(column_delta) - 1)  * 'r'
                if row == 0:
                    move_string += abs(column_delta) * 'rdllu'
                else:
                    move_string += abs(column_delta) * 'rulld'
            # apply common move as last
            move_string += row_delta * combo

        return move_string

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        #find the current position
        current_row, current_col = self.current_position(target_row, target_col)
        #find the move string with the helper function
        move_string = self.position_tile(target_row, target_col, current_row, current_col)
        #update the puzzle
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        
        move_string = "ur"
        
        self.update_puzzle(move_string)
        
        current_row,current_col = self.current_position(target_row, 0)
               
        if current_row == target_row:
            step = (self.get_width() - 2) * "r"
            self.update_puzzle(step)
            move_string += step
        else:
            step = self.position_tile(target_row - 1, 1, current_row, current_col)
            step += 'ruldrdlurdluurddlu' + (self.get_width() - 1) * 'r'
            self.update_puzzle(step)
            move_string += step
        
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if (row == 0 and col > target_col) or (row == 1 and col >= target_col) or row > 1:
                    if not self.current_position(row, col) == (row, col):
                        return False
        
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self.lower_row_invariant(1, target_col):
            return False
        
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if not self.current_position(row, col) == (row, col):
                    return False
            
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        
        move_string = "ld"
        
        self.update_puzzle(move_string)
        
        current_row , current_col = self.current_position(0, target_col)
        
        if current_row == 0 and current_col == target_col:
            return move_string
        else:
            step = self.position_tile(1, target_col -1, current_row, current_col)
            step += "urdlurrdluldrruld"
            self.update_puzzle(step)
            move_string += step
        
        assert self.row1_invariant(target_col - 1)
        
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        current_row, current_col = self.current_position(1, target_col)
        move_string = self.position_tile(1, target_col, current_row, current_col)
        move_string += "ur"
        self.update_puzzle(move_string)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        #bring zero til to (0,0)
        self.update_puzzle("ul")
        #check if already solved
        if self.current_position(0,1) == (0,1) and self.current_position(1,1) == (1,1):
            return "ul"
        
        if self.get_number(0,1) < self.get_number(1,1):
            move_string = "rdlu"
            self.update_puzzle(move_string)
        else:
            move_string = "drul"
            self.update_puzzle(move_string)
        
        return "ul" + move_string
            
       
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        ##move zero tile at bottom right
        zero_current_row, zero_current_col = self.current_position(0,0)
        move_right = (self.get_width() - 1 - zero_current_col) * "r" 
        move_down = (self.get_height() - 1 - zero_current_row) * "d"
        move_string = move_right + move_down
        
        self.update_puzzle(move_string)
        
        for row in range(self.get_height()-1, 1, -1):
            for col in range(self.get_width()-1, -1, -1):
                move_string += self.solve_col0_tile(row) if col == 0 else self.solve_interior_tile(row, col)
        
        
        for col in range(self.get_width()-1, 1, -1):
            move_string += self.solve_row1_tile(col)
            move_string += self.solve_row0_tile(col)
        
        move_string += self.solve_2x2()
        
        return move_string
# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

#obj = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(obj)
#print obj.lower_row_invariant(2, 2)
#print obj.current_position(0,1)
#obj = Puzzle(3, 3, [[3, 0, 2], [1, 4, 5], [6, 7, 8]])
#print obj.row0_invariant(1)
#poc_fifteen_gui.FifteenGUI(obj)
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print obj.solve_2x2()
#print obj
#print obj.solve_puzzle()
#poc_fifteen_gui.FifteenGUI(obj)
#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#obj = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
#poc_fifteen_gui.FifteenGUI(obj)
##print obj
#print obj.solve_puzzle()
#puzzle=Puzzle(4, 4, [[15, 11, 8, 12], [14, 10, 9, 13], [2, 6, 1, 4], [3, 7, 5, 0]])
#sol=puzzle.solve_puzzle()
#print sol
#print len(sol)