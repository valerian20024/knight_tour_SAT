# This function checks that a position is inside the chessboard
def valid_pos(i, j, M, N):
    return 0 <= i < M and 0 <= j < N
