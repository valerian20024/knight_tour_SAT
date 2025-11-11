from helpers import valid_pos

# Constant representing the knights moves offsets
KNIGHT_MOVES = [(-2, -1), (-2, 1),
                (-1, -2), (-1, 2),
                (1, -2), (1, 2),
                (2, -1), (2, 1)]

"""
This function adds constraints to the SAT solver that enforce
the possible moves of the knight. If a position was occupied
at a previous timestep, then all the positions that can be
reach by enumerating the knight moves can be occupied at the
next time step.

@param solver: The solver instance to add constraints to.
@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param T: The number of timesteps.
@param var: A dictionary containing all the variables.
"""
def add_legal_moves_constraints(solver, M, N, T, var):
    for t in range(T - 1):
        for i in range(M):
            for j in range(N):
                v = var[(i, j, t)]
                #print(f"¬{v} ({i}, {j}| {t})")
                move_lits = []
                for di, dj in KNIGHT_MOVES:
                    ni, nj = i + di, j + dj
                    # Check move leads inside the chessboard
                    if valid_pos(ni, nj, M, N):
                        move_lits.append(var[(ni, nj, t + 1)])
                        #print(f"Appending ({ni}, {nj}| {t + 1})")
                if move_lits:
                    # v => legal moves <=> not v and (ORing legal_moves)
                    #print(f"move_lits ", move_lits)
                    solver.add_clause([-v] + move_lits)
    return solver, var


"""
This function adds constraints to the SAT solver that enforce
only one cell to be visited at each timestep, and a given cell
is visited at only one timestep.
This function is naive and will compute a quadratic number
of clauses to exlude two cells from being visited at the same
time step.

@param solver: The solver instance to add constraints to.
@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param T: The number of timesteps.
@param var: A dictionary containing all the variables.
"""
def add_cell_constraints_naive(solver, M, N, T, var):
    # Each timestep visits a single cell
    for t in range(T):
        # Any cell in a snapshot can be visited at each time step
        lits = [var[(i, j, t)] for i in range(M) for j in range(N)]
        solver.add_clause(lits)
        # Two cells cannot be visited in a same snapshot
        # Take all different combinations of cells of a given snapshot
        for first_cell in range(len(lits)):
            for second_cell in range(first_cell + 1, len(lits)):
                # not(A and B) <=> (not A or not b)
                solver.add_clause([-lits[first_cell], -lits[second_cell]])
    return solver, var

"""
This function adds constraints to the SAT solver that enforce
only one cell to be visited at each timestep, and a given cell
is visited at only one timestep.
This function is naive and will compute a quadratic number
of clauses to exlude two cells from being visited at the same
time step.

@param solver: The solver instance to add constraints to.
@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param T: The number of timesteps.
@param var: A dictionary containing all the variables.
"""
def add_time_constraints_naive(solver, M, N, T, var):
    # A given cell is visited at exactly one time step
    for i in range(M):
        for j in range(N):
            # There must be at least one timestep for visiting the cell
            lits = [var[(i, j, t)] for t in range(T)]
            solver.add_clause(lits)
            # Several timesteps cannot visit a same cell
            for first_time in range(T):
                for second_time in range(first_time + 1, T):
                    solver.add_clause(
                        [-var[(i, j, first_time)], -var[(i, j, second_time)]])
    
    return solver, var


"""
This function adds constraints to the SAT solver that enforce
only one cell to be visited at each timestep.
This function is more efficient as it uses sequential counter
encoding, which adds a set of clauses linear w.r.t. the size
of the problem.

@param solver: The solver instance to add constraints to.
@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param T: The number of timesteps.
@param var: A dictionary containing all the variables.
"""
def add_cell_constraints_sequential_counter(solver, M, N, T, var, var_id):
    #print(f"add_cell_constraints_sequential_counter({solver}, {M}, {N}, {T}, {var}, {var_id}):")
    for t in range(T):
        # List of literals for all cells at time t
        lits = [var[(i, j, t)] for i in range(M) for j in range(N)]
        #print(f"lits", lits)

        # At least one cell is visited
        #solver.add_clause(lits)

        n = len(lits)

        # Case 1: 1x1 board (n = 1)
        if n == 1:
            solver.add_clause([lits[0]])  # The single cell must be visited
            continue
        
        # Add clause: at least one cell is visited
        solver.add_clause(lits)
        
        # Case 2: 1x2 or 2x1 board (n = 2)
        if n == 2:
            # Exactly one: (X_0 ∨ X_1) ∧ (¬X_0 ∨ ¬X_1)
            solver.add_clause([-lits[0], -lits[1]])  # At most one
            continue

        aux = []
        for k in range(n - 1):
            var[('aux_1', k, t)] = var_id
            aux.append(var_id)
            var_id += 1
        
        solver.add_clause([-lits[0], aux[0]])               # First: ¬X_0 ∨ a_0
        for l in range(1, n - 1):
            solver.add_clause([-lits[l], aux[l]])           # ¬X_i ∨ a_i
            solver.add_clause([-aux[l - 1], aux[l]])        # ¬a_{i-1} ∨ a_i
            solver.add_clause([-lits[l], -aux[l - 1]])      # ¬X_i ∨ ¬a_{i-1}
        solver.add_clause([-lits[-1], -aux[-2]])            # Last: ¬X_{n-1} ∨ ¬a_{n-2}
        
    return solver, var, var_id

"""
This function adds constraints to the SAT solver that enforce
cells are visited only at one timestep.
This function is more efficient as it uses sequential counter
encoding, which adds a set of clauses linear w.r.t. the size
of the problem.

@param solver: The solver instance to add constraints to.
@param M: The number of rows in the chessboard.
@param N: The number of columns in the chessboard.
@param T: The number of timesteps.
@param var: A dictionary containing all the variables.
"""
def add_time_constraints_sequential_counter(solver, M, N, T, var, var_id):
    for i in range(M):
        for j in range(N):
            # List of literals for cell (i, j) across all time steps
            lits = [var[(i, j, t)] for t in range(T)]
            n = len(lits)
            
            # Case 1: T = 1 (n = 1)
            if n == 1:
                solver.add_clause([lits[0]])  # Cell must be visited at t = 0
                continue
            
            # Add clause: cell is visited at least once
            solver.add_clause(lits)
            
            # Case 2: T = 2 (n = 2)
            if n == 2:
                # Exactly one: (X_0 ∨ X_1) ∧ (¬X_0 ∨ ¬X_1)
                solver.add_clause([-lits[0], -lits[1]])  # At most one
                continue

            aux = []
            for k in range(n - 1):
                var[('aux_2', k, i, j)] = var_id
                aux.append(var_id)
                var_id += 1

            #print(f"aux = {aux}")

            solver.add_clause([-lits[0], aux[0]])               # First: ¬X_0 ∨ a_0
            for l in range(1, n - 1):
                solver.add_clause([-lits[l], aux[l]])           # ¬X_i ∨ a_i
                solver.add_clause([-aux[l - 1], aux[l]])        # ¬a_{i-1} ∨ a_i
                solver.add_clause([-lits[l], -aux[l - 1]])      # ¬X_i ∨ ¬a_{i-1}
            solver.add_clause([-lits[-1], -aux[-2]])            # Last: ¬X_{n-1} ∨ ¬a_{n-2}
            
    return solver, var, var_id
