def num(s):
    try:
        return float(int(s))
    except ValueError:
        return float(s)


def read_grid_mdp_problem_p1(file_path):
    problem = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = "".join(f.readlines())

    lines = data.strip().split('\n')
    problem['seed'] = int(lines[0].split(":")[1])
    problem['noise'] = float(lines[1].split(":")[1])
    problem['livingReward'] = float(lines[2].split("livingReward:")[1])
    grid_start = lines.index('grid:') + 1
    grid_end = lines.index('policy:') - 1
    problem['grid'] = [line.strip().split() for line in lines[grid_start:grid_end + 1]]

    policy_start = lines.index('policy:') + 1
    problem['policy'] = [line.strip().split() for line in lines[policy_start:]]
    return problem


# print(read_grid_mdp_problem_p1("test_cases/p1/1.prob"))

def read_grid_mdp_problem_p2(file_path):
    problem = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = "".join(f.readlines())
    lines = data.split('\n')
    problem['discount'] = num(lines[0].split(":")[1])
    problem['noise'] = num(lines[1].split(':')[1])
    problem['livingReward'] = num(lines[2].split(":")[1])
    problem['iterations'] = num(lines[3].split(":")[1])

    grid_start = lines.index('grid:') + 1
    grid_end = lines.index('policy:') - 1
    problem['grid'] = [line.strip().split() for line in lines[grid_start:grid_end + 1]]

    policy_start = lines.index('policy:') + 1
    problem['policy'] = [line.strip().split() for line in lines[policy_start:]]
    return problem


# print(read_grid_mdp_problem_p2('test_cases/p2/1.prob'))
def read_grid_mdp_problem_p3(file_path):
    # Your p3 code here
    problem = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = "".join(f.readlines())
    lines = data.split("\n")
    problem['discount'] = num(lines[0].split(":")[1])
    problem['noise'] = num(lines[1].split(":")[1])
    problem['livingReward'] = num(lines[2].split(":")[1])
    problem['iterations'] = num(lines[3].split(":")[1])
    grid_start = lines.index('grid:') + 1

    problem['grid'] = [line.strip().split() for line in lines[grid_start:]]
    return problem


# print(read_grid_mdp_problem_p3('test_cases/p3/1.prob'))

def read_grid_mdp_problem_p4(file_path):
    problem = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        data = "".join(f.readlines())
    lines = data.split("\n")
    problem['discount'] = num(lines[0].split(":")[1])
    problem['noise']=num(lines[1].split(":")[1])
    problem['livingReward'] = num(lines[2].split(":")[1])
    grid_start_index=lines.index("grid:")+1
    problem['grid']=[line.strip().split() for line in lines[grid_start_index:]]
    return problem
# print(read_grid_mdp_problem_p4('test_cases/p4/1.prob'))