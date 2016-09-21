"""
Week 2/ Project 2
"""
import random
from collections import deque

def bfs_visited(ugraph, start_node):
    """ Takes the undirected graph ugraph
    and the node start_node and returns the
    set consisting of all nodes that are
    visited by a breadth-first search
    that starts at start_node.
    """
    queque = deque()

    visited = set([start_node])

    queque.append(start_node)

    while queque:

        node = queque.popleft()

        for neighbor in ugraph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queque.append(neighbor)

    return visited

def cc_visited(ugraph):
    """Takes the undirected graph ugraph
    and returns a list of sets, where each
    set consists of all the nodes (and nothing else)
    in a connected component, and there is exactly
    one set in the list for each connected component
    in ugraph and nothing else."""

    remaining_nodes = set(ugraph.keys())

    connected_component = []

    while remaining_nodes:
        node = remaining_nodes.pop()
        visited = bfs_visited(ugraph, node)
        connected_component.append(visited)
        remaining_nodes -= visited

    return connected_component

def largest_cc_size(ugraph):
    """Takes the undirected graph ugraph
    and returns the size (an integer) of
    the largest connected component in ugraph."""

    largest_list = cc_visited(ugraph)

    if not len(ugraph):
        return 0

    return max(map(len, largest_list))

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph
def remove_node(ugraph, node):
    """Helper function"""
    for neighbor in ugraph[node]:
        ugraph[node].remove(neighbor)
    del ugraph[node]

def compute_resilience(ugraph, attack_order):
    """Takes the undirected graph ugraph,
    a list of nodes attack_order and iterates
     through the nodes in attack_order"""

    resilience = [largest_cc_size(ugraph)]
    #ugraph = copy_graph(ugraph)
    for node in attack_order:
        neighbors = ugraph[node]
        ugraph.pop(node)
        for neighbor in neighbors:
            ugraph[neighbor].remove(node)
        resilience.append(largest_cc_size(ugraph))

    return resilience

