import sys, parse, grader
from heapq import heappush, heappop


def astar_search(problem: dict[str]) -> str:
    """
    priority_queue: [(heuristic[current_node] + transition[current_node], path)]

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
    :return:
    """
    start_state, goal_states, heuristic, transitions = problem["start_state"], problem["goal_states"], \
        problem['heuristic'], problem['transitions']
    pq = [(float(heuristic[start_state]), [start_state])]
    seen = list()
    while pq:
        current_cost, current_path = heappop(pq)
        current_node = current_path[-1]
        if current_node not in seen:
            if current_node in goal_states:
                return " ".join(seen) + "\n" + " ".join(current_path)
            if current_node in transitions:
                for weight, temp_node in transitions[current_node]:
                    old_g = current_cost - float(heuristic[current_node])
                    new_g = old_g + float(weight)
                    new_h = float(heuristic[temp_node])
                    new_path = current_path[:]
                    new_path.append(temp_node)
                    heappush(pq, (new_h + new_g, new_path))
            seen.append(current_node)


if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -7
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)
