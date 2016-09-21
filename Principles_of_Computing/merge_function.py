"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
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
        
   



