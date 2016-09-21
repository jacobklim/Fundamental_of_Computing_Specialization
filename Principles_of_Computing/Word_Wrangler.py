"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    answer = []
    if list1 == []:
        answer = []
        return answer
    else:
        first = list1[0]
        if first not in list1[1 :]:
            answer = [first] + remove_duplicates(list1[1 :])
        else:
            answer = remove_duplicates(list1[1 :])
        return answer

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if (len(list1) == 0 or len(list2) == 0):
        return []
    if (len(list1) <= len(list2)):
        first = list1[0]
        if first in list2:
            return [first] + intersect(list1[1 :], list2)
        else:
            return intersect(list1[1 :], list2)
    else:
        first = list2[0]
        if first in list1:
            return [first] + intersect(list1, list2[1 :])
        else:
            return intersect(list1, list2[1 :])
    


def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    answer = []
    copy1  = list(list1)
    copy2 = list(list2)
   
    while len(copy1) > 0 and len(copy2) > 0:
        if copy1[0] < copy2[0]:
            answer.append(copy1[0])
            copy1.pop(0)
        else:
            answer.append(copy2[0])
            copy2.pop(0)
    
    if len(copy1) > len(copy2):
        return answer + copy1
    else:
        return answer + copy2
                                    
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    
    
    if len(list1) <= 1:
        return list1
    else:
        half = len(list1) / 2
        first_half = list1[: half]
        second_half = list1[half :]
        return merge(merge_sort(first_half), merge_sort(second_half))
        

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [word]
    else:
        first = word[0]
        rest = word[1:]
        
        rest_strings = gen_all_strings(rest)
        words = []
        for string in rest_strings:
            for index in range(len(string)+1):
                words.append(string[:index] + first + string[index:])
                
        return rest_strings + words        
        

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    return netfile.readlines()

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()



    
    