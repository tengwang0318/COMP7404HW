import sys, grader, collections, parse

"""
to-do lists:
    1. a parser to read a search problem in the file parse.py
    2. Depth First Search (DFS) - Graph Search Algorithm (GSA) in the file p1.py

test code:
    run ```python file_name <int>```


return:
    1. Exploration order (i.e., the order in which states are added to the explored set)
    2. solution path (i.e., the first solution found)
problem:
    line 1: start state
    line 2: list of goal states separated by a space (order not relevant)
    line 3 ... (n+2): (n = number of states) heuristic for each state (order not relevant)
                             <state> <heuristic>
    line (n+3) ... end: state transitions of the form (order is relevant)
                      <start state> <end state> <cost>



"""


def dfs_search(problem: dict[str]) -> str:
    """
    :param problem:
     {
             "start_state": str,
             ""goal_states": set(str),
             "heuristic": {
                    "state": int
             },
             "transitions": {
                    f"{start_state}": [weight,f"{end_node}"]
                }

             }
    :return: str
    """
    solution = ""
    seen = []
    start_state, goal_states, heuristic, transitions = problem["start_state"], problem["goal_states"], \
        problem["heuristic"], problem["transitions"]
    stack = [([start_state], 0)]

    while stack:
        temp = stack.pop()
        current_node = temp[0][-1]
        if current_node in goal_states:
            # print(seen)
            # print(temp)
            solution = " ".join(seen) + "\n" + " ".join(temp[0])
            break
        if current_node in transitions:
            for item in transitions[current_node]:
                if item[1] in seen:
                    continue
                new_list = temp[0][:]
                new_list.append(item[1])
                stack.append([new_list, float(item[0]) + temp[1]])
        seen.append(temp[0][-1])
        # print(seen)
    return solution


# dfs_search(parse.read_graph_search_problem("test_cases/p1/2.prob"))
if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -7
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)
