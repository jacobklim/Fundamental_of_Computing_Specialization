"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
            self._obstacle_list = obstacle_list
        else:
            self._obstacle_list = []
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
            
    def obstacle(self):
        '''
        generator that yields the list of obstacles
        '''
        for obstacle in self._obstacle_list:
            yield obstacle
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        #copy of the original grid
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        
        #compute distance field
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        
        
        for obstacle in self.obstacle():
            visited.set_full(obstacle[0], obstacle[1])
        
        #initiate boundary
        boundary = poc_queue.Queue()
        
        #boundary is a copy of human or zombie list
        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        else:
            for human in self.humans():
                boundary.enqueue(human)
        
        #set full the occupied cells accoording to the boundary list
        #set distance to zero for theese cells
        for cells in boundary:
            visited.set_full(cells[0], cells[1])
            distance_field[cells[0]][cells[1]] = 0
        
        while boundary:
            current_cell = boundary.dequeue()
            neighbors = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    distance_field[neighbor[0]][neighbor[1]] = min(distance_field[neighbor[0]][neighbor[1]], distance_field[current_cell[0]][current_cell[1]] + 1)
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
        
        return distance_field
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        moved_humans = []
        for human in self.humans():
            movable_cells = self.eight_neighbors(human[0],human[1])            
            distance = [zombie_distance_field[human[0]][human[1]]]            
            location = [human]
            movable = None
            for movable in movable_cells:
                if self.is_empty(movable[0], movable[1]):
                    distance.append(zombie_distance_field[movable[0]][movable[1]])
                    location.append(movable)
            
            best_distance = max(distance)
           
            best_location = location[distance.index(best_distance)]
            
            self.set_empty(movable[0],movable[1])
            moved_humans.append(best_location)
              
        self._human_list = moved_humans    	
            
            
            
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        moved_zombies = []
        for zombie in self.zombies():
            movable_cells = self.four_neighbors(zombie[0],zombie[1])            
            distance = [human_distance_field[zombie[0]][zombie[1]]]            
            location = [zombie]
            movable = None
            for movable in movable_cells:
                if self.is_empty(movable[0], movable[1]):
                    distance.append(human_distance_field[movable[0]][movable[1]])
                    location.append(movable)
            
            best_distance = min(distance)
           
            best_location = location[distance.index(best_distance)]
            
            self.set_empty(movable[0],movable[1])
            moved_zombies.append(best_location)
              
        self._zombie_list = moved_zombies  

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))


