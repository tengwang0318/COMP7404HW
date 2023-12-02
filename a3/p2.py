import sys, grader, parse
from p1 import DELTA, DIRECTIONS, check_direction_feasibility
from parse import num


def policy_evaluation(problem: dict):
    """
    :param problem: a dict which has keys (discount, noise, livingReward, grid, iterations, policy)
    :return:
    """
    discount = problem['discount']
    noise = problem['noise']
    living_reward = problem['livingReward']
    grid = problem['grid']
    iterations = problem['iterations']
    policy = problem['policy']
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
        for i in range(m):
            for j in range(n):
                if not check_direction_feasibility(m, n, i, j, grid):
                    current_value_pi[i][j] = "#"
                elif policy[i][j] == "exit":
                    current_value_pi[i][j] = num(grid[i][j])
                else:
                    intended_action = policy[i][j]
                    actual_action = DIRECTIONS[intended_action]
                    probabilities = [1 - 2 * noise, noise, noise]
                    v = 0
                    for probability, action in zip(probabilities, actual_action):
                        new_i, new_j = DELTA[action][0] + i, DELTA[action][1] + j
                        if check_direction_feasibility(m, n, new_i, new_j, grid):
                            v += probability * (living_reward + discount * previous_value_pi[new_i][new_j])
                        else:
                            v += probability * (living_reward + discount * previous_value_pi[i][j])
                    current_value_pi[i][j] = v
        return_value += show_value_pi(current_value_pi, current_idx, m, n)
        current_idx += 1

    return return_value[:-1]


def show_value_pi(value_pi, k, m, n):
    res = "V^pi_k={}\n".format(k)
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


if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)
