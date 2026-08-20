from pysat.solvers import Glucose3
from constraints import *
import random

def extract_solution(solver: Glucose3, M: int, N: int, var: dict) -> list[list[int]]: 
    """Return one solution from the solver.
    
    If no solutions, returns a -1 initialized list.
    """

    if not solver.solve():
        return [[-1 for _ in range(N)] for _ in range(M)]

    model = solver.get_model()  # list of all the variables
    return model_to_solution(model, M, N, var)

# todo rewrite to get rid of the res return. Return an empty list.
def extract_all_solutions(solver: Glucose3, M: int, N: int, var: dict):
    """Return all the solutions from the solver."""

    res = False
    solutions = []

    if solver.solve():
        res = True
        seen = set()
        for model in solver.enum_models():  # list of all the variables
            solution = model_to_solution(model, M, N, var)
            # Convert to tuple of tuples for hashing
            sol_tuple = tuple(tuple(row) for row in solution)
            if sol_tuple not in seen:
                seen.add(sol_tuple)
                solutions.append(solution)

    return solutions, res

def model_to_solution(model, M, N, var) -> list[list]:
    """Helper function to convert a SAT model into a solution matrix."""

    T = M * N

    solution = [[-1 for _ in range(N)] for _ in range(M)]
    for index in range(T):
        for i in range(M):
            for j in range(N):
                # model[] is 0-indexed while variables are 1-indexed
                # Check var(123) => check model[122]
                if model[var[(i, j, index)] - 1] > 0:   # positive literal
                    solution[i][j] = index
                    break
    return solution


def build_knight_tour(M, N, i0, j0, mode='n'):
    """Orchestrator to build the Knight's Tour problem, adding constraints.

    @param M: The number of rows in the chessboard.
    @param N: The number of columns in the chessboard.
    @param i0: The start row (0-indexed)
    @param j0: The start column (0-indexed)
    @param mode: Whether to use naive or efficient constraints.
    """

    solver = Glucose3()
    T = M * N
    vars = {}  # Dict(i, j, t) -> variable id

    # Populating dict for each i, j, timestep
    var_id = 1
    for t in range(T):
        for i in range(M):
            for j in range(N):
                vars[(i, j, t)] = var_id
                var_id += 1

    solver.add_clause([vars[(i0, j0, 0)]])
    if (mode == 'n'):
        _, _ = add_cell_constraints_naive(solver, M, N, vars)
        _, _ = add_time_constraints_naive(solver, M, N, vars)
    elif (mode == 'sc'):
        _, _, var_id = add_cell_constraints_sequential_counter(solver, M, N, vars, var_id)
        _, _, var_id = add_time_constraints_sequential_counter(solver, M, N, vars, var_id)
    add_legal_moves_constraints(solver, M, N, vars)

    return solver, vars

def solve_with_constraints(extra_constraints, M, N, i0, j0):
    """ Builds the knight tour problem with additional specified constraints 
    and solves it, returning all solutions.
    """

    solver, vars = build_knight_tour(M, N, i0, j0, mode='sc')
    for ec in extra_constraints:
        lit = vars[ec]
        solver.add_clause([lit])

    sols, _ = extract_all_solutions(solver, M, N, vars)
    return sols

#todo rename uniqueness constraints
def get_uniqueness_constraints(M, N, i0, j0) -> list:
    """Computes the strictly necessary set of constraints to ensure 
    the problem has a unique solution. 
    
    Adding these constraints to the SAT solver will ensure only one solution. 
    Add a strictly smaller subset of them to the SAT solver will make it output
    several solutions.

    @return constraints written as (t, i, j)
    """

    random.seed()
    T = M * N

    solver, variables = build_knight_tour(M, N, i0, j0, mode='sc')
    solutions, _ = extract_all_solutions(solver, M, N, variables)

    # 0 or 1 solution is already unique
    if len(solutions) <= 1:
        return []

    # Build paths: path[t] = (i,j) represents where the knight was at t
    paths = set()
    for sol in solutions:
        path = [None] * T
        for i in range(M):
            for j in range(N):
                if sol[i][j] >= 0:
                    path[sol[i][j]] = (i, j)
        paths.add(tuple(path))
    paths = tuple(paths)
    
    # A reference path will be compared with alternative paths
    ref_path = random.choice(paths)
    constraints = set()
    
    # Eliminate every alternative path. Output the constraint on i, j, t
    # that will allow to only keep the reference path as solution.
    for alt_path in paths:
        if alt_path is not ref_path:  # don't kill the chosen one
            # Check whether this alternative already violates one of the constraints
            blocked = False
            for t, forced_i, forced_j in constraints:
                if alt_path[t] != (forced_i, forced_j):
                    blocked = True
                    break
            if blocked:
                continue  # alt path unreachable given current constraints
            
            # Finding the constraint that can differentiate two paths.
            # Constraints are indexed using t, i, j order
            # Start at 1 since every path starts the same at t = 0
            for t in range(1, T):  
                if alt_path[t] != ref_path[t]:
                    i, j = ref_path[t]  # force the reference position
                    constraints.add((t, i, j))
                    break

    return list(constraints)