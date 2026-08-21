from time import time
import os
import solution_template as st
from knight_tour import *
from helpers import *
from plot import *
from pathlib import Path

def timing_test_script() -> None:
    """ This script compares timing between many efficient and naive solutions."""

    def chrono(M: int, N: int, i0: int, j0: int, mode: str) -> tuple[float, float, bool]:
        """Tests the time it takes to find a solution.
        
        Returns the start and end time and whether a solution was found.
        """

        start = time()
        solver, vars = build_knight_tour(M, N, i0, j0, mode)
        _, res = extract_solution(solver, M, N, vars)
        end = time()

        return start, end, res

    M = N = range(0, 7)

    for m in M:
        for n in N:
            if m <= n:  # avoid to repeat MxN and NxM solutions
                for i0 in range(m):
                    for j0 in range(n):
                        
                        start_n, end_n, res_n = chrono(m, n, i0, j0, 'n')
                        start_sc, end_sc, res_sc = chrono(m, n, i0, j0, 'sc')
                        
                        time_sc = end_sc - start_sc
                        time_n = end_n - start_n
                        
                        print(f"Test {m}x{n}@({i0},{j0})")
                        print(f"  sc: {time_sc:.3}, {res_sc}")
                        print(f"  n : {time_n:.3}, {res_n}")

def exhaustive_plot() -> None:
    """Plots a single solution (if it exist) from every combination of M, N, i0, j0 and mode.
    
    Saves its result in a dedicated folder under `./figs/auto/`.
    """
    M = N = range(0, 7)
    MODE = ["n", "sc"]

    for m in M:
        for n in M:
            if m <= n:
                dir_path = Path(f"figs/auto/plots_{m}x{n}")
                dir_path.mkdir(parents=True, exist_ok=True)

                for i0 in range(m):
                    for j0 in range(n):
                        for mode in MODE:
                            solver, vars = build_knight_tour(m, n, i0, j0, mode)
                            solution, res = extract_solution(solver, m, n, vars)

                            if res:
                                file_path = dir_path / f"plot_{m}x{n}_{i0}-{j0}_{mode}"
                                rainbow_plot(solution, str(file_path))

if __name__ == '__main__':

    DIR = "figs/manual/"

    # Question 1
    #rainbow_plot(st.question1(5, 5, 0, 0)[0], DIR + "q1") # there should be a solution
    #rainbow_plot(st.question1(3, 7, 0, 0)[0], DIR + "q1") # there should be a solution
    #rainbow_plot(st.question1(7, 5, 3, 1)[0], DIR + "q1") # there should be a solution
    #rainbow_plot(st.question1(4, 4, 0, 0)[0], DIR + "q1") # there should not be a solution
    #rainbow_plot(st.question1(2, 3, 0, 0)[0], DIR + "q1") # there should not be a solution

    # Question 2
    #rainbow_plot(st.question1(8, 8, 0, 0)[0], DIR + "q2")

    # Question 3
    #print("Number of solutions for a 3x4 chessboard: " + str(st.question3()))

    # Question 4
    #print("Number of solutions for a 3x4 chessboard, up to symmetry: " + str(st.question4()))

    # Question 5
    print(st.question5(4, 4, 0, 0)) # should be the empty list
    print(st.question5(3, 4, 1, 3))
    print(st.question5(3, 4, 1, 3)) # should not systematically give the same result as the previous call

    # Custom tests
    #timing_test_script()
    #exhaustive_plot()