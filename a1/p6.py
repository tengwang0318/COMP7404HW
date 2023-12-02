import sys, parse, grader, copy
from collections import defaultdict
from copy import deepcopy
from math import comb


def number_of_attacks(problem: list[list[str]]):
    """
    this function doesn't perform well due to inflexibility of the data structure in the problem.
    In Problem 8, I refactor this function and named a new one as counter_number_of_attack()

    speed-up method:
        use hash-table to accelerate the find-up procedure.
    create three tables:
        1. row_to_cols: key: row, val: [cols]
        2. primary_diagonal: key: (row+col), val: cnt
        3. secondary_diagonal: key: (row-col), val: cnt

    :param problem: n*n lists
    :return:
    """

    n = len(problem)
    row_to_cols, primary_diagonal, secondary_diagonal = defaultdict(list), defaultdict(int), defaultdict(int)
    col_to_row = {}
    for i in range(n):
        for j in range(n):
            if problem[i][j] == "q":
                row_to_cols[i].append(j)
                primary_diagonal[i + j] += 1
                secondary_diagonal[i - j] += 1
                col_to_row[j] = i

    def helper(row, col, position):
        """
            find every node which is in the same row, top-left diagonal, or top-right diagonal.
            Then use combination to calculate the number
        """
        temp_row_to_cols, temp_primary_diagonal, temp_secondary_diagonal = deepcopy(row_to_cols), \
            deepcopy(primary_diagonal), deepcopy(secondary_diagonal)

        temp_primary_diagonal[position + col] += 1
        temp_primary_diagonal[row + col] -= 1

        temp_secondary_diagonal[row - col] -= 1
        temp_secondary_diagonal[position - col] += 1

        temp_row_to_cols[row].remove(col)
        temp_row_to_cols[position].append(col)
        cnt = 0
        for val in temp_primary_diagonal.values():
            if val <= 1: continue
            cnt += comb(val, 2)
        for val in temp_secondary_diagonal.values():
            if val <= 1: continue
            cnt += comb(val, 2)
        for val in temp_row_to_cols.values():
            if len(val) <= 1: continue
            cnt += comb(len(val), 2)
        return cnt

    res = [[0] * n for _ in range(n)]
    for position in range(n):
        for j in range(n):
            row = col_to_row[j]
            res[position][j] = helper(row, j, position)
    output = ""
    for idx, row in enumerate(res):

        output += ' '.join(str(x) if len(str(x)) > 1 else ' ' + str(x) for x in row)
        if idx != len(res) - 1:
            output += '\n'

    return output


# print(number_of_attacks(parse.read_8queens_search_problem('test_cases/p6/1.prob')))

if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -4
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)
