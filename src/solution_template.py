from knight_tour import *
from symmetry import count_solutions_up_to_symmetry
from plot import rainbow_plot
from helpers import leave_one_out_subsets

def question1(M, N, i0, j0):
    solver, variables = build_knight_tour(M, N, i0, j0)
    solution = extract_solution(solver, M, N, variables)
    
    return solution, solver, list(variables.values())

def question3():
    M = 3
    N = 4

    nb_sol = 0
    for i0 in range(M):
        for j0 in range(N):
            solver, variables = build_knight_tour(M, N, i0, j0)
            solutions, _ = extract_all_solutions(solver, M, N, variables)

            nb_sol += len(solutions)
    return nb_sol

def question4():
    M = 3
    N = 4
        
    nb_sol = 0
    for i0 in range(M):
        for j0 in range(N):
            solver, variables = build_knight_tour(M, N, i0, j0, 'sc')
            solutions, _ = extract_all_solutions(solver, M, N, variables)
            nb_sol += count_solutions_up_to_symmetry(solutions, M, N)
    
    return nb_sol

def question5(M, N, i0, j0):
        
    solver_base, vars_base = build_knight_tour(M, N, i0, j0, mode='sc')
    base_solutions, _ = extract_all_solutions(solver_base, M, N, vars_base)

    solver_constrained, vars_constrained = build_knight_tour(M, N, i0, j0, mode='sc')
    constraints = get_uniqueness_constraints(M, N, i0, j0)

    for c in constraints:
        solver_constrained.add_clause([vars_constrained[c]])
    constraints_solutions, _ = extract_all_solutions(solver_constrained, M, N, vars_constrained)
    constraints_solutions = solve_with_constraints(constraints, M, N, i0, j0)
    
    for sol in constraints_solutions:
        print(f"{sol} {hash(str(sol))}")
    
    subsets = leave_one_out_subsets(constraints)
    
    for subset in subsets:
        solutions = solve_with_constraints(subset, M, N, i0, j0)
        
        for sol in solutions:
            print(f"    solution: {sol} {hash(str(sol))}")

    return constraints
