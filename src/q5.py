from knight_tour import build_knight_tour, extract_all_solutions, model_to_solution
import random

def question5_fair(M, N, i0, j0):
    print("Q5 finding set of constraints")
    #random.seed(M * 10000 + N * 1000 + i0 * 10 + j0)  # deterministic per input, varies across inputs
    random.seed()

    T = M * N
    solver, variables = build_knight_tour(M, N, i0, j0, mode='sc')
    solutions, has_sol = extract_all_solutions(solver, M, N, T, variables)

    if not has_sol or len(solutions) <= 1:
        #print("NO SOLUTION")
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

    """
    #print(f"\nPaths:")
    for p in paths:
        #print(f"           {p[0:12]} {hash(p)}")
        #print()
    """
        
    ref_path = random.choice(paths)
    constraints = set()
    
    # ---- eliminate every other solution ----
    for alt_path in paths:
        if alt_path is ref_path:  # don't kill the chosen one
            continue
        #print(f"ref path : {ref_path} {hash(ref_path)}")
        #print(f"alt path : {alt_path} {hash(alt_path)}")

        # Check whether this alternative already violates one of the constraints
        #print("Does it already violates one of the constraints?")
        blocked = False
        for t, forced_i, forced_j in constraints:
            if alt_path[t] != (forced_i, forced_j):
                blocked = True
                #print("  yes")
                break

        if blocked:
            #print("   we go find another alt path\n")
            continue                       # already dead -> nothing to do

        #print("Still alive -> add the earliest constraint that kills it")
        for t in range(1, T):  # t = 0 is the fixed start, don't change it.
            if alt_path[t] != ref_path[t]:
                print(f"    alt_path[{t}] != ref_path[{t}] ==> {alt_path[t]} != {ref_path[t]}")
                i, j = ref_path[t]         # force the reference position
                print(f"    Constraint : (t: i, j) = ({t}: {i}, {j})")
                constraints.add((t, i, j))
                #print(f"    we break for t values")
                break

    
    #constraints.sort(key=lambda c: c[0])
    #print(f"constraints:\n  {constraints}")

    return constraints