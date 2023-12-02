import sys, grader, parse
from copy import deepcopy
import random
import p4

def transform(score, grid, Exit, dir_map):
    res = []
    for i in range(len(score)):
        res_line = []
        for j in range(len(score[0])):
            if [i, j] in Exit:
                res_line.append('x')
            elif grid[i][j] == '#':
                res_line.append('#')
            else:
                index = score[i][j].index(max(score[i][j]))
                res_line.append(dir_map[index])
        res.append(res_line)
    return res


def write_res(res_matrix):
    res = ''
    for i in range(len(res_matrix)):
        for j in range(len(res_matrix[0])):
            Format = '|{:^3}|'.format(res_matrix[i][j])
            res = f'{res}{Format}'
        if i + 1 == len(res_matrix):
            res = f'{res}'
        else:
            res = f'{res}\n'
    return res


def write_score(score):
    res = ''
    for i in range(len(score)):
        res_line = ''
        for j in range(len(score[0])):
            string = ''
            for k in score[i][j]:
                if k == '#':
                    string = f'{string}{k:^3}'
                else:
                    string = f'{string}{k:.3f} '
            res_line = f'{res_line}|{string}|'
        res = f'{res}{res_line}\n '

    return res


def td_learning(problem):
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    dir_map = {'N': 0, 0: 'N', 'E': 1, 1: 'E', 'S': 2, 2: 'S', 'W': 3, 3: 'W'}
    grid = problem['grid']
    D1 = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    D = {'N': ['N', 'E', 'W', 'S'], 'E': ['E', 'S', 'N', 'W'], 'S': ['S', 'W', 'E', 'N'], 'W': ['W', 'N', 'S', 'E']}
    Dir = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}
    m = len(grid)
    n = len(grid[0])
    iterations = 3000
    eposlion = 0.2
    learning_rate = 0.6
    # print(f'eposlion:{eposlion}')
    # print(f'learning_rate:{learning_rate}')
    policy = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S' or grid[i][j] == '_':
                policy[i][j] = 'N'
            elif grid[i][j] == '#':
                policy[i][j] = '#'
            elif grid[i][j] != '#':
                policy[i][j] = 'x'
    policy = [['E', 'E', 'E', 'x'],
              ['N', '#', 'E', 'x'],
              ['N', 'E', 'N', 'S']]
    p_is_run = 0
    Exit = []
    P_pos = []
    score = [[[0 for _ in range(4)] for _ in range(n)] for _ in range(m)]  # N,E,S,X
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                P_pos.append([i, j])
            elif grid[i][j] == '#':
                score[i][j] = ['#', '#', '#', '#']
            elif grid[i][j] != '_':
                Exit.append([i, j])
    P_pos_New = [P_pos[0][0], P_pos[0][1]]
    check = ''
    check1 = ''
    while (iterations):
        # print(iterations)
        check = f'{check}iterations:{iterations}\n{write_score(score)}\n'
        check1 = f'{check1}iterations:{iterations}\n{write_res(transform(score, grid, Exit, dir_map))}\n'
        if (p_is_run):
            iterations -= 1
            p_is_run = 0
            P_pos_New = [P_pos[0][0], P_pos[0][1]]
        intended = policy[P_pos_New[0]][P_pos_New[1]]  # max_direction
        want_taking = \
        random.choices(population=D[intended], weights=[1 - eposlion, eposlion / 3, eposlion / 3, eposlion / 3])[0]
        taking = random.choices(population=D1[want_taking], weights=[1 - 2 * noise, noise, noise])[0]
        new_X = P_pos_New[0] + Dir[taking][0]
        new_Y = P_pos_New[1] + Dir[taking][1]
        temp = (1 - learning_rate) * score[P_pos_New[0]][P_pos_New[1]][dir_map[want_taking]]
        for i in D1[want_taking]:
            xx = P_pos_New[0] + Dir[i][0]
            yy = P_pos_New[1] + Dir[i][1]
            maxx = 0
            if xx >= 0 and xx < m and yy >= 0 and yy < n and grid[xx][yy] != '#':
                maxx = max(score[xx][yy])
            else:
                maxx = max(score[P_pos_New[0]][P_pos_New[1]])
            if i == want_taking:
                temp += (1 - 2 * noise) * learning_rate * (livingReward + discount * maxx)
            else:
                temp += (noise) * learning_rate * (livingReward + discount * maxx)
        score[P_pos_New[0]][P_pos_New[1]][dir_map[want_taking]] = temp
        max_dir_list = []
        for index, i in enumerate(score[P_pos_New[0]][P_pos_New[1]]):
            if i == max(score[P_pos_New[0]][P_pos_New[1]]):
                max_dir_list.append(index)
        policy[P_pos_New[0]][P_pos_New[1]] = dir_map[random.choice(max_dir_list)]
        if new_X >= 0 and new_X < m and new_Y >= 0 and new_Y < n and grid[new_X][new_Y] != '#':
            P_pos_New[0] = new_X
            P_pos_New[1] = new_Y
        if [P_pos_New[0], P_pos_New[1]] in Exit:
            f = (1 - learning_rate) * score[P_pos_New[0]][P_pos_New[1]][0] + learning_rate * (
                        discount * float(grid[P_pos_New[0]][P_pos_New[1]]))
            score[P_pos_New[0]][P_pos_New[1]] = [f, f, f, f]
            p_is_run = 1

    res_matrix = transform(score, grid, Exit, dir_map)
    return_value = write_res(res_matrix)
    return return_value

print(td_learning(parse.read_grid_mdp_problem_p4('test.prob'))==p4.td_learning(parse.read_grid_mdp_problem_p4('test.prob')))
print(td_learning(parse.read_grid_mdp_problem_p4('test.prob')),"\n")
print(p4.td_learning(parse.read_grid_mdp_problem_p4('test.prob')))