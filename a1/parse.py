import os, sys


def read_graph_search_problem(file_path: str) -> dict[str]:
    # Your p1 code here
    """
    I think after change of dict in python 3.6, the following design will be okay.
    :param file_path: str
    :return: dict()
             the pattern likes: {
             "start_state": str,
             ""goal_states": set(str),
             "heuristic": {
                    "state": int
             },
             "transitions": {
                    f"{start_state}": [[weight,f"{end_node}], ..."]
                }
             }
    """
    problem = {
        'heuristic': {},
        "transitions": {}
    }
    with open(file_path) as f:
        for text in f.readlines():
            if "start_state" in text:
                problem["start_state"] = text.split()[1]
            elif "goal_states" in text:
                problem["goal_states"] = set(text.split()[1:])
            elif len(text.split()) == 2:
                temp_node, temp_heuristic = text.split()
                problem["heuristic"][temp_node] = temp_heuristic
            else:
                start_node, end_node, weight = text.split()
                if start_node not in problem['transitions']:
                    problem["transitions"][start_node] = [[weight, end_node]]
                else:
                    problem['transitions'][start_node].append([weight, end_node])

    return problem


# for key, val in read_graph_search_problem("test_cases/p1/6.prob").items():
#     print(key, val)


def read_8queens_search_problem(file_path: str) -> list[list[str]]:
    problem = []
    with open(file_path) as f:
        for items in f.readlines():
            problem.append(items.split())
    return problem


# print(read_8queens_search_problem("test_cases/p7/1.prob"))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
