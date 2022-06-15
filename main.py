"""
Author: Keegan Kresge
This file will find Watsky word grids based on his newest albums as seen below.
-----------
COM PLA INT
PLA CEM ENT
INT ENT ION
-----------
Each word can either be read along the rows or columns.


Note: I would love to see a variation of this code where the partitions can be different lengths, such as
------------
SL  I   CE
I   TE  M
CE  M   ENT
------------
"""


def get_params():
    """
    Asks user to input parameters for the watsky word grids, and returns parameters
    :return: [word length, partition length]
    """
    valid = False
    while not valid:  # Iterate until valid parameter values are given
        word_len = int(input("How long are the words? "))
        part_len = int(input("How long are the partitions? "))
        valid = (word_len % part_len) == 0
        if not valid: print("Those parameters don't work. Try again.")
    return word_len, part_len


def get_word_pool(word_len):
    """
    Retreives list of words of a given length
    :param word_len: lengths of words to retreive
    :return: list of words with length "word_len"
    """
    with open("words.txt") as word_file:
        words = []
        for line in word_file:
            line = line.strip()
            if len(line) == word_len: words.append(line)
    return words


def make_word_dict(word_pool, part_len, num_parts):
    """
    Makes a dictionary relating (word partition, index) tuples to the words that have that word partition at the index
    For instance, if the partition length is 3
                  ("PLA", 0) -> "PLACEMENT"
                  ("CEM", 1) -> "PLACEMENT"
                  ("ENT", 2) -> "PLACEMENT"
    :param word_pool: list of words to search through
    :param part_len: length of partitions
    :param num_parts: number of partitions in a given word
    :return: dictionary described above
    """
    d = dict()
    for word in word_pool:  # Add each word to the dictionary
        for idx in range(num_parts):  # iterate over each word partition
            tup = (word[idx * part_len:(idx + 1) * part_len], idx)
            if tup in d:  # If there are other words added already, add to the ongoing list
                d[tup].append(word)
            else:  # Otherwise, add list entry.
                d[tup] = [word]
    return d


def get_part(word, part_len, idx):
    """
    Get certain partition of a word, for instance get_part("PLACEMENT", 3, 2) == "ENT"
    :param word: word to partition
    :param part_len: length of partition
    :param idx: index of partition
    :return:
    """
    return word[part_len * idx:part_len * (idx + 1)]


def update_words(possible_words, lookup_dict, part_len, num_parts, word_idx):
    """
    Recursive function to find solutions to the word grid given a 2D array of possible word combinations
    :param possible_words: 2D array of possible words with the following format
           [ [first word],
             [list of potential second words],
             ...,
             [list of potential final words] ]
    :param lookup_dict: word lookup dictionary
    :param part_len: partition length
    :param num_parts: number of partitions / words
    :param word_idx: current word that is being decided/iterated through
    :return: a list of solutions with the following format
           [ [first, ..., last ], <- one solution
             [1st,   ..., nth  ], <- another solution
             ...,
             [one,   ..., final] ] <- final solution
    """
    solutions = []
    if word_idx == (num_parts - 1):  # If all filtering has been completed
        num_soln = len(possible_words[num_parts - 1])  # number of solutions for this set of possible words
        if num_soln == 0: return solutions
        for idx in range(num_parts - 1):  # reformat all but final words to be in a singular list
            solutions.append(possible_words[idx][0])
        solutions_temp = [solutions.copy() for _ in range(num_soln)]  # copy list "num_soln" times
        solutions = solutions_temp
        for idx in range(num_soln):  # add different final word to each copy of the list
            solutions[idx].append(possible_words[-1][idx])
    else:  # Otherwise, filter on the "word_idx"-th word
        for curr_word in possible_words[word_idx]:  # iterate over possible next words
            valid = True
            possible_words_copy = possible_words.copy()
            possible_words_copy[word_idx] = [curr_word]  # update copy of list with current word
            for part in range(word_idx + 1,
                              num_parts):  # iterate over partitions to the right of the word grid diagonal
                tup = (get_part(curr_word, part_len, part), word_idx)  # create search tuple
                if tup not in lookup_dict: valid = False; break  # if no words match search, move onto the next word.
                temp = lookup_dict[tup]  # get words that match search
                new_words = [word for word in temp
                             if word in possible_words_copy[part]]  # find words that overlap search and possible words
                if not len(new_words): valid = False; break  # if there are no overlapping words, move onto next word.
                possible_words_copy[part] = new_words  # update possible words copy with the potential new words
            if valid:  # if there are potential words, recurse on the set of potential words with updated word index
                solutions_temp = update_words(possible_words_copy, lookup_dict, part_len, num_parts, word_idx + 1)
                solutions = solutions + solutions_temp  # add solutions found to ongoing list of solutions
    return solutions


def find_words(word_len, part_len, num_parts):
    """
    Find solutions for the word grid
    :param word_len: word length
    :param part_len: partition length
    :return: list of solutions
    """
    # assign related variables
    word_pool = get_word_pool(word_len)
    lookup_dict = make_word_dict(word_pool, part_len, num_parts)

    # Find Words
    solutions = []
    for first in word_pool:  # iterate over possible first words
        possible_words = [[]] * num_parts  # create possible words structure
        possible_words[0] = [first]
        for part in range(1, num_parts):  # Iterate over partitions
            tup = (get_part(first, part_len, part), 0)
            if tup not in lookup_dict: break  # If there are no words that match the search, go to the next word.
            possible_words[part] = lookup_dict[tup]  # update possible words with words that match the search
        # Recurse
        solutions_temp = update_words(possible_words, lookup_dict, part_len, num_parts, 1)
        solutions = solutions + solutions_temp  # add solutions to ongoing list
    return solutions


def print_solutions(solutions, part_len, num_parts):
    """
    Print solutions to show the partitions
    :param solutions: list of solutions
    :param num_parts: number of partitions
    :return:
    """
    if not solutions: print("There are no word grids with the requested parameters. :(")
    for solution in solutions:
        print("---------------")
        for word in solution:
            for idx in range(num_parts):
                print(get_part(word, part_len, idx), end=" ")
            print()


if __name__ == '__main__':
    # Get parameters
    word_len, part_len = get_params()
    num_parts = word_len // part_len

    # Find and print solutions
    solutions = find_words(word_len, part_len, num_parts)
    print_solutions(solutions, part_len, num_parts)
