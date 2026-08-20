
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