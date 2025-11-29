# This function checks that a position is inside the chessboard
def valid_pos(i, j, M, N):
    return 0 <= i < M and 0 <= j < N

    """
    Generates all subsets of the original_list that contain all but one element.

    Returns:
        A list of lists, where each inner list is a subset of size len(original_list) - 1.
    """
def leave_one_out_subsets(items):
    subsets = [items[:i] + items[i+1:] for i in range(len(items))]
    return subsets


