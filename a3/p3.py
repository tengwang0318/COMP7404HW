import sys, grader, parse
from p1 import DELTA, DIRECTIONS
from parse import num
from p1 import check_direction_feasibility


def value_iteration(problem):
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']

    current_idx = 0
    m, n = len(grid), len(grid[0])
    current_value_pi = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "#":
                current_value_pi[i][j] = "#"
    return_value = show_value_pi(current_value_pi, current_idx, m, n)
    current_idx += 1
    while current_idx < iterations:
        previous_value_pi = current_value_pi
        current_value_pi = [[0] * n for _ in range(m)]
        policy = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if not check_direction_feasibility(m, n, i, j, grid):
                    current_value_pi[i][j] = "#"
                    policy[i][j] = "#"
                elif grid[i][j] not in "#_S":
                    current_value_pi[i][j] = num(grid[i][j])
                    policy[i][j] = "x"
                else:
                    max_ = -float('inf')
                    max_direction = None
                    for intended_action in "NEWS":
                        actual_action = DIRECTIONS[intended_action]
                        probabilities = [1 - 2 * noise, noise, noise]
                        v = 0
                        for probability, action in zip(probabilities, actual_action):
                            new_i, new_j = DELTA[action][0] + i, DELTA[action][1] + j
                            if check_direction_feasibility(m, n, new_i, new_j, grid):
                                v += probability * (living_reward + discount * previous_value_pi[new_i][new_j])
                            else:
                                v += probability * (living_reward + discount * previous_value_pi[i][j])
                        if max_ < v:
                            max_ = v
                            max_direction = intended_action
                    policy[i][j] = max_direction
                    current_value_pi[i][j] = max_
        return_value += generate_result(current_value_pi, policy, current_idx, m, n)
        current_idx += 1
    return return_value[:-1]


def show_value_pi(value_pi: float, k: int, m: int, n: int) -> str:
    """
    get the value pi string
    :param value_pi: float 
    :param k: int
    :param m: int
    :param n: int
    :return: str
    """
    res = "V_k={}\n".format(k)
    for i in range(m):
        temp_res = ""
        for j in range(n):
            if type(value_pi[i][j]) is not str:
                temp_res += '|{:7.2f}|'.format(value_pi[i][j])
            else:
                temp_res += "| ##### |"
        temp_res += "\n"
        res += temp_res
    return res


def generate_result(value_pi: float, policy: str, k: int, m: int, n: int) -> str:
    """
    get the policy for every point in specified iteration.
    :param value_pi: float
    :param policy: str
    :param k: int
    :param m: int
    :param n:int
    :return:
    """
    res = show_value_pi(value_pi, k, m, n)
    if k != 0:
        res += "pi_k={}\n".format(k)
        for i in range(m):
            temp_res = ""
            for j in range(n):
                temp_res += '| {} |'.format(policy[i][j])
            temp_res += '\n'
            res += temp_res
    return res


if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)
