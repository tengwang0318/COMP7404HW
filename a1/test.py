import time
from random import randrange


def all_solutions():
    """
    Attention!!!
    Thanks for your valuable time. Please read the following comments.

    this solution won't use anything from p6 and p7. I think functions and data structure in p6 and p7 are not flexible and inefficient for me to handle it.
    I try to do it three times(You could check the git log.), but it failed. So I think the best way for me to solve is refactor it.
    What's more, at bottom of this file I wrote a dfs version of solve 8 queues, whose name is `dfs_all_solution()`.
    """
    n = 8

    def initialization():
        """
        The reason why I would use indices of row, instead of column is that I won't write lots of loop firstly row codes which wasts the time.
        The reason why I won't use p6 and p7 representations is that 1D is good enough to express the graph clearly and improve the efficiency of program.
        :return: 1D list which stores the indices of queue along row
        """
        return [randrange(0, n) for _ in range(n)]

    def counter_number_of_attack(state: list[int], cache):
        """
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

        # Store the result in cache
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

    def find_all_best_neighbors(neighbors: list[list[int]], cache):
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
        while True:
            current_attack_cnt = counter_number_of_attack(state, cache)
            neighbors = find_all_neighbors(state, )
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

    # def hill_climbing_v2(state: list[int], random=False):
    #     count_plateau = 0
    #     while True:
    #         current_attack_cnt = counter_number_of_attack(state)
    #         neighbors = find_all_neighbors(state)
    #         best_neighbors, min_attack_cnt = find_all_best_neighbors(neighbors)
    #
    #         if random:
    #             new_state = best_neighbors[randrange(0, len(best_neighbors))]
    #         else:
    #             new_state = best_neighbors[0]
    #         if current_attack_cnt == 0:
    #             return state
    #         elif min_attack_cnt == current_attack_cnt:
    #             count_plateau += 1
    #             print(min_attack_cnt, current_attack_cnt)
    #             print(count_plateau)
    #             if count_plateau > 1:
    #                 return False
    #         elif min_attack_cnt >= current_attack_cnt > 0:
    #             return False
    #         else:
    #             count_plateau = 0
    #         state = new_state

    def hill_climbing_v2_3(state: list[int], cache, MAX_PLATEAU=3, EARLY_EXIT=True, HIGH_VALUE=12):
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
    res = sorted(res)
    solutions = []
    for i, item in enumerate(res):
        state = []
        # print(item)
        for idx, q_col in enumerate(item):
            temp = "." * q_col + "q" + "." * (n - q_col - 1)
            temp = " ".join(temp)
            state.append(temp)
        # print(state)
        state = "\n".join(state)
        state = "Solution: {}\n".format(i) + state
        solutions.append(state)
    solutions = "".join(solutions)
    solutions += "Num solutions found: {}".format(len(res))
    return solutions


all_solutions()
