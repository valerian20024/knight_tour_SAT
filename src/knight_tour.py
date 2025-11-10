from pysat.solvers import Glucose3
from constraints import *


def extract_solution(solver, M, N, T, var):
    res = False
    if solver.solve():
        print("Solution found")
        res = True
        model = solver.get_model()  # list of all the variables
        solution = model_to_solution(model, M, N, T, var)

    return solution, res

def extract_all_solutions(solver, M, N, T, var):
    res = False
    solutions = []
    if solver.solve():
        res = True
        for model in solver.enum_models():  # list of all the variables
            solution = model_to_solution(model, M, N, T, var)
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
@param mode: Whether to use naive quadratic constraints or linear ones






"""
def build_knight_tour(M, N, i0, j0, mode='n', solutions='one'):
    print(f"solve_knight_tour: {M}x{N}@({i0}, {j0}) in {mode} mode")
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



