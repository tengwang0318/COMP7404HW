#Do not make changes to this file
import os, sys, parse, difflib
import p1, p2, p3, p4, p5, p6, p7, p8

def grade(problem_id, test_case_id, student_code_problem, student_code_parse):
    print('Grading Problem',problem_id,':')
    if test_case_id > 0:
        #single test case
        check_test_case(problem_id, test_case_id, student_code_problem, student_code_parse)
    else:
        #multiple test cases
        num_test_cases = test_case_id * (-1)
        for i in range(1, num_test_cases+1):
            check_test_case(problem_id, i, student_code_problem, student_code_parse)

def check_test_case(problem_id, test_case_id, student_code_problem, student_code_parse):
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    if student_code_parse != None:
        problem = student_code_parse(os.path.join(path,file_name_problem))
        student_solution = student_code_problem(problem)
    else:
        student_solution = student_code_problem()
    solution = ''
    with open(os.path.join(path,file_name_sol)) as file_sol:
        solution = file_sol.read()
    if solution == student_solution:
        print('---------->', 'Test case', test_case_id, 'PASSED', '<----------')
    else:
        print('---------->', 'Test case', test_case_id, 'FAILED', '<----------')
        print('Your solution')
        print(student_solution)
        print('Correct solution')
        print(solution)
        #for i,s in enumerate(difflib.ndiff(student_solution, solution)):
        #    if s[0]==' ': continue
        #    elif s[0]=='-':
        #        print(u'Delete "{}" from position {}'.format(s[-1],i))
        #    elif s[0]=='+':
        #        print(u'Add "{}" to position {}'.format(s[-1],i))
                
if __name__ == "__main__":

    try: problem_id = int(sys.argv[1])
    except: problem_id = -1    
    if problem_id == -1 or problem_id == 1: grade(1, -7, p1.dfs_search, parse.read_graph_search_problem)
    if problem_id == -1 or problem_id == 2: grade(2, -7, p2.bfs_search, parse.read_graph_search_problem)
    if problem_id == -1 or problem_id == 3: grade(3, -8, p3.ucs_search, parse.read_graph_search_problem)
    if problem_id == -1 or problem_id == 4: grade(4, -7, p4.greedy_search, parse.read_graph_search_problem)
    if problem_id == -1 or problem_id == 5: grade(5, -7, p5.astar_search, parse.read_graph_search_problem)
    if problem_id == -1 or problem_id == 6: grade(6, -4, p6.number_of_attacks, parse.read_8queens_search_problem)
    if problem_id == -1 or problem_id == 7: grade(7, -6, p7.better_board, parse.read_8queens_search_problem)
    if problem_id == -1 or problem_id == 8: grade(8, -1, p8.all_solutions, None)