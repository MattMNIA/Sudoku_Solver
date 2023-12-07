def solve(bd):
    """
    Solves a sudoku board using backtracking
    :param bd: 2d list of ints
    :return: solution
    """
    empty_cell = empty(bd)
    if empty_cell:
        row, col = empty_cell
    else:
        return True
    for i in range(1, 10):
        if valid(bd, (row, col), i):
            bd[row][col] = i

            if (solve(bd)):
                return True

            bd[row][col] = 0

    return False


def valid(bd, pos, num):
    """
    Checks if the move is valid
    :param bo: 2d list of ints
    :param pos: position on board (row,col)
    :param num: attempted input
    :return: True or Fals
    """
    # Check row
    for i in range(0, len(bd)):
        if bd[pos[0]][i] == num and pos[1] != i:
            return False
    # Check col
    for i in range(0, len(bd)):
        if bd[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bd[i, j] == num and (i, j) != pos:
                return False
    return True


def empty(bd):
    """
    finds empty cell in board
    :param bo: 2d list of ints
    :return: (int, int) row, col
    """
    for i in range(len(bd)):
        for j in range(len(bd[i])):
            if bd[i][j] == 0:
                return (i, j)

    return None
