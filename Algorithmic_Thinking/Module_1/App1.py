import urllib2
import matplotlib.pyplot as plt
import math
import random

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"


def load_graph(graph_url):
    # type: (object) -> object
    # type: (object) -> object
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


# citation_graph = load_graph(CITATION_URL)


def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph
    and computes the in-degrees
    for the nodes in the graph
    """

    in_degree = {}

    ##Initiate the degrees of the nodes to 0
    for dummy_node in digraph:
        in_degree[dummy_node] = 0

    ##Count the in-degree of the nodes
    for edge in digraph.values():
        for node in edge:
            in_degree[node] += 1

    return in_degree


def how_many(values, node):
    """
    Helper function to count the number of appearences
    in a list
    """
    count = 0
    for item in values:
        if item == node:
            count += 1
    return count


def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the unnormalized distribution
    of the in-degrees of the graph.
    """
    ##A list with the in-degree
    in_degrees = compute_in_degrees(digraph).values()

    ##A set from the in_degrees tha will be the keys for
    ##the output dictionary
    keys = set(in_degrees)

    ##Initiate an empty list to put the number of appearences for
    ##ever degree
    nodes = []

    ##Count the in-degree distribution with the helper function
    for degree in keys:
        nodes.append(how_many(in_degrees, degree))

    ##Make a dictionary from two lists keys and nodes
    degree_dist = dict(zip(keys, nodes))

    return degree_dist


def normalize_in_degree_dist(in_degree):
    """
    Function that converts the in-degree distribution to
    a fraction
    :return: a dictionary with normalized in-degree dist
    """

    #citation_graph = load_graph(CITATION_URL)

    degree_dist = in_degree_distribution(in_degree)

    total = float(sum(degree_dist.itervalues()))

    normalized_degree = {degree: nodes / total for degree, nodes in degree_dist.iteritems()}

    return normalized_degree

def question1():
    plot_dict = normalize_in_degree_dist(citation_graph)

    plt.plot(plot_dict.keys(), plot_dict.values(), 'bo')
    plt.loglog()

    plt.title("Normalized in-degree dist for citation graph (log base e)")
    plt.xlabel("In-degree")
    plt.ylabel("Distribution")
    #plt.xlim(0, 1000)
    plt.tight_layout()
    plt.show()


def algorith_er(n, p):
    graph = {key: set() for key in xrange(n)}
    for i in xrange(n):
        for j in xrange(n):
            if i == j:
                continue
            if random.random() < p:
                graph[i].add(j)
            if random.random() < p:
                graph[j].add(i)

    return graph



#citation_graph = load_graph(CITATION_URL)
#question1()

def question2():
    er_plot = normalize_in_degree_dist(algorith_er(3000, 0.1))

    plt.plot(er_plot.keys(), er_plot.values(), 'bo')
    #plt.loglog()
    plt.title("Normalized in-degree dist for algorith er graph (log base e)")
    plt.xlabel("In-degree")
    plt.ylabel("Distribution")
    plt.tight_layout()
    plt.show()

#question2()

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes num_nodes and
    returns a dictionary corresponding to a
    complete directed graph with the specified
    number of nodes
    """
    graph = {}
    edges = 0

    assert (num_nodes > 0), "Enter a positive number of nodes"
    ##in a completed directed graph the number
    ##of possible edges is given by the type: n * (n-1)
    total_number_edges = num_nodes * (num_nodes - 1)

    for node in xrange(num_nodes):

        graph[node] = set([dummy_edge for dummy_edge in xrange(num_nodes)])
        graph[node].remove(node)
        edges += len(graph[node])

    assert (total_number_edges == edges)

    return graph

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm

    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def avg_out_degree(graph):
    total = len(graph)

    average = sum(len(edges) for edges in graph.itervalues()) / total
    return average

#citation_graph = load_graph(CITATION_URL)
#print avg_out_degree(citation_graph)

def question3():
    citation_graph = load_graph(CITATION_URL)
    m = avg_out_degree(citation_graph)
    n = len(citation_graph)
    return n,m

#print question3()

def algorithm_dpa(n, m):
    graph = make_complete_graph(m)
    dpa = DPATrial(m)
    for i in xrange(m, n):
        graph[i] = dpa.run_trial(m)
    return graph

def question4():
    citation_graph = load_graph(CITATION_URL)
    m = avg_out_degree(citation_graph)
    dpa_plot = normalize_in_degree_dist(algorithm_dpa(27770, m))

    plt.plot(dpa_plot.keys(), dpa_plot.values(), 'bo')
    plt.loglog()
    plt.title("Normalized in-degree dist for algorith dpa graph (log base e)")
    plt.xlabel("In-degree")
    plt.ylabel("Distribution")
    plt.tight_layout()
    plt.show()

#question4()

def question5():
    graph = algorithm_dpa(27770, 12)
    citation_graph = load_graph(CITATION_URL)
    in_degrees_dpa = compute_in_degrees(graph)
    in_degrees_citation= compute_in_degrees(citation_graph)
    file_1 = open("dpa_graph_in_degrees", "w")
    file_2 = open("citation_graph_in_degrees", "w")
    print >> file_1, in_degrees_dpa
    print >> file_2, in_degrees_citation
    file_1.close()
    file_2.close()
question5()