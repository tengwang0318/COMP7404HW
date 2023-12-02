import os, sys


def read_layout_problem(file_path):
    """
    just concatenate strings
    """
    with open(file_path) as f:
        problem = ''.join(f.readlines())
    return problem


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
