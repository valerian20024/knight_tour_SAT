from pysat.solvers import Glucose3
from constraints import *
import random

"""
Return one solution from the solver.
"""
def extract_solution(solver, M, N, T, var):
    res = False
    solution = None
    if solver.solve():
        res = True
        model = solver.get_model()  # list of all the variables
        solution = model_to_solution(model, M, N, T, var)

    return solution, res

"""
Return all the solutions from the solver.
def extract_all_solutions_base(solver, M, N, T, var):
    res = False
    solutions = []
    if solver.solve():
        res = True
        for model in solver.enum_models():  # list of all the variables
            solution = model_to_solution(model, M, N, T, var)
            solutions.append(solution)

    return solutions, res
"""

"""
Return all the solutions from the solver.
"""
def extract_all_solutions(solver, M, N, T, var):
    res = False
    solutions = []
    if solver.solve():
        res = True
        seen = set()
        for model in solver.enum_models():  # list of all the variables
            solution = model_to_solution(model, M, N, T, var)
            # Convert to tuple of tuples for hashing
            sol_tuple = tuple(tuple(row) for row in solution)
            if sol_tuple not in seen:
                seen.add(sol_tuple)
                solutions.append(solution)

    return solutions, res

"""Helper function to convert a SAT model into a solution matrix."""
def model_to_solution(model, M, N, T, var):
    solution = [[-1] * N for m in range(M)]  # N x M list filled with -1
    for index in range(T):
        for i in range(M):
            for j in range(N):
                # model[] is 0-indexed while variables are 1-indexed
                # Check var(123) => check model[122]
                if model[var[(i, j, index)] - 1] > 0:   # positive literal
                    solution[i][j] = index
                    break
    return solution

"""
This function will solve the Knight's Tour problem.

@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param i0: The start row (0-indexed)
@param j0: The start column (0-indexed)
@param mode: Whether to use naive or efficient constraints.
"""
def build_knight_tour(M, N, i0, j0, mode='n'):
    #print(f"solve_knight_tour: {M}x{N}@({i0}, {j0}) in {mode} mode")
    solver = Glucose3()
    
    T = M * N  # Number of timesteps
    var = {}  # (i,j,t) -> variable id
    var_id = 1

    # Populating dict for each i, j, timestep
    for t in range(T):
        for i in range(M):
            for j in range(N):
                var[(i, j, t)] = var_id
                var_id += 1

    # Adding the start position clause
    solver.add_clause([var[(i0, j0, 0)]])

    if (mode == 'n'):
        _, _ = add_cell_constraints_naive(solver, M, N, T, var)
        _, _ = add_time_constraints_naive(solver, M, N, T, var)
    elif (mode == 'sc'):
        _, _, var_id = add_cell_constraints_sequential_counter(solver, M, N, T, var, var_id)
        _, _, var_id = add_time_constraints_sequential_counter(solver, M, N, T, var, var_id)

    add_legal_moves_constraints(solver, M, N, T, var)

    return solver, var


"""
Builds the knight tour problem with additional specified constraints 
and solves it, returning all solutions.
"""
def solve_with_constraints(extra_constraints, M, N, i0, j0):
    T = M * N

    solver, vars = build_knight_tour(M, N, i0, j0, mode='sc')
    for ec in extra_constraints:
        lit = vars[ec]
        solver.add_clause([lit])

    sols, _ = extract_all_solutions(solver, M, N, T, vars)
    return sols

"""
Computes the strictly necessary set of constraints to ensure 
the problem has only one solution. Adding these constraints
to the SAT solver will ensure only one solution. Add a strictly 
smaller subset of them to the SAT solver will make it output
several solutions.
"""
def get_uniqueness_constraints(M, N, i0, j0):
    random.seed()  # to ensure outputs fairness

    T = M * N
    solver, variables = build_knight_tour(M, N, i0, j0, mode='sc')
    solutions, has_sol = extract_all_solutions(solver, M, N, T, variables)

    if not has_sol or len(solutions) <= 1:
        return []

    # Build paths representing the knight's moves.
    paths = set()  # keep unique paths to improve computation time
    for sol in solutions:
        path = [None] * T
        for i in range(M):
            for j in range(N):
                if sol[i][j] >= 0:
                    path[sol[i][j]] = (i, j)
        paths.add(tuple(path))
    paths = tuple(paths)  # to be able to index it

    """print(f"\nPaths:")
    for p in paths:
        print(f"           {p[0:12]} {hash(p)}")
        print()"""
    
    # A reference path will be compared with alternative paths
    ref_path = random.choice(paths)
    constraints = set()
    
    # Eliminate every alternative path. Output the constraint on i, j, t
    # that will allow to only keep the reference path as solution.
    for alt_path in paths:
        if alt_path is not ref_path:  # don't kill the chosen one
            """print(f"ref path : {ref_path} {hash(ref_path)}")
            print(f"alt path : {alt_path} {hash(alt_path)}")"""

            # Check whether this alternative already violates one of the constraints
            blocked = False
            for t, forced_i, forced_j in constraints:
                if alt_path[t] != (forced_i, forced_j):
                    blocked = True
                    break
            if blocked:
                continue  # alt path unreachable given current constraints
            
            # Finding the constraint that can differentiate two paths.
            # Constraints are indexed using t, i, j order because paths are
            # inherently a set of t-indexed (i, j) pairs.
            for t in range(1, T):  # every path starts at the same place at t = 0
                if alt_path[t] != ref_path[t]:
                    i, j = ref_path[t]  # force the reference position
                    constraints.add((t, i, j))
                    break

    # Swapping back to normal i, j, t indexing
    constraints = [(i, j, t) for (t, i, j) in constraints]
    return constraints