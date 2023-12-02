import sys, parse, grader, copy, p6
from math import comb
from copy import deepcopy
from collections import defaultdict


def better_board(problem:list[list[str]]):
    """
        this function doesn't perform well due to inflexibility of the data structure in the problem.
        In problem 8, I also refactor it and name it as find_all_neighbors

        use hash-table to accelerate the find-up procedure.
        create four tables:
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

    # print(primary_diagonal)
    # print(secondary_diagonal)
    min_r, min_c, min_val = -1, -1, float('inf')

    def helper(row, col, position):
        nonlocal min_val, min_c, min_r

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
        if cnt < min_val:
            min_c = col
            min_r = position
            min_val = cnt
        return cnt

    res = [[0] * n for _ in range(n)]
    for position in range(n):
        for j in range(n):
            row = col_to_row[j]
            res[position][j] = helper(row, j, position)
    problem[col_to_row[min_c]][min_c] = "."
    problem[min_r][min_c] = "q"

    res = ""
    for idx, temp in enumerate(problem):
        res += " ".join(temp)
        if idx != n - 1:
            res += "\n"

    return res


# print(better_board(parse.read_8queens_search_problem("test_cases/p7/1.prob")))

if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -6
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)
