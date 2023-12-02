import functools
import sys, parse, random
import time, os, copy

SEED = 1


def reflex_play_multiple_ghosts(problem, verbose):
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
    ORDER = "WXYZ"
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
                if action is None:
                    action = ""
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

    @functools.lru_cache(maxsize=2 ** 10)
    def get_distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    @functools.lru_cache(maxsize=1024)
    def evaluate_func(p_r, p_c, w_rs, w_cs, food_r, food_c):
        """
        :param p_r: pacman row index
        :param p_c: pacman column index
        :param w_rs: all of ghosts row indices
        :param w_cs: all of ghosts column indices
        :param food_r: food row index
        :param food_c: food column index
        :return: a score

         score consists of a penalty and the distance from food.
        if the distance between ghost and pacman is so close, there will be a penalty. otherwise, pacman always finds
        the closest path to the nearest food
        """
        penalty = 0

        food_distance = get_distance(p_r, p_c, food_r, food_c)
        ghosts_distances = []
        for w_r, w_c in zip(w_rs, w_cs):
            ghosts_distances.append(get_distance(p_r, p_c, w_r, w_c))
        ghosts_distances = [min(ghosts_distances)]
        for ghost_distance in ghosts_distances:
            if ghost_distance == 2:
                penalty -= 100
            elif ghost_distance == 1:
                penalty -= 1000
            elif ghost_distance == 0:
                penalty -= 10000
        return penalty - food_distance

    def get_the_copy(layout: list[list[str]]) -> list[list[str]]:
        """
        instead of using slow deepcopy
        """
        return list(layout)

    def get_ghost_nums(layout: list[list[str]]) -> int:
        seen = set()
        for i in range(len(layout)):
            for j in range(len(layout[0])):
                if layout[i][j] not in seen:
                    seen.add(layout[i][j])
        return len(seen) - 4

    def determine_direction_and_wisely_choose_for_pacman(layout: list[list[str]], row: int, col: int) -> str:
        """
        :param layout: the layout
        :param row: the subject's position
        :param col: the subject's position
        :return: the eligible directions
        """
        nonlocal w_rs, w_cs
        m, n = len(layout), len(layout[0])
        w_rs, w_cs = tuple(w_rs), tuple(w_cs)
        max_evaluation_score, max_directions = -float('inf'), []
        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = row + delta_x, col + delta_y
            if 0 <= new_x < m and 0 <= new_y < n and layout[new_x][new_y] != "%":
                for f_x, f_y in FOOD_POSITIONS:

                    current_score = evaluate_func(new_x, new_y, w_rs, w_cs, f_x, f_y)
                    if current_score > max_evaluation_score:
                        max_evaluation_score = current_score
                        max_directions = [direction]
                    elif current_score == max_evaluation_score:
                        max_directions.append(direction)
        w_rs, w_cs = list(w_rs), list(w_cs)
        return random.choice(max_directions)

    def determine_direction_and_random_choose_for_ghost(layout: list[list[str]], row: int, col: int) -> str:
        """
        :param layout: the layout
        :param row: the subject's position
        :param col: the subject's position
        :return: the eligible directions
        """
        m, n = len(layout), len(layout[0])
        directions = []
        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = row + delta_x, col + delta_y
            if 0 <= new_x < m and 0 <= new_y < n:
                if layout[new_x][new_y] in " P.":
                    directions.append(direction)

        return random.choice(directions) if directions else False

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

    def move_pacman(layout, x, y):
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
            if cnt_food == 0:
                finish = True
                WINNER = "Pacman"
                scores[-1] += PACMAN_WIN_SCORE
        elif layout[x][y] in "WXYZ":
            finish = True
            WINNER = "Ghost"
            if (x, y) in OVERLAP:
                scores.append(scores[-1] + EAT_FOOD_SCORE + PACMAN_MOVING_SCORE + PACMAN_EATEN_SCORE)
            else:
                scores.append(scores[-1] + PACMAN_MOVING_SCORE + PACMAN_EATEN_SCORE)
        layouts.append(layout)
        return finish, x, y, layout

    def move_ghost(layout, x, y):
        nonlocal WINNER
        layout = get_the_copy(layout)
        finish = False
        subject = layout[x][y]
        subjects.append(layout[x][y])
        direction = determine_direction_and_random_choose_for_ghost(layout, x, y)
        if not direction:
            actions.append(None)  # don't have one
            scores.append(scores[-1])
            layouts.append(layout)
            return finish, x, y, layout

        actions.append(direction)

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
            layout[x][y] = subject
        elif layout[x][y] == ".":
            scores.append(scores[-1])
            OVERLAP[(x, y)] = 1
            layout[x][y] = subject
        else:
            layout[x][y] = subject
            finish = True
            WINNER = "Ghost"
            scores.append(scores[-1] + PACMAN_EATEN_SCORE)
        layouts.append(layout)
        return finish, x, y, layout

    seed, layout = parse_problem(problem)
    global SEED
    random.seed(SEED)
    SEED += 1

    number_of_ghost = get_ghost_nums(layout)
    ghosts = ORDER[:number_of_ghost]

    p_r, p_c = get_position("P", layout)
    w_rs, w_cs = [], []

    for i in range(number_of_ghost):
        w_r, w_c = get_position(ghosts[i], layout)
        w_rs.append(w_r)
        w_cs.append(w_c)

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
        for i in range(number_of_ghost):
            finish, w_rs[i], w_cs[i], layout = move_ghost(layout, w_rs[i], w_cs[i])
            layout = get_the_copy(layout)
            if finish:
                break
        if finish:
            break

    solution = generate_result(actions, subjects, layouts, scores, WINNER, seed)
    return solution, WINNER


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
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
        solution, winner = reflex_play_multiple_ghosts(copy.deepcopy(problem), verbose)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
