import sys, random, grader, parse
from parse import num

DIRECTIONS = {'N': ["N", "E", "W"], "E": ["E", "S", "N"], "S": ["S", "W", "E"], "W": ["W", "N", "S"]}
DELTA = {"N": (-1, 0), "E": (0, 1), "W": (0, -1), "S": (1, 0)}


def play_episode(problem: dict) -> str:
    """
    :param problem: a dict which has keys: seed, noise, livingReward, grid, policy
    :return: str
    """
    seed, noise, living_reward, grid, policy = problem['seed'], problem['noise'], \
        problem['livingReward'], problem['grid'], problem['policy']
    random.seed(seed, version=1)
    is_exit = False
    current_row, current_col = find_start_position(grid)
    overlap_row, overlap_col = current_row, current_col
    overlap_item = "S"

    grid[current_row][current_col] = "P"
    experience = 'Start state:\n' + print_grid(grid) + "Cumulative reward sum: 0.0\n"
    m, n = len(grid), len(grid[0])
    cumulative_reward = 0

    while not is_exit:
        current_experience = "-------------------------------------------- \n"
        action = policy[current_row][current_col]
        # if the current action is exit, then just update some info and exit.
        if action == "exit":
            reward = num(overlap_item)
            grid[overlap_row][overlap_col] = overlap_item
            cumulative_reward += num(reward)
            direction = 'exit'
            is_exit = True
        # if the current action is not exit, choose the intended direction based on the policy and go to the real
        # direction based on the probability.
        else:
            feasible_directions = DIRECTIONS[action]
            direction = random.choices(population=feasible_directions, weights=[1 - 2 * noise, noise, noise])[0]
            temp_row, temp_col = current_row + DELTA[direction][0], current_col + DELTA[direction][1]
            # if the real direction is feasible, just do it and update some info. Otherwise, keep the previous position.
            if check_direction_feasibility(m, n, temp_row, temp_col, grid):
                current_row, current_col = temp_row, temp_col
                grid[overlap_row][overlap_col] = overlap_item
                overlap_item = grid[current_row][current_col]
                overlap_row, overlap_col = current_row, current_col
            grid[current_row][current_col] = "P"
            reward = living_reward
            cumulative_reward += living_reward
        cumulative_reward = round(cumulative_reward, 3)
        current_experience += "Taking action: {} (intended: {})\n" \
                              "Reward received: {}\n" \
                              "New state:\n" \
                              "{}" \
                              "Cumulative reward sum: {}\n".format(
            direction, action, reward, print_grid(grid), cumulative_reward)
        experience += current_experience
    return experience[:-1]


def find_start_position(grid: list[list[str]]) -> tuple[int, int]:
    """
    return the position of start item
    :param grid: list[list[str]], the grid of the board
    :return: tuple[int, int], the start position.
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "S":
                return i, j


def check_direction_feasibility(m:int, n:int, row:int, col:int, grid:list[list[int]])->bool:
    """
    check the feasibility of the new position
    :param m: int, the height of board.
    :param n: int, the weight of board.
    :param row: int, the current row position.
    :param col: int, the current col position.
    :param grid: list[list[int]], the game board.
    :return: boolean, the feasibility of new position
    """
    if row < 0 or row >= m or col < 0 or col >= n:
        return False
    if grid[row][col] == "#": return False
    return True


def print_grid(grid:list[list[str]])->str:
    """
    print the str
    :param grid: list[list[str]]
    :return: str
    """
    grid_str = ""
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(grid[row_idx]):
            grid_str += " " * (5 - len(str(value))) + str(value)
        grid_str += '\n'
    return grid_str


if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -8
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)
