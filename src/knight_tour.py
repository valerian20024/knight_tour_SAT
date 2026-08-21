from pysat.solvers import Glucose3
from constraints import *
from helpers import solutions_to_paths
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
    vars = {}  # (i, j, t) -> variable id

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

def uniqueness_constraints(M, N, i0, j0) -> list:
    """Computes a minimal set of constraints that, once added to the
    solver, leaves exactly one solution for the M x N Knight's Tour
    starting at (i0, j0).
    
    Adding these constraints to the SAT solver will ensure only one solution. 
    Add a strictly smaller subset of them to the SAT solver will make it output
    several solutions.

    @return: constraints written as (t, i, j)
    """

    random.seed()
    T = M * N

    solver, variables = build_knight_tour(M, N, i0, j0, mode='sc')
    solutions, has_solution = extract_all_solutions(solver, M, N, variables)

    # 0 or 1 solution is already unique
    if not has_solution or len(solutions) <= 1:
        return []

    # Build paths: path[t] = (i,j) represents where the knight was at t
    paths = solutions_to_paths(solutions, M, N)
    ref_path = random.choice(paths)
    
    constraints = set()  # (t, i, j) constraints
    
    for alt_path in paths:
        if alt_path is ref_path:
            continue

        # If a constraint gathered so far already contradicts alt_path,
        # alt_path is already impossible: no new constraint is needed.
        already_excluded = any(
            alt_path[t] != (i, j) for (t, i, j) in constraints
        )
        if already_excluded:
            continue
        
        # Otherwise, find the first point of divergence with ref_path.
        # (t = 0 is skipped, since every path starts at the same cell)
        for t in range(1, T):  
            if alt_path[t] != ref_path[t]:
                i, j = ref_path[t]
                constraints.add((t, i, j))
                break

    return list(constraints)