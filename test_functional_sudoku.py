""" Unit tests for the Sudoku solver.
"""

import unittest as ut
import sudoku

__author__ = "Matthew Celnik"
__copyright__ = "Matthew Celnik"
__licence__ = "All rights reserved"
__maintainer__ = "Matthew Celnik"
__email__ = "matthew@celnik.co.uk"


class TestSet(ut.TestCase):
    """ Unit tests for the set_cell function.
    """

    def setUp(self):
        self.grid = sudoku.create_grid()

    def test_row_clash(self):
        """ Does not set cell when the same number is in the row already.
        """
        self.grid[1][6] = 7
        self.assertFalse(sudoku.set_cell(1, 2, self.grid, 7))

    def test_col_clash(self):
        """ Does not set cell when the same number is in the column already.
        """
        self.grid[1][7] = 8
        sudoku.print_grid(self.grid)
        print(sudoku.get_square(2, 8, self.grid))
        self.assertFalse(sudoku.set_cell(2, 8, self.grid, 8))

    def test_guardian_20161112(self):
        """ Guardian classic on 12 November 2016.
        """
        self.grid[0] = [0, 2, 0, 0, 0, 0, 0, 7, 0]
        self.grid[1] = [0, 0, 8, 0, 7, 0, 5, 0, 0]
        self.grid[2] = [3, 0, 0, 9, 0, 4, 0, 0, 8]

        self.grid[3] = [6, 0, 0, 5, 0, 8, 0, 0, 3]
        self.grid[4] = [0, 0, 1, 7, 0, 3, 9, 0, 0]
        self.grid[5] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.grid[6] = [0, 4, 3, 6, 2, 9, 7, 8, 0]
        self.grid[7] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.grid[8] = [0, 8, 0, 0, 1, 0, 0, 4, 0]
        solution = sudoku.smarter_solve(self.grid)
        sudoku.print_grid(solution)
        self.fail()
