import functools
import sys, parse
import time, os, copy
import random

SEED = 1

expectimax_cache = {}
@functools.lru_cache(2 ** 12)
def get_distance(x1, y1, x2, y2) -> int:
    """
    calculate the manhattan distance from point 1 to point 2
    """
    return abs(x1 - x2) + abs(y1 - y2)


def expectimax_single_ghost(problem, k, verbose):
    # it represents the delta from row and column axes perspective
    ALL_DIRECTIONS = {"E": (0, 1), "N": (-1, 0), "S": (1, 0), "W": (0, -1)}
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    OVERLAP = dict()
    WINNER = None
    FOOD_POSITIONS = []
    # it is used for caching the expectimax function parameter

    k = k * 2 - 1

    def generate_result(actions: list[str], subjects: list[str],
                        layouts: list[list[list[str]]], scores: list[int], winner, seed) -> str:
        """
        :param actions: pacman or the ghost's actions or None(means the start status)
        :param subjects: the subject in each turn, or None(means the start status)
        :param layouts: the layout list after taking actions
        :param scores: the score in each turn
        :param winner: the winner of this game
        :return: the final result

        """
        # check the equality of each list's length
        assert len(actions) == len(subjects) == len(layouts)

        res = ""
        is_first = True
        for idx, (action, subject, layout, score) in enumerate(zip(actions, subjects, layouts, scores)):
            if is_first:
                new_one = "seed: {}\n0\n".format(seed)
            else:
                new_one = "{}: {} moving {}\n".format(idx, subject, action)
            for i in range(len(layout)):
                new_one += "".join(layout[i]) + "\n"

            if is_first:
                is_first = False
            else:
                new_one += "score: {}\n".format(score)
            res += new_one
        res += "WIN: {}".format(winner)
        return res

    def parse_problem(problem: str) -> (int, list[list[str]]):
        """
        parse the string of problem to get the seed and list regarding layout of maze
        :param problem: the original problem string
        :return: the seed and list of layout
        """
        items = problem.split("\n")
        seed = items[0].split()[-1]
        layout = [list(item) for item in items[1:]]
        return seed, layout

    def expectimax(level, p_r, p_c, w_r, w_c, food_r, food_c) -> int:
        """
        :param level: the current height of expectimax
        :param p_r: the pacman's row index
        :param p_c: the pacman's column index
        :param w_r: the ghost's row index
        :param w_c: the pacman's column index
        :param food_r: the food's row index
        :param food_c: the food's column index
        :return: a score
        """
        cache_key = (level, p_r, p_c, w_r, w_c, food_r, food_c)
        if cache_key in expectimax_cache:
            return expectimax_cache[cache_key]

        # the ghost meets pacman
        if get_distance(p_r, p_c, w_r, w_c) == 0:
            utility = -2000
            expectimax_cache[cache_key] = utility
            return utility
        # get the expectimax leaves
        if level == 0:
            utility = -get_distance(p_r, p_c, food_r, food_c)
            expectimax_cache[cache_key] = utility
            return utility
        if level % 2 == 1:  # Maximizer Node (Pacman's turn)
            max_utility = -float('inf')
            for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
                new_x, new_y = p_r + delta_x, p_c + delta_y
                if is_valid_move(new_x, new_y):
                    penalty = 0
                    distance_p_w = get_distance(new_x, new_y, w_r, w_c)
                    if distance_p_w == 2:
                        penalty = -20
                    elif distance_p_w == 1:
                        penalty = -200
                    elif distance_p_w == 0:
                        penalty = -2000
                    utility = expectimax(level - 1, new_x, new_y, w_r, w_c, food_r, food_c) + penalty
                    max_utility = max(max_utility, utility)
            expectimax_cache[cache_key] = max_utility
            return max_utility
        else:  # Chance Node (Ghost's turn)
            total_utility = 0
            num_moves = 0
            for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
                new_x, new_y = w_r + delta_x, w_c + delta_y
                if is_valid_move(new_x, new_y):
                    utility = expectimax(level - 1, p_r, p_c, new_x, new_y, food_r, food_c)
                    total_utility += utility
                    num_moves += 1
            utility = total_utility / num_moves if num_moves > 0 else 0
            expectimax_cache[cache_key] = utility
            return utility

    def is_valid_move(x, y):
        return 0 <= x < len(layout) and 0 <= y < len(layout[0]) and layout[x][y] != "%"

    def get_the_copy(layout: list[list[str]]) -> list[list[str]]:
        """
        instead of using slow deepcopy
        """
        return list(layout)

    def determine_direction_and_random_choose(layout: list[list[str]], row: int, col: int) -> str:
        """
        :param layout: the layout
        :param row: the subject's position
        :param col: the subject's position
        :return: the eligible directions

        choose the direction of the ghost randomly
        """

        m, n = len(layout), len(layout[0])
        directions = []
        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = row + delta_x, col + delta_y
            if 0 <= new_x < m and 0 <= new_y < n and layout[new_x][new_y] != "%":
                directions.append(direction)
        return random.choice(directions)

    def determine_direction_and_wisely_choose_for_pacman(layout: list[list[str]], row: int, col: int) -> str:
        """
        :param layout: the layout
        :param row: the subject's position
        :param col: the subject's position
        :return: the eligible directions

        choose the direction of the pacman wisely based on the evaluation function score.
        """

        m, n = len(layout), len(layout[0])

        max_evaluation_score, max_directions = -float('inf'), []

        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = row + delta_x, col + delta_y
            if 0 <= new_x < m and 0 <= new_y < n and layout[new_x][new_y] != "%":
                for f_x, f_y in FOOD_POSITIONS:
                    current_score = expectimax(k - 1, new_x, new_y, w_r, w_c, f_x, f_y)
                    if current_score > max_evaluation_score:
                        max_evaluation_score = current_score
                        max_directions = [direction]
                    elif current_score == max_evaluation_score:
                        max_directions.append(direction)
        return random.choice(max_directions)

    def get_position(item: str, layout: list[list[str]]) -> (int, int):
        """
        get the position of item
        """
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if layout[i][j] == item:
                    return i, j

    def count_food(layout: list[list[str]]) -> int:
        """
        count the number of food
        """
        cnt = 0
        for i in range(len(layout)):
            for j in range(len(layout[0])):
                if layout[i][j] == ".":
                    FOOD_POSITIONS.append((i, j))
                    cnt += 1
        return cnt

    def move_pacman(layout: list[list[str]], x: int, y: int) -> (bool, int, int, list[list[str]]):
        """
        :param layout: the layout of game-board.
        :param x: the row position of pacman
        :param y: the column position of pacman
        :return: (
            bool: the game is finished or not;
            int: new_x;
            int: new_y;
            layout: list[list[str]]
        )
        find a direction to move pacman.

                """
        nonlocal WINNER
        finish = False
        subjects.append("P")
        direction = determine_direction_and_wisely_choose_for_pacman(layout, x, y)

        actions.append(direction)
        delta_x, delta_y = ALL_DIRECTIONS[direction]
        layout = get_the_copy(layout)
        layout[x][y] = " "

        x += delta_x
        y += delta_y
        if layout[x][y] == " ":
            scores.append(scores[-1] + PACMAN_MOVING_SCORE)
            layout[x][y] = "P"

        elif layout[x][y] == ".":
            scores.append(scores[-1] + EAT_FOOD_SCORE + PACMAN_MOVING_SCORE)
            layout[x][y] = "P"
            nonlocal cnt_food
            cnt_food -= 1
            FOOD_POSITIONS.remove((x, y))
            # make sure that is it finished or not
            if cnt_food == 0:
                finish = True
                WINNER = "Pacman"
                scores[-1] += PACMAN_WIN_SCORE
        elif layout[x][y] == "W":
            finish = True
            WINNER = "Ghost"
            # make sure the overlap situation of FOOD and ghost
            if (x, y) in OVERLAP:
                scores.append(scores[-1] + EAT_FOOD_SCORE + PACMAN_MOVING_SCORE + PACMAN_EATEN_SCORE)
            else:
                scores.append(scores[-1] + PACMAN_MOVING_SCORE + PACMAN_EATEN_SCORE)
        layouts.append(layout)
        return finish, x, y, layout

    def move_ghost(layout, x, y):
        """
         :param layout: the layout of game-board.
         :param x: the row position of pacman
         :param y: the column position of pacman
         :return: (
                 bool: the game is finished or not;
                 int: new_x;
                 int: new_y;
                 layout: list[list[str]]
             )
        find a direction to move pacman.
                   """
        nonlocal WINNER
        finish = False
        subjects.append("W")
        direction = determine_direction_and_random_choose(layout, x, y)
        actions.append(direction)
        layout = get_the_copy(layout)
        if (x, y) in OVERLAP:
            layout[x][y] = "."
            OVERLAP.pop((x, y))
        else:
            layout[x][y] = " "

        delta_x, delta_y = ALL_DIRECTIONS[direction]
        x += delta_x
        y += delta_y
        if layout[x][y] == " ":
            scores.append(scores[-1])
            layout[x][y] = "W"
        elif layout[x][y] == ".":
            scores.append(scores[-1])
            OVERLAP[(x, y)] = 1
            layout[x][y] = "W"
        else:
            layout[x][y] = "W"
            finish = True
            WINNER = "Ghost"
            scores.append(scores[-1] + PACMAN_EATEN_SCORE)
        layouts.append(layout)
        return finish, x, y, layout

    seed, layout = parse_problem(problem)
    global SEED
    random.seed(SEED)
    SEED += 1
    p_r, p_c = get_position("P", layout)
    w_r, w_c = get_position("W", layout)
    cnt_food = count_food(layout)

    subjects = [None]
    actions = [None]
    layouts = [layout]
    scores = [0]

    while True:
        layout = get_the_copy(layout)
        finish, p_r, p_c, layout = move_pacman(layout, p_r, p_c)
        layout = get_the_copy(layout)
        if finish:
            break
        finish, w_r, w_c, layout = move_ghost(layout, w_r, w_c)
        if finish:
            break

    solution = generate_result(actions, subjects, layouts, scores, WINNER, seed)

    return solution, WINNER


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:', test_case_id)
    print('k:', k)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expectimax_single_ghost(copy.deepcopy(problem), k, verbose)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
