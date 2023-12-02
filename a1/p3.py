import sys, parse, grader, collections
from heapq import heappush, heappop


def ucs_search(problem: dict[str]) -> str:
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
    start_state, goal_states, heuristic, transitions = problem["start_state"], problem['goal_states'], \
        problem["heuristic"], problem['transitions']
    pq = [(0, [start_state])]
    seen = []
    while pq:
        cost, path = heappop(pq)
        if path[-1] in goal_states:
            return " ".join(seen) + "\n" + " ".join(path)
        if path[-1] not in seen:
            if path[-1] in transitions:
                for (weight, end) in transitions[path[-1]]:
                    if end not in seen:
                        new_path = path[:]
                        new_path.append(end)
                        heappush(pq, [float(weight) + cost, new_path])
            seen.append(path[-1])

    return solution


# print(ucs_search(parse.read_graph_search_problem("test_cases/p3/1.prob")))
if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -8
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)
