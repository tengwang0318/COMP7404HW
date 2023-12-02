import sys, parse, grader, collections
from heapq import heappush, heappop


def greedy_search(problem:dict[str])->str:
    """
    priority_queue: [(heuristic[current_node], path)]
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
    start_state, goal_states, heuristic, transitions = problem["start_state"], problem["goal_states"], \
        problem["heuristic"], problem['transitions']
    pq = [(float(heuristic[start_state]), [start_state])]
    seen = list()
    while pq:
        _, path = heappop(pq)
        current_node = path[-1]
        if current_node not in seen:
            if current_node in goal_states:
                return " ".join(seen) + "\n" + " ".join(path)
            if current_node in transitions:
                for _, temp_node in transitions[current_node]:
                    if temp_node in seen:
                        continue
                    new_path = path[:]
                    new_path.append(temp_node)
                    heappush(pq, (float(heuristic[temp_node]), new_path))
            seen.append(current_node)


# print(greedy_search(parse.read_graph_search_problem('test_cases/p4/1.prob')))
# print(greedy_search(parse.read_graph_search_problem("test_cases/p4/5.prob")))
# print(greedy_search(parse.read_graph_search_problem("test_cases/p4/7.prob")))
#
if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -7
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)
