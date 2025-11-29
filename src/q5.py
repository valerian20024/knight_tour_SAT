from knight_tour import build_knight_tour, extract_all_solutions, model_to_solution
import random

"""BASE QUESTION 5 FUNCTION. NOT FAIR"""
def q5(M, N, i0, j0):
    T = M * N
    solver, variables = build_knight_tour(M, N, i0, j0, mode='sc')  # 'sc' is faster for enumeration on larger boards

    solutions, has_sol = extract_all_solutions(solver, M, N, T, variables)

    # If no solution exists or the problem already has a unique solution → no extra constraints needed
    if not has_sol or len(solutions) <= 1:
        return []

    # Convert every solution into a path: path[t] = (i, j)
    paths = []
    for sol in solutions:
        print("solution: ", sol)
        path = [None] * T
        for i in range(M):
            for j in range(N):
                if sol[i][j] >= 0:
                    path[sol[i][j]] = (i, j)
        print("path: ", path)
        paths.append(tuple(path))          # tuple so we can sort

    # Use the lexicographically smallest tour as reference (deterministic)
    paths.sort()
    print("paths sorted: ")
    for p in paths: 
        print("  path: ", p)
    ref_path = list(paths[0])

    constraints = []

    for alt_path_tuple in paths[1:]:
        alt_path = list(alt_path_tuple)

        # If the alternative tour still agrees with the reference on all previously forced timesteps,
        # we have to force an additional timestep to distinguish it
        if all(alt_path[t] == ref_path[t] for t, _, _ in constraints):
            # Force the earliest differing timestep (makes the set small and “early”)
            for t in range(1, T):
                if alt_path[t] != ref_path[t]:
                    i, j = ref_path[t]
                    constraints.append((t, i, j))
                    break

    # Sort constraints by timestep (optional but nice for the output)
    constraints.sort(key=lambda c: c[0])

    return constraints




"""UPDATED QUESTION 5 FUNCTION. FAIR"""
def question5_fair(M, N, i0, j0):
    print("Q5 finding set of constraints")
    #random.seed(M * 10000 + N * 1000 + i0 * 10 + j0)  # deterministic per input, varies across inputs
    random.seed()

    T = M * N
    solver, variables = build_knight_tour(M, N, i0, j0, mode='sc')
    solutions, has_sol = extract_all_solutions(solver, M, N, T, variables)

    if not has_sol or len(solutions) <= 1:
        print("NO SOLUTION")
        return []

    
    # Build paths
    paths = set()  # keep unique paths to improve computation time
    for sol in solutions:
        path = [None] * T
        for i in range(M):
            for j in range(N):
                if sol[i][j] >= 0:
                    path[sol[i][j]] = (i, j)
        paths.add(tuple(path))

    paths = tuple(paths)  # to be able to index it

    print(f"\nPaths:")
    for p in paths:
        print(p[0:12])
        print("...")

    # Pick one randomly (but deterministically per input)
    ref_path = random.choice(paths)
    #ref_path = paths[0]
    constraints = []
    
    # ---- eliminate every other solution ----
    for alt_path in paths:
        if alt_path is ref_path:  # don't kill the chosen one
            continue
        print(f"ref path : {ref_path}")
        print(f"alt path : {alt_path}")

        # Check whether this alternative already violates one of the constraints
        print("Does it already violates one of the constraints?")
        blocked = False
        for t, forced_i, forced_j in constraints:
            if alt_path[t] != (forced_i, forced_j):
                blocked = True
                print("  yes")
                break

        if blocked:
            print("   we go find another alt path\n")
            continue                       # already dead -> nothing to do

        print("Still alive -> add the earliest constraint that kills it")
        # Still alive -> add the earliest constraint that kills it
        for t in range(1, T):  # t = 0 is the fixed start, don't change it.
            if alt_path[t] != ref_path[t]:
                print(f"    alt_path[{t}] != ref_path[{t}] ==> {alt_path[t]} != {ref_path[t]}")
                i, j = ref_path[t]         # force the reference position
                print(f"    Constraint : (t: i, j) = ({t}: {i}, {j})")
                constraints.append((t, i, j))
                print(f"    we break for t values")
                break

    print("constraints")
    print(constraints)
    constraints.sort(key=lambda x: x[0])
    print(constraints)
    return constraints