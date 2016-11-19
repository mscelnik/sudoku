# /usr/bin/python3
""" Sudoku solver using only standard Python (no 3rd party libraries).

# A Sudoku grid contains 9 * 9 = 81 cells, numbered thusly:
+-----------+----------+----------+
|  0  1  2  |  3  4  5 |  6  7  8 |
|  9 10 11  | 12 13 14 | 15 16 17 |
| 18 19 20  | 21 22 23 | 24 25 26 |
+-----------+----------+----------+
| 27 28 29  | 30 31 32 | 33 34 35 |
| 36 37 38  | 39 40 41 | 42 43 44 |
| 45 46 47  | 48 49 50 | 51 52 53 |
+-----------+----------+----------+
| 54 55 56  | 57 58 59 | 60 61 62 |
| 63 64 65  | 66 67 68 | 69 70 71 |
| 72 73 74  | 75 76 77 | 78 79 80 |
+-----------+----------+----------+
"""

import random

__author__ = "Matthew Celnik"
__copyright__ = "Matthew Celnik"
__licence__ = "All rights reserved"
__maintainer__ = "Matthew Celnik"
__email__ = "matthew@celnik.co.uk"


# For debugging, provide a known seed.  This ensures all results are the same.
random.seed(2)


def create_grid(random_fill=0):
    """ Constructs a 9x9 grid.  Use zeros to denote an unfilled square.

    Args:
        random_fill = Number of grid squares to fill in.

    Returns:
        A  list of lists filled with zeros.
    """
    import random

    grid = [[0] * 9 for i in range(9)]

    n = 0
    while n < random_fill:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        value = random.randint(0, 8)
        if set_cell(i, j, grid, value):
            print('Set', i, j, value)
            n += 1

    return grid


def set_cell(i, j, grid, value):
    """ Attempts to set grid cell i value, satisfying Sudoku rules.

    The cell can only be set if the value is not present in any of:
        - The cell row,
        - The cell column, or
        - The cell grid 3x3 square.

    The value must be in the range 1-9.

    Args:
        i = Row index (0-8), see module docstring.
        j = Column index (0-8), see module docstring.
        grid = The grid from which to get the row.
        value = Cell value (1-9)

    Returns:
        True if setting was successful, otherwise False.
    """
    if 1 <= value <= 9:
        row = get_row(i, grid)
        col = get_col(j, grid)
        square = get_square(i, j, grid)
        # Check if the value is already in the row, column or square.
        if value in row:
            # print('Already in row: {}'.format(row))
            return False
        elif value in col:
            # print('Already in column: {}'.format(col))
            return False
        elif value in square:
            # print('Already in square: {}'.format(square))
            return False
        else:
            # This value can be set as it does not invalidate the grid.
            grid[i][j] = value
            return True
    else:
        # Value is out of range.
        return False


def get_row(i, grid):
    """ Gets row for cell i from a grid.

    Args:
        i = Row index (0-8), see module docstring.
        grid = The grid from which to get the row.

    Returns:
        The 9 cell values making the row as a list.
    """
    # Calculate row index y from the cell index using integer division.
    return grid[i][:]


def get_col(j, grid):
    """ Gets column for cell i from a grid.

    Args:
        j = Column index (0-8), see module docstring.
        grid = The grid from which to get the column.

    Returns:
        The 9 cell values making the column as a list.
    """
    # Calculate the column index x from the cell index.
    return [grid[i][j] for i in range(9)]


def get_square(i, j, grid):
    """ Gets 3x3 square which contains cell i from a grid.

    Args:
        i = Row index (0-8), see module docstring.
        j = Column index (0-8), see module docstring.
        grid = The grid from which to get the square.

    Returns:
        The square values as a 1D list, with indices:
            0  1  2
            3  4  5
            6  7  8
    """
    # Calculate the square indices (on a 3x3 grid of squares).
    sqx = j // 3
    sqy = i // 3
    # Calculate x, y coordinate of the first cell in the square.
    x1 = sqx * 3
    y1 = sqy * 3
    # Use a double loop to return the values in the 3x3 grid square, starting at
    # (x1, y1).  j loops over the ys, and k loops over the xs.
    return [grid[y][x] for y in range(y1, y1 + 3) for x in range(x1, x1 + 3)]


def print_grid(grid, zero_replacement='?'):
    """ Displays a grid on the console.
    """
    sep_style = '+-------+-------+-------+'
    row_style = '| {:d} {:d} {:d} | {:d} {:d} {:d} | {:d} {:d} {:d} |'

    print(sep_style)
    for i, row in enumerate(grid):
        # Unpack the 9 row values and supply to the row_style.format function.
        row_string = row_style.format(*row)
        # The grid contains zero for unknown values.  convert them for display
        # on the console using the replace function.
        print(row_string.replace('0', zero_replacement))
        # Print a separator after every 3rd row.
        if i % 3 == 2:
            print(sep_style)


def print_flattened_grid(grid, zero_replacement='?'):
    """ Prints a grid which has been flattened into a 1D list of 89 values.
    """
    grid2d = [[grid[(j * 9) + i]] for j in range(9) for i in range(9)]
    print_grid(grid2d, zero_replacement=zero_replacement)


def brute_solve(grid):
    """ Attempts to solves the grid by brute force.
    """
    import copy
    # Make a copy of the grid to fill.
    solution = copy.deepcopy(grid)
    print_grid(grid)
    print_grid(solution)

    first_blank = 0
    x = 0
    iteration = 0
    while first_blank <= x < 81:
        iteration += 1
        # print('Looking at cell {} on iteration {}'.format(x, iteration))
        i = x // 9
        j = x % 9
        print (x, i, j, grid[i][j], solution[i][j], iteration)
        if grid[i][j] == 0:
            # Search all values, from the current solution value up to 9.  We
            # don't use zero here, as we might be resetting a solution value
            # already deemed to be invalid
            for value in range(solution[i][j] + 1, 10):
                # set_cell returns True only if the value is valid, given the
                # current grid status.
                # print('Trying to set cell {} = {}, iteration {}'.format(
                    # x, value, iteration))
                if set_cell(i, j, solution, value):
                    # If the cell filled successfully, go to the next one.
                    # print('Set cell {} = {}.'.format(x, value))
                    x += 1
                    break
            else:
                # Could not set this cell, so clear it and revert to previous
                # cell.
                solution[i][j] = 0
                x -= 1
                # print ('Failed, x now = {}'.format(x))
        else:
            if x == first_blank:
                first_blank += 1
            x += 1

    return solution


def smarter_solve(grid):
    """ Attempts to solves the grid by brute force, but checking possibilities.

    The brute force algorithm iterates through all possibilities to fill the
    blank squares.  This algorithm also eliminates impossible values given the
    initial grid, which reduces the number of iterations required.

    Also, as the brute force approach assigns equal probability to all values,
    the possible values are shuffled (there is no logical reason to start at 1).
    """
    import copy
    # Make a copy of the grid to fill.
    solution = copy.deepcopy(grid)
    print_grid(grid)
    print_grid(solution)

    # Make a list of all empty cell indices.
    empty_indices = [x for x in range(81) if grid[x // 9][x % 9] == 0]
    N = len(empty_indices)
    print(N, empty_indices)

    # Make a list of all empty cell possibilities.
    all_possibilities = [list(range(1, 10)) for ix in range(N)]
    loop_possibilities = copy.deepcopy(all_possibilities)
    print(all_possibilities)

    # Loop through all the empty cells, testing each combination in turn.
    ix = 0
    iteration = 0
    while 0 <= ix < N:
        iteration += 1

        # Get the cell index and convert to the 2D grid coordinates (i, j).
        x = empty_indices[ix]
        i = x // 9
        j = x % 9

        # Save a copy of the list of possibilities for this cell.
        # possibilities = all_possibilities[ix][:]

        # Search all values, from the current solution value up to 9.  We
        # don't use zero here, as we might be resetting a solution value
        # already deemed to be invalid.
        while len(loop_possibilities[ix]) > 0:
            # set_cell returns True only if the value is valid, given the
            # current grid status.
            value = loop_possibilities[ix].pop()
            # print("Checking", x, i, j, value)
            if set_cell(i, j, solution, value):
                # If the cell filled successfully, go to the next one.
                ix += 1
                break
        else:
            # Could not set this cell, so clear it and revert to previous
            # cell.  Also reset its possible values for the next iteration.
            solution[i][j] = 0
            loop_possibilities[ix] = all_possibilities[ix][:]
            ix -= 1

    if ix < 0:
        print('No solution found!')
    else:
        print('Solution found!')
        print_grid(solution)

    return solution


if __name__ == '__main__':
    mygrid = create_grid(random_fill=5)
    print_grid(mygrid)
    print('Row (cell=40)', get_row(5, mygrid))
    print('Column (cell=40)', get_col(5, mygrid))
    print('Square (cell=40)', get_square(5, 5, mygrid))

    solved = brute_solve(mygrid)
    print_grid(mygrid)
    print_grid(solved)
