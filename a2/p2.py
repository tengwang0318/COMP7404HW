import functools
import math
import sys, random, parse
import time, os, copy

SEED = 1


def reflex_play_single_ghost(problem, verbose):
    """
        :param problem: a string which consists seed and the layout
        :return: str, the process of eat bean/ being caught under specified seed.
    """
    # it represents the delta from row and column axes perspective
    ALL_DIRECTIONS = {"E": (0, 1), "N": (-1, 0), "S": (1, 0), "W": (0, -1)}
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1
    OVERLAP = dict()
    WINNER = None
    FOOD_POSITIONS = []

    def generate_result(actions: list[str], subjects: list[str],
                        layouts: list[list[list[str]]], scores: list[int], winner, seed) -> str:
        """

        :param actions: pacman or the ghost's actions or None(means the start status)
        :param subjects: the subject in each turn, or None(means the start status)
        :param layouts: the layout list after taking actions
        :param scores: the score in each turn
        :param winner: the winner of this game
        :return: the final result

        it must check the equality of each list length
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

    @functools.lru_cache(maxsize=1024)
    def get_distance(x1, y1, x2, y2) -> int:
        """
        calculate the manhattan distance from point 1 to point 2
        """
        return abs(x1 - x2) + abs(y1 - y2)
        # return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    @functools.lru_cache(maxsize=1024)
    def evaluate_func(p_r: int, p_c: int, w_r: int, w_c: int, food_r: int, food_c: int) -> int:
        """
        :param p_r: pacman row index
        :param p_c: pacman column index
        :param w_r: ghost row index
        :param w_c: ghost column index
        :param food_r: food row index
        :param food_c: food column index
        :return: the score

        score consists of a penalty and the distance from food.
        if the distance between ghost and pacman is so close, there will be a penalty. otherwise, pacman always finds
        the closest path to the nearest food
        """
        food_distance = get_distance(p_r, p_c, food_r, food_c)
        ghost_distance = get_distance(p_r, p_c, w_r, w_c)
        penalty = 0
        if ghost_distance == 2:
            penalty -= 100
        elif ghost_distance == 1:
            penalty -= 1000
        elif ghost_distance == 0:
            penalty -= 10000
        return -food_distance + penalty

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
        it will use the evaluate_func return values as the score and choose the max score.
        If there are more than one max value, choose one randomly based on their frequency. NOT CHOOSE THE FIRST ONE.
        If some results come up often, it means that they have a high frequencies than other, and it will converge more quickly.
        """

        m, n = len(layout), len(layout[0])

        max_evaluation_score, max_directions = -float('inf'), []

        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = row + delta_x, col + delta_y
            if 0 <= new_x < m and 0 <= new_y < n and layout[new_x][new_y] != "%":
                for f_x, f_y in FOOD_POSITIONS:
                    current_score = evaluate_func(new_x, new_y, w_r, w_c, f_x, f_y)
                    if current_score > max_evaluation_score:
                        max_evaluation_score = current_score
                        max_directions = [direction]
                    elif current_score == max_evaluation_score:
                        max_directions.append(direction)
        return random.choice(max_directions)  # randomly choose
        # return random.choice(list(set(max_directions)))
        # return max_directions[0]

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
    # print(seed)

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
    # random.seed(0)
    test_case_id = int(sys.argv[1])
    problem_id = 2
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:', test_case_id)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        # print(i)
        # start_time = time.time()
        solution, winner = reflex_play_single_ghost(copy.deepcopy(problem), verbose)
        end_time = time.time()
        # print(end_time-start_time)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time:', end - start)
    print('win %', win_p)
