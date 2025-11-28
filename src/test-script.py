from time import time
import os
import solution_template as st
from knight_tour import *

from plot import *

"""
This script generates many solutions and compares timing between the efficient 
and naive solutions.
"""
def timing_test_script():

    def test(m, n, i0, j0, mode):
        dir_path = f"figs/test/{mode}/{m}x{n}/"
        filename = f"{i0}_{j0}"
        path = dir_path + filename
        os.makedirs(dir_path, exist_ok=True)

        start = time()
        solver, var = build_knight_tour(m, n, i0, j0, mode)
        solution, res = extract_solution(solver, m, n, m * n, var)
        end = time()

        if res: 
            rainbow_plot(solution, path)

        return start, end, res

    M = [0, 1, 2, 3, 4, 5, 6]
    N = M

    for m in M:
        for n in N:
            if m <= n:  # avoid to repeat 3x7 and 7x3 solutions
                for i0 in range(m):
                    for j0 in range(n):
                        
                        start_n, end_n, res_n = test(m, n, i0, j0, 'n')
                        start_sc, end_sc, res_sc = test(m, n, i0, j0, 'sc')
                        
                        time_sc = end_sc - start_sc
                        time_n = end_n - start_n
                        
                        print(f"Test {m}x{n}@({i0},{j0})")
                        print(f"  sc: {time_sc}, {res_sc}")
                        print(f"  n : {time_n}, {res_n}")
                        print(f"  BETTER" if time_n > time_sc and res_n and res_sc else "  Meh")
                        

if __name__ == '__main__':

    # Question 1
    #rainbow_plot(st.question1(3, 4, 0, 0)[0], "figs/test/test_rainbow_plot") # custom made
    #rainbow_plot_all(st.question1(3, 4, 0, 0)[0], "figs/test/testrainbowplotall") # plotting all solutions
    
    #timing_test_script()
    #rainbow_plot(st.question1(3, 3, 1, 1)[0], "figs/manual/test_3x3@(1, 1)")

    #plot_solution(st.question1(5, 5, 0, 0)[0]) # there should be a solution
    #plot_solution(st.question1(3, 7, 0, 0)[0]) # there should be a solution
    #plot_solution(st.question1(7, 5, 3, 1)[0]) # there should be a solution
    #plot_solution(st.question1(4, 4, 0, 0)[0]) # there should not be a solution

    # Question 2
    #plot_solution(st.question1(8, 8, 0, 0)[0])
    """
    start = time()
    sol = st.question1(8, 8, 0, 0)[0]
    end = time()
    print(f"end - start = {end - start}")
    
    start = time()
    plot_solution(sol)
    end = time()
    print(f"   end - start = {end - start}")
    """
    
    

    # Question 3
    #print("Number of solutions for a 3x4 chessboard: " + str(st.question3()))

    # Question 4
    #print("Number of solutions for a 3x4 chessboard, up to symmetry: " + str(st.question4()))

    # Question 5
    #print(st.question5(4, 4, 0, 0)) # should be the empty list
    #print(st.question5(3, 4, 1, 3))
    print(st.question5(3, 4, 1, 3)) # should not systematically give the same result as the previous call
