class Board:
    """ An object to represent a 2-Dimensional rectangular board
    """

    def __init__(self, num_cols=10, num_rows=20, cell_item=None, grid=None):
        """ Create a Board instance that has num cols and num rows.
            The 2D board is represented with a single list, if the board looks like:
            
            col  col  col
             0   1    2
            -------------
            | 0 | 1 | 2 |  row 0
            ----+---+----
            | 3 | 4 | 5 |  row 1
            -------------
            
            Where num cols = 3, num rows = 2
            
            Then the underlying representation looks like:
            [0, 1, 2, 3, 4, 5]

        Parameters
        ----------
        num_cols (int, required):
            number of columns. Defaults to 10.
        
        num_rows (int, required):
            number of rows. Defaults to 20.
        
        cell_item (any, optional):
            create default items. Defaults to None.
        
        grid (list[any], optional): a list to create the underlying board representation.
                However len(grid) = num_cols * num_rows. Defaults to None.
        """
        assert num_cols is not None and num_rows is not None
        assert type(num_cols) == int and type(num_rows) == int
        assert num_cols >= 0 and num_rows >= 0
        self._num_rows = num_rows
        self._num_cols = num_cols
        if grid:
            assert num_cols * num_rows == len(grid)
            self._grid = grid[:]
        else:
            self._grid = [cell_item for _ in range(num_cols * num_rows)]



# ---------------------------------------------------------------------------- #
# --------------------------------- Required --------------------------------- #
# ---------------------------------------------------------------------------- #

    def get_col(self, x):
        """Get a copy of column x

        Parameters
        ----------
        x (int):
            column number

        Returns
        -------
        list[any]:
            a list copy of column x

        >>> board = Board(3, 2, grid=[7, 6, 3, 9, 5, 2])
        >>> print(board)
        =====
        7 6 3
        9 5 2
        =====
        >>> board.get_col(1)
        [6, 5]
        >>> board2 = Board(2, 2, grid=[1, 0, 4, 3])
        >>> print(board2)
        ===
        1 0
        4 3
        ===
        >>> board2.get_col(0)
        [1, 4]
        """
        copy = []
        for i in range(0, self._num_rows):
            copy.insert(i, self._grid[x + i*self._num_cols])
        return(copy)

    def get_item(self, x, y):
        """Get the item at coordinate (x, y)

        Parameters
        ----------
        x (int):
            column number
        y (int):
            row number

        Returns
        -------
        any:
            actual item

        >>> board = Board(3, 2, grid=[5, 4, 1, 3, 0, 6])
        >>> print(board)
        =====
        5 4 1
        3 0 6
        =====
        >>> [board.get_item(x, y) for y in range(2) for x in range(3)]
        [5, 4, 1, 3, 0, 6]
        >>> board2 = Board(4, 1, grid=[9, 2, 4, 1])
        >>> print(board2)
        =======
        9 2 4 1
        =======
        >>> [board2.get_item(x, y) for y in range(1) for x in range(4)]
        [9, 2, 4, 1]
        """
        return(self._grid[(y * self._num_cols) + x])

    def set_item(self, x, y, item):
        """Overwrite the item at (x, y)

        Parameters
        ----------
        x (int):
            column number
        y (int):
            row number
        item (any):
            new item

        >>> board = Board(3, 2, grid=[i for i in range(6)])
        >>> print(board)
        =====
        0 1 2
        3 4 5
        =====
        >>> board.set_item(0, 1, 30)
        >>> board.set_item(2, 0, 11)
        >>> print(board)
        =====
        0 1 11
        30 4 5
        =====
        """
        self._grid[(y * self._num_cols) + x] = item

    def insert_row_at(self, y, lst):
        """Insert lst as new row at row y. Increment num_rows by 1

        Parameters
        ----------
        y (int):
            row number
        lst (list[any]):
            list of row items
        >>> board = Board(3, 2, grid=list(range(6)))
        >>> print(board)
        =====
        0 1 2
        3 4 5
        =====
        >>> board.insert_row_at(1, [6, 7, 8])
        >>> print(board)
        =====
        0 1 2
        6 7 8
        3 4 5
        =====
        >>> board.get_num_rows()
        3
        """
        self._num_rows += 1 # DO NOT touch this line
        for i in range(0, len(lst)):
            self._grid.insert(y*self._num_cols+i, lst[i])

    def valid_coordinate(self, coordinate):
        """Check if coordinate (x, y) is within the board

        Parameters
        ----------
        coordinate (tuple(x, y)):
            an (x: int, y: int) coordinate

        Returns
        -------
        bool:
            if the coordinate is valid within *this* board

        >>> board = Board(3, 2, grid=list(range(6)))
        >>> print(board)
        =====
        0 1 2
        3 4 5
        =====
        >>> sum([board.valid_coordinate((x, y)) for x in range(3) for y in range(2)]) == 6
        True
        >>> board.valid_coordinate((2, 1))
        True
        >>> board.valid_coordinate((1, 1))
        True
        >>> board.valid_coordinate((0, 2))
        False
        >>> board.valid_coordinate((0, -1))
        False
        >>> board.valid_coordinate((-1, 0))
        False
        >>> board.valid_coordinate((3, 0))
        False
        """
        if coordinate[0] >= 0 and coordinate[1] >= 0:
            if coordinate[0] <= self._num_cols - 1:
                if coordinate[1] <= self._num_rows - 1:
                    return(True)
        return(False) 
        

# ---------------------------------------------------------------------------- #
# --------------------------- Helpers: Not Required -------------------------- #
# ---------------------------------------------------------------------------- #

    def get_row(self, y):
        """Get a copy of row y
        
        Parameters
        ----------
        y (int):
            row number

        Returns
        -------
        list[any]:
            A list copy of row y
        
        >>> board = Board(3, 2, grid=[i for i in range(6)])
        >>> print(board)
        =====
        0 1 2
        3 4 5
        =====
        >>> board.get_row(0)
        [0, 1, 2]
        >>> board.get_row(1)
        [3, 4, 5]
        """
        assert 0 <= y < self._num_rows, f'Invalid y: {y}'
        start_index = y * self._num_cols
        return self._grid[start_index : start_index + self._num_cols]

    def delete_row(self, y):
        """Delete row y and decremet num_rows count by 1

        Parameters
        ----------
        y (int):
            row number

        >>> board = Board(3, 3, grid=list(range(9)))
        >>> print(board)
        =====
        0 1 2
        3 4 5
        6 7 8
        =====
        >>> board.delete_row(1)
        >>> print(board)
        =====
        0 1 2
        6 7 8
        =====
        >>> board.get_num_rows()
        2
        """
        index_start = y * self._num_cols
        del self._grid[index_start : index_start + self._num_cols]
        self._num_rows -= 1

    def index_to_coordinate(self, index):
        """Convert an index to (x, y) coordinate

        Parameters
        ----------
        index (int): 
            index in underlying list representation

        Returns
        -------
        tuple[int, int]: 
            tuple coordinate

        >>> board = Board(3, 2, grid=[i for i in range(6)])
        >>> print(board)
        =====
        0 1 2
        3 4 5
        =====
        >>> board.index_to_coordinate(5)
        (2, 1)
        """
        assert 0 <= index < len(self._grid), f'Invalid index: {index}'
        return (index % self._num_cols, index // self._num_cols)

    def filter_coordinates(self, fn):
        """Extract coordinates of all item that satisfy fn and returns
            a list of these coordinates in tuples

        Parameters
        ----------
        fn (any -> bool): 
            a boolean function that operates on items of *this* board

        Returns
        -------
        list[tuple[int, int]]: 
            a list of tuple coordinates

        >>> board = Board(3, 3, grid=[i for i in range(9)])
        >>> board.filter_coordinates(lambda x: x % 2 == 1)
        [(1, 0), (0, 1), (2, 1), (1, 2)]
        """
        return [(i % self._num_cols, i // self._num_cols) \
                    for i, item in enumerate(self._grid) if fn(item)]
        
    def update_grid(self, new_grid):
        """ Overwrite existing underlying board with a new board
        """
        assert len(new_grid) == len(self._grid), 'unequal grid lengths'
        self._grid = new_grid

    def get_num_rows(self):
        return self._num_rows

    def get_num_cols(self):
        return self._num_cols

    def get_grid(self):
        """ Returns a COPY of the underlying grid
        """
        return self._grid[:]

    def __contains__(self, item):
        """ Returns True if item is in this Board, False otherwise

        >>> board = Board(2, 3, grid=list(range(6)))
        >>> 5 in board
        True
        >>> 6 in board
        False
        """
        return self._grid.__contains__(item)

    def __getitem__(self, key):
        """ Using bracket notation e.g. [, ] and pass in either a number
        or a coordinate.

        >>> board = Board(3, 5, '*')
        >>> board[4] == board[(1, 1)] == board[[1, 1]] == '*'
        True
        """
        if isinstance(key, int):
            return self._grid[key]
        return self.get_item(key[0], key[1])

    def __setitem__(self, key, value):
        """ Using bracket notation e.g. [, ] and pass in either a number
        or a coordinate.

        >>> board = Board(3, 5, '*')
        >>> board[7] = 70
        >>> board.get_item(1, 2)
        70
        """
        if isinstance(key, int):
            self._grid[key] = value
        else:
            self.set_item(key[0], key[1], value)

    def __iter__(self):
        """ Iterate through the underlying grid in row major order

        >>> board = Board(2, 2, grid=list(range(4)))
        >>> list(board)
        [0, 1, 2, 3]
        """
        return self._grid.__iter__()

    def __reversed__(self):
        """ Iterate through the underlying grid in reverse row major order
            Use the built-in reversed() call.

        >>> board = Board(2, 2, grid=list(range(4)))
        >>> list(reversed(board))
        [3, 2, 1, 0]
        """
        return self._grid.__reversed__()

    def __len__(self):
        """ Returns the total number of elements

        >>> board = Board(3, 3, grid=list(range(9)))
        >>> len(board)
        9
        """
        return self._grid.__len__()

    def __repr__(self):
        return f'<Board num_cols: {self._num_cols} num_rows: {self._num_rows}>'

    def __str__(self):
        """ Print out the board items in a grid

        >>> board = Board(2, 3, grid=list(range(6)))
        >>> print(board)
        ===
        0 1
        2 3
        4 5
        ===
        """
        s = '=' * (self._num_cols * 2 - 1) + '\n'
        for i, val in enumerate(self._grid):
            s += str(val)
            if (i + 1) % self._num_cols != 0:
                s += ' '
            if (i + 1) % self._num_cols == 0:
                s += '\n'
        s += '=' * (self._num_cols * 2 - 1)
        return s
