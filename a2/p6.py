import sys, parse
import time, os, copy, random, functools

SEED = 1


@functools.lru_cache(2 ** 12)
def get_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def expectimax_multiple_ghost(problem, k, verbose):
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
    FOOD_POSITIONS = []
    expectimax_cache = {}

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

    def is_valid_move(x, y):
        return 0 <= x < len(layout) and 0 <= y < len(layout[0]) and layout[x][y] != "%"

    def expectimax(level, p_r, p_c, w_rs, w_cs, food_r, food_c):
        cache_key = (level, p_r, p_c, tuple(w_rs), tuple(w_cs), food_r, food_c)
        if cache_key in expectimax_cache:
            return expectimax_cache[cache_key]
        # Calculate average distance from all ghosts
        avg_ghost_distance = sum([get_distance(p_r, p_c, w_r, w_c) for w_r, w_c in zip(w_rs, w_cs)]) / len(w_rs)

        # If any ghost meets Pacman
        if any([get_distance(p_r, p_c, w_r, w_c) == 0 for w_r, w_c in zip(w_rs, w_cs)]):
            utility = -2000
            expectimax_cache[cache_key] = utility - avg_ghost_distance
            return utility

        if level == 0:
            utility = -get_distance(p_r, p_c, food_r, food_c)
            expectimax_cache[cache_key] = utility
            return utility

        # pacman's move
        if level % (number_of_ghost + 1) == 0:
            max_utility = -float('inf')
            for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
                new_x, new_y = p_r + delta_x, p_c + delta_y
                if is_valid_move(new_x, new_y):
                    min_ = min([get_distance(new_x, new_y, w_r, w_c) for w_r, w_c in zip(w_rs, w_cs)])
                    penalty = 0
                    if min_ <= 2:
                        penalty -= 20
                    # if min_ == 2:
                    #     penalty = -10
                    # elif min_ == 1:
                    #     penalty = -100
                    # elif min_ == 0:
                    #     penalty = -2000

                    utility = expectimax(level - 1, new_x, new_y, w_rs[:], w_cs[:], food_r, food_c) + penalty
                    max_utility = max(max_utility, utility)
            expectimax_cache[cache_key] = max_utility
            return max_utility

        else:  # ghosts' moves
            ghost_idx = (level % (number_of_ghost + 1)) - 1
            w_r, w_c = w_rs[ghost_idx], w_cs[ghost_idx]

            total_utility = 0
            num_moves = 0
            for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
                new_x, new_y = w_r + delta_x, w_c + delta_y
                if is_valid_move(new_x, new_y):
                    new_w_rs = w_rs[:ghost_idx] + [new_x] + w_rs[ghost_idx + 1:]
                    new_w_cs = w_cs[:ghost_idx] + [new_y] + w_cs[ghost_idx + 1:]
                    utility = expectimax(level - 1, p_r, p_c, new_w_rs, new_w_cs, food_r, food_c)
                    total_utility += utility
                    num_moves += 1

            utility = total_utility / num_moves if num_moves > 0 else 0
            expectimax_cache[cache_key] = utility
            return utility

    def get_the_copy(layout: list[list[str]]):
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

        m, n = len(layout), len(layout[0])

        max_evaluation_score, max_directions = -float('inf'), []

        for direction, (delta_x, delta_y) in ALL_DIRECTIONS.items():
            new_x, new_y = row + delta_x, col + delta_y
            if 0 <= new_x < m and 0 <= new_y < n and layout[new_x][new_y] != "%":
                for f_x, f_y in FOOD_POSITIONS:
                    current_score = expectimax(k, new_x, new_y, w_rs, w_cs, f_x, f_y)
                    if current_score > max_evaluation_score:
                        max_evaluation_score = current_score
                        max_directions = [direction]
                    elif current_score == max_evaluation_score:
                        max_directions.append(direction)

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
    k = k * (1 + number_of_ghost) - 1
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
    problem_id = 6
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
        solution, winner = expectimax_multiple_ghost(copy.deepcopy(problem), k, verbose)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
