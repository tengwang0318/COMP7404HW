import sys, grader, collections, parse


def bfs_search(problem: dict[str]) -> str:
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
    start_state, goal_states, heuristic, transitions = problem['start_state'], problem["goal_states"], \
        problem["heuristic"], problem["transitions"]
    queue = collections.deque()
    queue.append([[start_state], 0])
    seen = list()

    while queue:
        temp_length = len(queue)
        for _ in range(temp_length):
            temp = queue.popleft()
            # print(temp)
            if temp[0][-1] in seen:
                continue
            current_node = temp[0][-1]
            # print(current_node)
            if current_node in goal_states:
                solution = " ".join(seen) + "\n" + " ".join(temp[0])

                return solution

            if current_node in transitions:
                for item in transitions[current_node]:
                    new_lists = temp[0][:]
                    new_lists.append(item[1])
                    # print(item)
                    queue.append([new_lists, float(item[0]) + temp[1]])
            seen.append(temp[0][-1])
    return False


if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)
