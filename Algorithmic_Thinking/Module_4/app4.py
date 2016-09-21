"""Algorithm Thinking part II
    Application 4
"""

###Provided Code###

DESKTOP = True

import math
import random
import urllib2
import project4
import string

if DESKTOP:
    import matplotlib.pyplot as plt
    import project4 as student
else:
    import simpleplot
    import userXX_XXXXXXX as student

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"


###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)

    # read in files as string
    words = word_file.read()

    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list

def question_1():
    human = read_protein(HUMAN_EYELESS_URL)
    fly = read_protein(FRUITFLY_EYELESS_URL)

    scoring_matrix = read_scoring_matrix(PAM50_URL)

    alignment_matrix = project4.compute_alignment_matrix(human, fly, scoring_matrix, False)

    answer = project4.compute_local_alignment(human, fly, scoring_matrix, alignment_matrix)

    print "score =", answer[0]
    print "align human = ", answer[1]
    print "align fly = ", answer[2]

    return answer[0]

def question_2():

    human = read_protein(HUMAN_EYELESS_URL)
    fly = read_protein(FRUITFLY_EYELESS_URL)
    consensus = read_protein(CONSENSUS_PAX_URL)

    scoring_matrix = read_scoring_matrix(PAM50_URL)

    alignment_matrix_local = project4.compute_alignment_matrix(human, fly, scoring_matrix, False)

    local_aligns = project4.compute_local_alignment(human, fly, scoring_matrix, alignment_matrix_local)

    human_local_align = local_aligns[1]
    fly_local_align = local_aligns[2]

    human_no_dashes = human_local_align.replace('-','')
    fly_no_dashes = fly_local_align.replace('-','')

    global_matrix_human_consensus = project4.compute_alignment_matrix(human_no_dashes, consensus, scoring_matrix,True)
    global_matrix_fly_consensus = project4.compute_alignment_matrix(fly_no_dashes,consensus, scoring_matrix, True)

    global_align_human_consensus = project4.compute_global_alignment(human_no_dashes,consensus,scoring_matrix,global_matrix_human_consensus)
    align_global_human = global_align_human_consensus[1]

    global_align_fly_consensus = project4.compute_global_alignment(fly_no_dashes, consensus,scoring_matrix,global_matrix_fly_consensus)
    align_global_fly = global_align_fly_consensus[1]

    count_human = 0
    count_fly = 0

    #print align_global_human
    #print align_global_fly
    #print consensus

    for pair in zip(align_global_human, consensus):
        if pair[0] == pair[1]:
            count_human += 1.
    for pair in zip(align_global_fly,consensus):
        if pair[0] == pair[1]:
            count_fly += 1.

    human_percentage = (count_human / len(align_global_human)) * 100
    fly_percentage = (count_fly / len(align_global_fly)) * 100

    print "human percentage: ", human_percentage
    print "fly percentage: ", fly_percentage

def generate_null_distribution(seq_x, seq_y,scoring_matrix, num_trials):

    scoring_distribution = {}
    scores_list = []

    for i in range(num_trials):
        temp = list(seq_y)
        random.shuffle(temp)
        rand_y = ''.join(temp)

        align_matrix = project4.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)

        local_align = project4.compute_local_alignment(seq_x, rand_y, scoring_matrix, align_matrix)

        score = local_align[0]

        if score not in scoring_distribution:
            scoring_distribution[score] = 0

        scoring_distribution[score] += 1
        scores_list.append(score)

    return scoring_distribution, scores_list

def question_4(num_trials, flag):

    human = read_protein(HUMAN_EYELESS_URL)
    fly = read_protein(FRUITFLY_EYELESS_URL)

    scoring_matrix = read_scoring_matrix(PAM50_URL)

    scores, score_list = generate_null_distribution(human, fly, scoring_matrix, num_trials)

    if flag == True:

        x_axis = scores.keys()

        y_axis = []

        for appearence in scores.values():
            y_axis.append(appearence/float(num_trials))


        plt.bar(x_axis,y_axis)
        plt.xlabel('Scores')
        plt.ylabel('Fraction of total trials')
        plt.title('Distribution of scores')
        plt.tight_layout()
        plt.show()
    else:
        return score_list

def question_5(num_trials):

    scores_list = question_4(num_trials, False)

    s_score = question_1()

    mean_deviation = (sum(scores_list)) /num_trials

    standard_deviation = math.sqrt(sum((score - mean_deviation) **2 for score in scores_list) /num_trials)

    z_score = (s_score - mean_deviation) / standard_deviation

    print "mean deviation: ", mean_deviation
    print "standard deviation: ", standard_deviation
    print "z-score: ", z_score

def edit_distance(seq_x, seq_y):
    alphabet = string.ascii_lowercase
    scoring_matrix = project4.build_scoring_matrix(alphabet, 2, 1, 0)
    alignment_matrix = project4.compute_alignment_matrix(seq_x, seq_y, scoring_matrix,True)
    score = project4.compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix)
    return len(seq_x) + len(seq_y) - score[0]

def check_spelling(checked_word, dist, word_list):
    print "Start checking..."
    words = set()
    for word in word_list:
        if edit_distance(checked_word, word) <= dist:
            words.add(word)
            print "Word %s added"%word
    print "Total %d words added"%len(words)
    return words

def question_8():
    load_words = read_words(WORD_LIST_URL)
    humble = check_spelling('humble', 1, load_words)
    firefly = check_spelling('firefly', 2, load_words)
    return humble, firefly






