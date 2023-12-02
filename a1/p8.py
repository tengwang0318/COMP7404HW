import sys, parse, grader, copy
import p7, p6
from random import randrange
from copy import deepcopy
from pprint import pprint
import time


def all_solutions():
    """
    Attention!!!
    Thanks for your valuable time. Please read the following comments.

    this solution won't use anything from p6 and p7. I think functions and data structure in p6 and p7 are not flexible and inefficient for me to handle it.
    I try to do it three times(You could check the git log.), but it failed. So I think the best way for me to solve is refactor it.

    I finish 5 version of methods:
        1. try normal local search without any optimization.
        2. local search + random choose the node which has the same min cost.
        3. utilize the cache/memory to memorize the number of attack.
        4. give the algorithm some chance to get out of the plateau (count the number of the consecutive plateau)
        5. early exit mechanism: set a high value, if the number of attack is greater than that, just exit and reinitialize it.

    Due to the inflexibility of the function interface you give, I couldn't add any parameters in the signature of all_solutions().
    Just change the following 5 versions of local search inside all_solutions() if you want to check :)
    The version of all_solutions() is using (MAX_PLATEAU=50, EARLY_EXIT=True, HIGH_VALUE=20, Cache={}, random_choose_min_nodes)


    What's more, at bottom of this file I wrote a dfs version of solve 8 queues, whose name is `dfs_all_solution()`.
    DFS version is much faster than any version local search I wrote.
    """
    n = 8

    def initialization():
        """
        The reason why I would use indices of row, instead of column is that it helps me to generate the result without lots of boring operates.
        The reason why I won't use p6 and p7 representations is that 1D is good enough to express the graph clearly and improve the efficiency of program.
        :return: 1D list which stores the indices of queue along row
        """
        return [randrange(0, n) for _ in range(n)]

    def counter_number_of_attack(state: list[int], cache):
        """
        cache: use memory mechanism to avoid lots of repeated calculations.

        all conditions that causes attack could be generalized in two ways:
        1. they are in the different rows but have the same column. state[i] == state[j]
        2. they are in the different rows and columns but in the primary or secondary diagonal line.
           state[i]-state[j]= i-j or state[i]-state[j]=j-i
           =>
           abs(state[i]-state[j])=abs(i-j)
        loop_cnts = n choose 2
        :return:
        """
        state_tuple = tuple(state)

        if state_tuple in cache:
            return cache[state_tuple]

        attack_cnt = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(state[i] - state[j]) == j - i or state[i] == state[j]:
                    attack_cnt += 1

        cache[state_tuple] = attack_cnt
        return attack_cnt

    def find_all_neighbors(state: list[int]):
        """
        loop every row to find which column could change.
        :param state:
        :return:
        """
        neighbors = []
        for old_row_idx in range(n):
            for new_column_value in range(n):
                if state[old_row_idx] != new_column_value:
                    new_state = state[:]
                    new_state[old_row_idx] = new_column_value
                    neighbors.append(new_state)
        return neighbors

    def find_all_best_neighbors(neighbors: list[list[int]], cache: dict):
        """
        min_neighbors is a list! Just try to help get out of the plateau situation.
        """
        min_attack_cnt = float('inf')
        min_neighbors = []
        for neighbor in neighbors:
            current_attack_number = counter_number_of_attack(neighbor, cache)
            if min_attack_cnt > current_attack_number:
                min_neighbors = [neighbor]
                min_attack_cnt = current_attack_number
            elif min_attack_cnt == current_attack_number:
                min_neighbors.append(neighbor)
        return min_neighbors, min_attack_cnt

    def hill_climbing_v0_1(state: list[int], cache, random=False):
        """
        1. try normal local search without any optimization.
        2. local search + random choose the node which has the same min cost.
        3. utilize the cache/memory to memorize the number of attack.


        """
        while True:
            current_attack_cnt = counter_number_of_attack(state, cache)
            neighbors = find_all_neighbors(state)
            best_neighbors, min_attack_cnt = find_all_best_neighbors(neighbors, cache)
            if random:
                new_state = best_neighbors[randrange(0, len(best_neighbors))]
            else:
                new_state = best_neighbors[0]
            if current_attack_cnt == 0:
                return state
            elif min_attack_cnt >= current_attack_cnt > 0:
                return False

            state = new_state

    def runner_v0_1(random=False):
        res = set()
        cache = {}
        start_time = time.time()
        while len(res) != 92:
            state = initialization()
            solution = hill_climbing_v0_1(state, cache, random)
            if solution is False:
                continue
            else:
                res.add(tuple(solution))
        end_time = time.time()
        print(f"running:{end_time - start_time}")
        return res

    # runner_v0_1(True)

    def hill_climbing_v2_3(state: list[int], cache, MAX_PLATEAU=3, EARLY_EXIT=True, HIGH_VALUE=12):
        """
        4. give the algorithm some chance to get out of the plateau (count the number of the consecutive plateau)
        5. early exit mechanism: set a high value, if the number of attack is greater than that, just exit and reinitialize it.
        """
        count_plateau = 0
        while True:
            current_attack_cnt = counter_number_of_attack(state, cache)
            neighbors = find_all_neighbors(state)
            best_neighbors, min_attack_cnt = find_all_best_neighbors(neighbors, cache)
            if EARLY_EXIT and current_attack_cnt > HIGH_VALUE:
                return False
            if current_attack_cnt == 0:
                return state

            if min_attack_cnt < current_attack_cnt:
                count_plateau = 0
            elif min_attack_cnt == current_attack_cnt:
                count_plateau += 1
                if count_plateau > MAX_PLATEAU:
                    return False

            state = best_neighbors[randrange(0, len(best_neighbors))]

    def runner_v2_3(MAX_PLATEAU, EARLY_EXIT, HIGH_VALUE=10):
        res = set()
        cache = {}
        start_time = time.time()
        while len(res) != 92:
            state = initialization()
            if EARLY_EXIT:
                solution = hill_climbing_v2_3(state, cache, MAX_PLATEAU, EARLY_EXIT, HIGH_VALUE)
            else:
                solution = hill_climbing_v2_3(state, cache, MAX_PLATEAU, EARLY_EXIT)
            if solution is False:
                continue
            else:
                res.add(tuple(solution))
            # print(len(res))
        end_time = time.time()
        print(f"running:{end_time - start_time}")
        return res

    #
    # runner_v2_3(MAX_PLATEAU=50, EARLY_EXIT=True, HIGH_VALUE=12)
    #
    # runner_v2_3(MAX_PLATEAU=50, EARLY_EXIT=True, HIGH_VALUE=20)
    # runner_v2_3(MAX_PLATEAU=3, EARLY_EXIT=True, HIGH_VALUE=12)
    # runner_v2_3(MAX_PLATEAU=3, EARLY_EXIT=True, HIGH_VALUE=20)
    # for _ in range(10):
    #     runner_v2_3(MAX_PLATEAU=100,EARLY_EXIT=True,HIGH_VALUE=15)
    #
    # runner_v2_3(MAX_PLATEAU=15, EARLY_EXIT=False)
    # runner_v2_3(MAX_PLATEAU=3, EARLY_EXIT=False)
    res = runner_v2_3(MAX_PLATEAU=50, EARLY_EXIT=True, HIGH_VALUE=15)
    solutions = []
    for i, item in enumerate(res):
        state = []
        for idx, q_col in enumerate(item):
            temp = "." * q_col + "q" + "." * (n - q_col - 1)
            temp = " ".join(temp)
            state.append(temp)
        state = "\n".join(state)
        solutions.append(state)
    solutions = sorted(solutions)
    res = []
    for i, state in enumerate(solutions):
        state = "Solution: {}\n".format(i) + state
        res.append(state)
    res = "\n\n".join(res)
    res += "\n\nNum solutions found: {}".format(len(solutions))
    return res


#
def dfs_all_solution():
    res = []

    n = 8
    # fixed the column and change and track the rows
    rows = [1] * n

    # check which row has been visited
    seen = [False] * n
    # 0 + 0 -> n-1+n-1, number is 2*n-1. The same for secondary_diagonal
    primary_diagonal = [False] * (2 * n - 1)
    secondary_diagonal = [False] * (2 * n - 1)

    def dfs(column):
        """
        fixed column, then move the row
        :return:
        """
        if column == n:
            temp = ""
            for i in range(n):
                idx = rows.index(i)
                # temp+="Solution: {}".format(i)
                temp += " ".join("." * idx + "q" + "." * (n - idx - 1))
                temp += "\n"
            # print(temp)
            res.append(temp)
        for row in range(n):
            if not seen[row] and not primary_diagonal[row + column] and not secondary_diagonal[row - column]:
                primary_diagonal[row + column] = True
                secondary_diagonal[row - column] = True
                seen[row] = True

                rows[column] = row

                dfs(column + 1)
                secondary_diagonal[row - column] = False
                primary_diagonal[row + column] = False
                seen[row] = False

    dfs(0)
    # print(res)
    res = sorted(res)
    number_of_found = len(res)
    # print(res)
    final_res = ""
    for i, item in enumerate(res):
        final_res += "Solution: {}\n".format(i)
        final_res += item
        final_res += "\n"
    final_res += 'Num solutions found: {}'.format(number_of_found)
    # print(final_res)
    return final_res


if __name__ == "__main__":
    test_case_id = 1  # there is just one testcase for p8
    problem_id = 8
    grader.grade(problem_id, test_case_id, all_solutions, None)
