from plot import rainbow_plot

"""Apply vertical axial symmetry: (i, j) -> (i, N-1-j)."""
def vertical_symmetry(solution, M, N):
    new_solution = [[-1] * N for _ in range(M)]
    for i in range(M):
        for j in range(N):
            new_solution[i][N-1-j] = solution[i][j]
    return new_solution

"""Apply a horizontal symmetry to a solution"""
def horizontal_symmetry(solution, M, N):
    new_solution = [[-1] * N for _ in range(M)]
    for i in range(M):
        for j in range(N):
            new_solution[M-1-i][j] = solution[i][j]
    return new_solution

"""Apply a central symmetry to a solution"""
def central_symmetry(solution, M, N):
    new_solution = [[-1] * N for _ in range(M)]
    for i in range(M):
        for j in range(N):
            new_solution[M-1-i][N-1-j] = solution[i][j]
    return new_solution

"""Check if solution1 is equivalent to solution2 using any symmetry."""
def are_equivalent(solution1, solution2, M, N):
    # Check identity (no symmetry)
    if solution1 == solution2:
        return True
    if vertical_symmetry(solution2, M, N) == solution1:
        return True
    if horizontal_symmetry(solution2, M, N) == solution1:
        return True
    if central_symmetry(solution2, M, N) == solution1:
        return True
    return False

"""Count the number of distinct solutions up to symmetry."""
def count_solutions_up_to_symmetry(solutions, M, N):
    if not solutions:
        return 0

    groups = []
    for sol in solutions:
        # Check if sol belongs to an existing group
        found = False
        for group in groups:
            if are_equivalent(sol, group[0], M, N):
                group.append(sol)
                found = True
                break
        if not found:
            groups.append([sol])
    
    return len(groups)