"""Week 4/ Application 2"""

##General Imports
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt
import UPATrial
import Project_2

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


###Provided Code for loading the graph###
def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[: -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1: -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


###Provided code - Helper functions###

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph


def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)


def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order


###ER-algorithm###
def algorithm_er(n, p):
    graph = {key: set() for key in xrange(n)}
    for i in xrange(n):
        for j in xrange(n):
            if i == j:
                continue
            if random.random() < p:
                graph[i].add(j)
            #if random.random() < p:
                graph[j].add(i)
                #graph[j].add(i)

    return graph


###UPA algorithm###
def algorithm_upa(n, m):
    graph = make_complete_undirected_graph(m)
    upa = UPATrial.UPATrial(m)
    for i in xrange(m, n):
        neighbors = upa.run_trial(m)
        graph[i] = neighbors
        for neighbor in neighbors:
            graph[neighbor].add(i)
    return graph


###MAke completd undirected graph###
def make_complete_undirected_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and
    returns a dictionary corresponding to a
    complete undirected graph with the specified
    number of nodes
    """
    graph = {}
    edges = 0

    assert (num_nodes > 0), "Enter a positive number of nodes"
    ##in a completed directed graph the number
    ##of possible edges is given by the type: n * (n-1)
    total_number_edges = (num_nodes * (num_nodes - 1)) / 2

    for node in xrange(num_nodes):
        graph[node] = set([dummy_edge for dummy_edge in xrange(num_nodes)])
        graph[node].remove(node)
        edges += len(graph[node])

    assert (total_number_edges == edges / 2)
    return graph


###Make a rando undirected graph (ER)
def make_random_undirected_graph(num_nodes, p):
    #graph = {key: set() for key in xrange(num_nodes)}
    graph = {}
    for node in xrange(num_nodes):
        if node not in graph:
            graph[node] = set()
        for dummy_edge in xrange(num_nodes):
            if node != dummy_edge:

                a = random.random()
                if p > a:
                    graph[node].add(dummy_edge)
                    #graph[dummy_edge].add(node)
                    if dummy_edge not in graph:
                        graph[dummy_edge] = set([node])
                    else:
                        graph[dummy_edge].add(node)
    return graph

def make_random_undirected_graph2(num_nodes, probility):
    """
        Takes the number of nodes n and the probility p
        returns a dictionary corresponding to a random undirected graph
        with the specified number of nodes. (Algorithm ER)
        """
    graph = {}
    edges = 0
    for dummy_node in range(num_nodes):
        if dummy_node not in graph:
            graph[dummy_node] = set()
        for dummy_node_pair in range(num_nodes):
            if dummy_node_pair != dummy_node:
                a = random.random() # a real number [0,1)
                if a < probility:
                    print dummy_node, dummy_node_pair
                    graph[dummy_node].add(dummy_node_pair)
                    if dummy_node_pair not in graph:
                        graph[dummy_node_pair] = set([dummy_node])
                    else:
                        graph[dummy_node_pair].add(dummy_node)
        edges += len(graph[dummy_node])
    print "number of edges are ", edges/2

    return graph


###Count the total number of egdes in an udirected graph###
def num_of_edges(ugraph):
    """Compute how many edges the graph contains"""
    return sum([len(v) for k, v in ugraph.iteritems()]) / 2

def count_edges(ugraph):
    edges = 0
    for node in ugraph:
        for neighbor in graph[node]:
            edges += 1
    return edges / 2


###Helper function###
def random_order(ugraph):
    # type: (object) -> object
    """Shuffle the nodes"""
    nodes = ugraph.keys()
    random.shuffle(nodes)
    return nodes


###Question 1 answer###
def question_1():
    er_graph = algorithm_er(1239, 0.002)
    upa_graph = algorithm_upa(1239, 3)
    network_graph = load_graph(NETWORK_URL)

    er_random = random_order(er_graph)
    upa_random = random_order(upa_graph)
    network_random = random_order(network_graph)

    network_resilience = Project_2.compute_resilience(network_graph, network_random)
    er_resilience = Project_2.compute_resilience(er_graph, er_random)
    upa_resilience = Project_2.compute_resilience(upa_graph, upa_random)

    plt.plot(range(len(network_resilience)), network_resilience, '-r', label='Network graph')
    plt.plot(range(len(er_resilience)), er_resilience, '-b', label='ER-generated (p = 0.002)')
    plt.plot(range(len(upa_resilience)), upa_resilience, '-g', label='UPA-generated (m = 3)')
    plt.title('Graph resilience')
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


###Fast targeted order function####
def fast_targeted_order(ugraph):
    """Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes"""

    copy = copy_graph(ugraph)

    degree_sets = {}

    for k in range(len(copy)):
        degree_sets[k] = set([])

    for i in copy:
        d = len(copy[i])
        degree_sets[d].add(i)

    attack_order = []

    for k in range(len(copy)-1, -1, -1):
        while len(degree_sets[k]):
            u = degree_sets[k].pop()
            for neighbor in copy[u]:
                d = len(copy[neighbor])
                degree_sets[d].remove(neighbor)
                degree_sets[d-1].add(neighbor)

            attack_order.append(u)
            delete_node(copy, u)

    return attack_order

###Start of Question 3####
def compute_time_targeted():
    targeted_time = []
    for node in range(10, 1000, 10):
        upa_graph = algorithm_upa(node, 5)
        start_time = time.time()
        targeted_order(upa_graph)
        end_time = time.time()
        duration = end_time - start_time
        targeted_time.append(duration)
    return targeted_time

def compute_time_fast_targeted():
    fast_targeted_time = []
    for node in range(10, 1000, 10):
        upa_graph  = algorithm_upa(node, 5)
        start_time = time.time()
        fast_targeted_order(upa_graph)
        end_time = time.time()
        duration = end_time - start_time
        fast_targeted_time.append(duration)
    return fast_targeted_time

def question_3():
    targeted_time = compute_time_targeted()
    fast_targeted_time = compute_time_fast_targeted()

    plt.plot(range(10,1000,10), targeted_time, '-b', label = 'targeted order')
    plt.plot(range(10,1000,10), fast_targeted_time, '-r', label = 'fast targeted order')
    plt.legend(loc='upper right')
    plt.title(" Plot of running time of desktop Python")
    plt.xlabel("Number of nodes")
    plt.ylabel("Running times")
    plt.show()

####Question 4####

def question_4():
    network_graph = load_graph(NETWORK_URL)
    er_graph = algorithm_er(1239, 0.002)
    upa_graph = algorithm_upa(1239, 3)

    network_target_order = fast_targeted_order(network_graph)
    er_target_order = fast_targeted_order(er_graph)
    upa_target_order = fast_targeted_order(upa_graph)

    network_resilience = Project_2.compute_resilience(network_graph,network_target_order)
    er_resilience = Project_2.compute_resilience(er_graph, er_target_order)
    upa_resilience = Project_2.compute_resilience(upa_graph, upa_target_order)

    plt.plot(range(len(network_resilience)), network_resilience, '-r', label='Network graph')
    plt.plot(range(len(er_resilience)), er_resilience, '-b', label='ER-generated (p = 0.002)')
    plt.plot(range(len(upa_resilience)), upa_resilience, '-g', label='UPA-generated (m = 3)')

    plt.title('Graph resilience after targeted order')
    plt.xlabel('Number of nodes removed')
    plt.ylabel('Size of the largest connected component')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

