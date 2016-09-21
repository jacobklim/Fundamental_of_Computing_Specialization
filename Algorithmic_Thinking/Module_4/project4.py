"""
Algorithm Thinking Part 2
Week 4
Project 4
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """Takes as input a set of characters alphabet and three scores
    diag_score, off_diag_score, and dash_score. The function returns
    a dictionary of dictionaries whose entries are indexed by pairs
    of characters in alphabet plus '-'.
    The score for any entry indexed by one or more dashes is
    dash_score. The score for the remaining diagonal entries is
     diag_score. Finally, the score for the remaining off-diagonal
     entries is off_diag_score."""

    scoring_matrix = {letter:{} for letter in alphabet}
    scoring_matrix["-"] = {}

    for row in scoring_matrix:
        for column in scoring_matrix:

            if row != "-" and column != "-":

                if row == column:
                    scoring_matrix[row][column] = diag_score
                else:
                    scoring_matrix[row][column] = off_diag_score

            if row == "-" or column == "-":
                scoring_matrix[row][column] = dash_score

    return scoring_matrix

def global_or_local(global_flag, score):
    """Helper function"""
    if global_flag:
        return score
    else:
        return max(0, score)

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """Takes as input two sequences seq_x and seq_y whose elements
    share a common alphabet with the scoring matrix scoring_matrix.
    The function computes and returns the alignment matrix for seq_x
    and seq_y as described in the Homework. If global_flag is True,
    each entry of the alignment matrix is computed using the method
    described in Question 8 of the Homework.
    If global_flag is False, each entry is computed using
    the method described in Question 12 of the Homework."""

    columns = len(seq_y) +1
    rows = len(seq_x) + 1

    alignment_matrix = [[0 for _ in range(columns)] for _ in range(rows)]

    for idx_i in range(1, rows):

        score = alignment_matrix[idx_i-1][0] + scoring_matrix[seq_x[idx_i-1]]["-"]
        alignment_matrix[idx_i][0] = global_or_local(global_flag, score)

    for idx_j in range(1, columns):

        score = alignment_matrix[0][idx_j-1] + scoring_matrix["-"][seq_y[idx_j-1]]
        alignment_matrix[0][idx_j] = global_or_local(global_flag, score)

    for idx_i in range(1, rows):
        for idx_j in range(1, columns):

            score = max(alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]],
                        alignment_matrix[idx_i-1][idx_j] + scoring_matrix[seq_x[idx_i-1]]["-"],
                        alignment_matrix[idx_i][idx_j-1] + scoring_matrix["-"][seq_y[idx_j-1]])

            alignment_matrix[idx_i][idx_j] = global_or_local(global_flag, score)


    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix.
    This function computes a global alignment of seq_x and seq_y
    using the global alignment matrix alignment_matrix.The function
    returns a tuple of the form (score, align_x, align_y) where score
    is the score of the global alignment align_x and align_y.
    Note that align_x and align_y should have the same length
    and may include the padding character '-'."""

    idx_i = len(seq_x)
    idx_j = len(seq_y)

    align_x = ""
    align_y = ""

    while idx_i != 0 and idx_j != 0:

        if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j-1] + scoring_matrix[seq_x[idx_i-1]][seq_y[idx_j-1]]:

            align_x = seq_x[idx_i-1] + align_x
            align_y = seq_y[idx_j-1] + align_y

            idx_i -= 1
            idx_j -= 1

        else:

            if alignment_matrix[idx_i][idx_j] == alignment_matrix[idx_i-1][idx_j] + scoring_matrix[seq_x[idx_i-1]]["-"]:

                align_x = seq_x[idx_i-1] + align_x
                align_y = "-" + align_y

                idx_i -= 1
            else:
                align_x = "-" + align_x
                align_y = seq_y[idx_j-1] + align_y

                idx_j -= 1

    while idx_i != 0:

        align_x = seq_x[idx_i-1] + align_x
        align_y = "-" + align_y

        idx_i -= 1

    while idx_j != 0:

        align_x = "-" + align_x
        align_y = seq_y[idx_j-1] + align_y

        idx_j -= 1

    return alignment_matrix[len(seq_x)][len(seq_y)], align_x, align_y

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """Takes as input two sequences seq_x and seq_y whose elements share a
    common alphabet with the scoring matrix scoring_matrix. This function
    computes a local alignment of seq_x and seq_y using the local alignment
    matrix alignment_matrix.The function returns a tuple of the form (score,
    align_x, align_y) where score is the score of the optimal local alignment
    align_x and align_y. Note that align_x and align_y should have the same
    length and may include the padding character '-'."""

    align_x = ""
    align_y = ""

    ##find maximum score and position
    max_score = 0
    max_i = 0
    max_j = 0

    for dummy_i in range(len(seq_x)+1):
        for dummmy_j in range(len(seq_y)+1):
            if alignment_matrix[dummy_i][dummmy_j] > max_score:
                max_i = dummy_i
                max_j = dummmy_j
                max_score = alignment_matrix[dummy_i][dummmy_j]

    while max_i != 0 and max_j != 0 and alignment_matrix[max_i][max_j] != 0:

        if alignment_matrix[max_i][max_j] == alignment_matrix[max_i - 1][max_j - 1] + scoring_matrix[seq_x[max_i - 1]][seq_y[max_j - 1]]:

            align_x = seq_x[max_i - 1] + align_x
            align_y = seq_y[max_j - 1] + align_y

            max_i -= 1
            max_j -= 1

        else:

            if alignment_matrix[max_i][max_j] == alignment_matrix[max_i - 1][max_j] + scoring_matrix[seq_x[max_i - 1]]["-"]:

                align_x = seq_x[max_i - 1] + align_x
                align_y = "-" + align_y

                max_i -= 1
            else:
                align_x = "-" + align_x
                align_y = seq_y[max_j - 1] + align_y

                max_j -= 1

    return max_score, align_x, align_y
