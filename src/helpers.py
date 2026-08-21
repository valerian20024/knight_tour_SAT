def valid_pos(i, j, M, N) -> bool:
    """Checks that a position is inside the chessboard."""
    return 0 <= i < M and 0 <= j < N


def leave_one_out_subsets(items) -> list[list]:
    """Generates all subsets of the original_list that contain all but one element.
    
    @return A list of lists, where each inner list is a subset of size len(original_list) - 1.
    """

    # a subset is items from start to i[, and items from i + 1] to end.
    subsets = [items[:i] + items[i+1:] for i in range(len(items))]
    return subsets

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

def solutions_to_paths(solutions, M, N) -> tuple:
    """Converts solution matrices into path sequences and deduplicates them.
 
    A solution matrix has solution[i][j] = t ("cell (i,j) is visited at
    time t"). A path is the inverse view: path[t] = (i, j) ("at time t,
    the knight is at (i,j)").
 
    @param solutions: list of solution matrices.
    @param M: number of rows.
    @param N: number of columns.
    @return: a tuple of unique paths (each path is a tuple of (i, j)
             positions indexed by timestep).
    """
    T = M * N
    paths = set()
    for sol in solutions:
        path = [None] * T
        for i in range(M):
            for j in range(N):
                if sol[i][j] >= 0:
                    path[sol[i][j]] = (i, j)
        paths.add(tuple(path))
    return tuple(paths)
 