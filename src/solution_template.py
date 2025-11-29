from knight_tour import *
from symmetry import count_solutions_up_to_symmetry
from plot import rainbow_plot
from q5 import *
from helpers import leave_one_out_subsets

"""
The first question implementation. Solves the Knight's Tour problem.

@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param i0: The start row (0-indexed)
@param j0: The start column (0-indexed)

@return solution: A list of lists, such that solution[i][j] is the number of
moves required to arrive in cell (i, j). If no solution is found, every cell
value is set to -1.
@return solver: The instance of the solver used.
@return variables: The list of variables used.

"""
def question1(M, N, i0, j0):
    T = M * N
    
    solver, variables = build_knight_tour(M, N, i0, j0)

    solution, _ = extract_solution(solver, M, N, T, variables)

    #print(f"variables: {variables}")
    print(f"solution: {solution}")
    
    return solution, solver, list(variables.values())

"""
The third question implementation.

@return nb_sol: The number of solutions for a given instance of the problem.
"""
def question3():
    M = 3
    N = 4
    T = M * N

    nb_sol = 0
    for i0 in range(M):
        for j0 in range(N):
            solver, variables = build_knight_tour(M, N, i0, j0)
            solutions, _ = extract_all_solutions(solver, M, N, T, variables)
            for sol in solutions:
                print("sol")
                for row in sol:
                    print(f"{row}")

            nb_sol += len(solutions)
            print("Number of solutions", len(solutions))
    
    return nb_sol


"""
The fourth question implementation. Counts the number of solutions up to symmetry. 
Two solutions are identical if one can be obtained by applying a symmetry to the other.

@return nb_sol: The number of solutions up to symmetry of the problem.
"""
def question4():
    M = 3
    N = 4
    T = M * N
    
    nb_sol = 0
    for i0 in range(M):
        for j0 in range(N):
            solver, variables = build_knight_tour(M, N, i0, j0)
            solutions, _ = extract_all_solutions(solver, M, N, T, variables)
            index = 0        
            for sol in solutions:
                rainbow_plot(sol, f"3x4_{index}")
                index += 1
                print("sol")
                for row in sol:
                    print(f"{row}")
            nb_sol += count_solutions_up_to_symmetry(solutions, M, N)
            print("Number of solutions so far", nb_sol)

    return nb_sol

"""
The fifth question implementation. Computes the constraints that guarantee
there is a unique solution. All constraints are necessary for uniqueness
of the solution. They enforce the knight to visit a specific cell at a specific timestep.

@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param i0: The start row (0-indexed)
@param j0: The start column (0-indexed)

@return constraints: Constraints are of the form [(t1, i1, j1), (t2, i2, j2), ...]. If the function is called with parameters such that
no solution exists, it returns an empty list.
"""
def question5(M, N, i0, j0):
    T = M * N
    solver_base, vars_base = build_knight_tour(M, N, i0, j0, mode='sc')
    base_solutions, _ = extract_all_solutions(solver_base, M, N, T, vars_base)

    print("=" * 20 + "\nSOLUTIONS BASE\n" + "=" * 20)

    for sol in base_solutions:
        print(f"  {sol}")
    print(f"  => number of solutions BASE : {len(base_solutions)}")




    print("=" * 30 + "\nTEST 1: ALL CONSTRAINTS REDUCE TO UNIQUE SOL\n" + "=" * 30)

    solver_constrained, vars_constrained = build_knight_tour(M, N, i0, j0, mode='sc')
    constraints = question5_fair(M, N, i0, j0)
    print(f"  constraints: {constraints}")

    """for c in constraints:
        solver_constrained.add_clause([vars_constrained[c]])

    constraints_solutions, _ = extract_all_solutions(solver_constrained, M, N, T, vars_constrained)
    """

    constraints_solutions = solve_with_constraints(constraints, M, N, i0, j0)

    for sol in constraints_solutions:
        print(f"{sol} {hash(str(sol))}")

    print(f"number of solutions FULL ADDITIONAL CONSTRAINTS : {len(constraints_solutions)}")




    print("=" * 30 + "\nTEST 2: REMOVE ANY CONSTRAINT GIVE SEVERAL SOLS\n" + "=" * 30)
    subsets = leave_one_out_subsets(constraints)
    
    print(f"subsets: {subsets}")
    for subset in subsets:
        print(f"  {subset}")
        solutions = solve_with_constraints(subset, M, N, i0, j0)
        print(f"  number of solutions with subset {subset} is {len(solutions)}")
        for sol in solutions:
            print(f"    solution: {sol} {hash(str(sol))}")

    return constraints
