import sys, random, grader, parse, math, copy


def random_play_multiple_ghosts(problem):
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

    def get_ghost_nums(layout: list[list[str]]) -> int:
        seen = set()
        for i in range(len(layout)):
            for j in range(len(layout[0])):
                if layout[i][j] not in seen:
                    seen.add(layout[i][j])
        return len(seen) - 4

    def determine_direction_and_random_choose_for_pacman(layout: list[list[str]], row: int, col: int) -> str:
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
            if 0 <= new_x < m and 0 <= new_y < n and layout[new_x][new_y] != "%":
                directions.append(direction)
        return random.choice(directions)

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
                    cnt += 1
        return cnt

    def move_pacman(layout: list[list[str]], x: str, y: str) -> (bool, int, int, list[list[str]]):
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
        direction = determine_direction_and_random_choose_for_pacman(layout, x, y)

        actions.append(direction)
        delta_x, delta_y = ALL_DIRECTIONS[direction]
        layout = copy.deepcopy(layout)
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

    def move_ghost(layout: list[list[str]], x: int, y: int):
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
        layout = copy.deepcopy(layout)
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
    number_of_ghost = get_ghost_nums(layout)
    ghosts = ORDER[:number_of_ghost]

    random.seed(int(seed))
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
        layout = copy.deepcopy(layout)
        finish, p_r, p_c, layout = move_pacman(layout, p_r, p_c)
        layout = copy.deepcopy(layout)
        if finish:
            break
        for i in range(number_of_ghost):
            finish, w_rs[i], w_cs[i], layout = move_ghost(layout, w_rs[i], w_cs[i])
            layout = copy.deepcopy(layout)
            if finish:
                break
        if finish:
            break

    solution = generate_result(actions, subjects, layouts, scores, WINNER, seed)
    return solution


if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -7
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)
