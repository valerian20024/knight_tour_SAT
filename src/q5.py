from knight_tour import build_knight_tour, extract_all_solutions, model_to_solution
import random

def question5_fair(M, N, i0, j0):
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
        print(f"           {p[0:12]} {hash(p)}")
        print()
    
    
    # The chosen path to which the others will be compared
    ref_path = random.choice(paths)
    constraints = set()
    
    # Eliminating every other solution
    for alt_path in paths:
        if alt_path is not ref_path:  # don't kill the chosen one
            print(f"ref path : {ref_path} {hash(ref_path)}")
            print(f"alt path : {alt_path} {hash(alt_path)}")

            # Check whether this alternative already violates one of the constraints
            blocked = False
            for t, forced_i, forced_j in constraints:
                if alt_path[t] != (forced_i, forced_j):
                    blocked = True
                    break
            if blocked:
                continue  # path is already unreachable given the constraints
            
            # Finding the constraint tat can differentiate two paths
            for t in range(1, T):  # t = 0 is the fixed start, don't change it.
                if alt_path[t] != ref_path[t]:
                    print(f"    alt_path[{t}] != ref_path[{t}] ==> {alt_path[t]} != {ref_path[t]}")
                    i, j = ref_path[t]         # force the reference position
                    print(f"    Adding constraint : (t: i, j) = ({t}: {i}, {j})")
                    constraints.add((t, i, j))
                    break
        print(f"constraints:\n  {constraints}")
    # swapping back to normal i, j, t indexing
    constraints = [(i, j, t) for (t, i, j) in constraints]
    return list(constraints)