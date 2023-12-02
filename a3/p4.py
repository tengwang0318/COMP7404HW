import sys, grader, parse
import random
from p1 import DELTA, DIRECTIONS, check_direction_feasibility
from parse import num

DIRECTION_TO_IDX = {"N": 0, "E": 1, "S": 2, "W": 3}
IDX_TO_DIRECTION = {0: "N", 1: "E", 2: "S", 3: "W"}

ALPHA = 0.001
EPSILON = 2
SEED = 64
MAX_ITERATIONS = 100000


class Agent:
    def __init__(self, discount, noise, living_reward, grid, alpha):
        self.discount = discount
        self.noise = noise
        self.living_reward = living_reward
        self.grid = grid
        self.m, self.n = len(self.grid), len(self.grid[0])
        self.q_values = [[[0] * 4 for _ in range(self.n)] for _ in range(self.m)]
        self.start_state_row, self.start_state_col = self.find_start_state()
        self.alpha = alpha
        self.current_iteration = 0
        self.max_iterations = MAX_ITERATIONS

    def find_start_state(self):
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] == "S":
                    return i, j

    def find_max_direction(self, row, col):
        max_idx = self.q_values[row][col].index(max(self.q_values[row][col]))
        return IDX_TO_DIRECTION[max_idx]

    def epsilon_greedy_with_decay(self, row, col):
        """
        At the beginning of iterations, every sample have much higher probabilities to go randomly.
        After processing many samples, the sample try to find the direction regarding the max q value.
        :param row:
        :param col:
        :return:
        """
        if random.random() < EPSILON * (1 - self.current_iteration ** 1 / self.max_iterations ** 1):
            return random.choices(population="NWES")[0]
        else:
            return self.find_max_direction(row, col)

    def run_an_iteration(self):
        is_exit = False
        current_row, current_col = self.start_state_row, self.start_state_col
        while not is_exit:
            previous_row, previous_col = current_row, current_col

            if self.grid[previous_row][previous_col] not in "S_#":
                sample = self.living_reward + num(self.grid[previous_row][previous_col])
                for k in range(4):
                    self.q_values[previous_row][previous_col][k] = self.alpha * sample + (1 - self.alpha) * \
                                                                   self.q_values[previous_row][previous_col][k]
                    is_exit = True
                continue

            intended_direction = self.epsilon_greedy_with_decay(previous_row, previous_col)
            direction = random.choices(population=DIRECTIONS[intended_direction],
                                       weights=[1 - 2 * self.noise, self.noise, self.noise])[0]
            current_row, current_col = previous_row + DELTA[direction][0], previous_col + DELTA[direction][1]
            if not check_direction_feasibility(self.m, self.n, current_row, current_col, self.grid):
                current_row, current_col = previous_row, previous_col
            sample = self.living_reward + self.discount * max(self.q_values[current_row][current_col])
            self.q_values[previous_row][previous_col][DIRECTION_TO_IDX[intended_direction]] = \
                self.alpha * sample + (1 - self.alpha) * self.q_values[previous_row][previous_col][
                    DIRECTION_TO_IDX[intended_direction]]

    def run_all_iterations(self):
        while self.current_iteration < self.max_iterations:
            self.run_an_iteration()
            self.current_iteration += 1

    def generate_the_policy(self):
        res = ""
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] == "#":
                    res += "| # |"
                elif self.grid[i][j] not in "S#_":
                    res += "| x |"
                else:
                    max_ = self.q_values[i][j].index(max(self.q_values[i][j]))
                    res += "| {} |".format(IDX_TO_DIRECTION[max_])

            res += "\n"
        return res[:-1]

    def show_convergence_situation(self):
        res = ""

        for i in range(self.m):
            row_res = ""
            for j in range(self.n):
                if self.grid[i][j] == "#":
                    row_res += "|{:^8}|".format("#####")
                elif self.grid[i][j] not in "S#_":
                    row_res += "|{:^8}|".format(round(self.q_values[i][j][0], 3))
                else:
                    for k in range(4):
                        direction = IDX_TO_DIRECTION[k]
                        value = round(self.q_values[i][j][k], 3)
                        cell_content = "{} {}".format(direction, value)
                        row_res += "|{:^8}|".format(cell_content)
            row_res += '\n'
            res += row_res
        print(res)


def td_learning(problem):
    random.seed(SEED)
    agent = Agent(problem['discount'], problem['noise'], problem['livingReward'], problem['grid'], alpha=ALPHA)
    agent.run_all_iterations()
    # agent.show_convergence_situation()
    return agent.generate_the_policy()


if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -4
    problem_id = 4
    grader.grade(problem_id, test_case_id, td_learning, parse.read_grid_mdp_problem_p4)
