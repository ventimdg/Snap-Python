from enum import Enum, auto
from colors import Color


class Pytromino:
    """An object to represent a block of squares
    """

    class Types(Enum):
        I = auto()
        O = auto()
        L = auto()
        S = auto()
        T = auto()
        J = auto()
        Z = auto()

    def __init__(self, block_rel_pos, color, pytromino_type, center_rot=(0, 0)):
        """ Create a new Pytromino instance. A pytromino consists of a list of 
            coordinates for the center points of blocks. One of these blocks should
            have coordinate (0, 0), this is the reference block. All other blocks'
            coordinates are relatively the reference block's coordinate. Additionally,
            the center of rotation can be any point that's relative to center of reference;
            it does not have to be (0, 0).

        Parameters
        ----------
        block_rel_pos (list[tuple[int, int]]): A list of tuples (x, y) that 
            represent a block's relative position to the center

        color (tuple[int, int, int]): RGB colors of this Pytromino
        
        pytromino_type (Pytromino.Types): Type of Pytromino
        
        center_rot (tuple[number, number], optional): Center of rotation coordinate 
            relative to the (0, 0) reference block. Defaults to (0, 0).
        """
        assert isinstance(pytromino_type, Pytromino.Types)
        assert type(color) == tuple
        self._blocks_pos = block_rel_pos
        self._color = color
        self._type = pytromino_type
        self._center_rot = center_rot
        self._placed = False
        

# ---------------------------------------------------------------------------- #
# ----------------------------- Required Methods ----------------------------- #
# ---------------------------------------------------------------------------- #        
        
    def rotate_block_90_cw(self, pos):
        """Rotate pos e.g. (x, y) by 90 degree clockwise

        Parameters
        ----------
        pos (tuple[int, int]):
            A tuple coordinate (x, y)

        Returns
        -------
        tuple[int, int]:
            A new tuple coordinate after rotating input tuple coordinate
            90 degrees clockwise

        >>> T = Pytromino([(0, 0), (0, -1), (-1, 0), (1, 0)], Color.PURPLE.value, Pytromino.Types.T) # type T
        >>> T.rotate_block_90_cw((-1, 0))
        (0, -1)
        >>> T.rotate_block_90_cw((0, 0))
        (0, 0)
        >>> T.rotate_block_90_cw((1, 0))
        (0, 1)
        """
        x = self._center_rot[1] - pos[1] + self._center_rot[0]
        y = pos[0] - self._center_rot[0] + self._center_rot[1]
        newpos = (x, y)
        return(newpos)

        # Hint: 
        # The new x value is: center_rot.y - pos.y + center_rot.x
        # The new y value is: pos.x - center_rot.x + center_rot.y
        # You need to translate the above equations to code and 
        # return the right solution.

    def filter_blocks_pos(self, fn):
        """Use a function to filter out blocks positions

        Parameters
        ----------
        fn ((tuple[int, int]) -> bool): 
            A function that takes in a tuple coordinate and returns boolean

        Returns
        -------
        list[tuple[int, int]]:
            A list of tuple coordinates that satisfy fn
            
        >>> S = Pytromino([(0, 0), (-1, 0), (0, -1), (1, -1)], Color.GREEN.value, Pytromino.Types.S) # type S
        >>> f = lambda pos: pos[0] == 0
        >>> S.filter_blocks_pos(f)
        [(0, 0), (0, -1)]
        >>> S.filter_blocks_pos(lambda pos: pos[0] * pos[1] < 0)
        [(1, -1)]
        """
        return([x for x in self._blocks_pos if fn(x) == True])


    @staticmethod
    def shift_down_fn(steps):
        """Create a function that will shift *this* pytromino 
            down number of steps

        Parameters
        ----------
        steps (int):
            number of steps to shift down

        Returns
        -------
        tuple[int, int] -> tuple[int, int]:
            A function that takes in a tuple coordinate and returns 
            a new tuple coordinate

        >>> f = Pytromino.shift_down_fn(1)
        >>> f((0, 0))
        (0, 1)
        >>> m = Pytromino.shift_down_fn(3)
        >>> m((0, 0))
        (0, 3)
        """
        return(lambda x: (x[0], x[1] + steps))


    @staticmethod
    def shift_left_fn(steps):
        """Create a function that will shift *this* pytromino 
            left number of steps

        Parameters
        ----------
        steps (int):
            number of steps to shift left

        Returns
        -------
        tuple[int, int] -> tuple[int, int]:
            A function that takes in a tuple coordinate and returns 
            a new tuple coordinate

        >>> f = Pytromino.shift_left_fn(1)
        >>> f((0, 0))
        (-1, 0)
        >>> m = Pytromino.shift_left_fn(3)
        >>> m((0, 0))
        (-3, 0)
        """
        return(lambda x: (x[0] - steps, x[1]))

    @staticmethod
    def shift_right_fn(steps):
        """Create a function that will shift *this* pytromino 
            right number of steps

        Parameters
        ----------
        steps (int):
            number of steps to shift right

        Returns
        -------
        tuple[int, int] -> tuple[int, int]:
            A function that takes in a tuple coordinate and returns 
            a new tuple coordinate

        >>> f = Pytromino.shift_right_fn(1)
        >>> f((0, 0))
        (1, 0)
        >>> m = Pytromino.shift_right_fn(3)
        >>> m((0, 0))
        (3, 0)
        """
        return(lambda x: (x[0] + steps, x[1]))

    def validated_apply(self, fn, is_rotation=False, validator=lambda pos: True):
        """ Apply fn on all block coordinates of the pytromino, and check the 
            validity of each resulting coordinate using a validator function.
            A side effect will only occur when ALL resulting coordinates pass
            the validator check. Else, no effect will occur and False will be 
            returned. If is_rotation, fn is not applied to self._center_rot.

        Parameters
        ----------
        fn ((tuple[int, int])) -> tuple[int, int]):
            A function that takes in a tuple of 2 int, then does some 
            transformation, and return a new tuple of 2 int.

        is_rotation (bool):
            If fn is a rotational transfermation, self.center_rot will not
            be applied with fn

        validator ((tuple[int, int]) -> bool):
            A function that takes in the result of fn, a tuple of 2 int, 
            does some check, then return a boolean of the result. By default,
            there is no meaningful check.

        Returns
        -------
        bool
            True when fn has been applied to ALL blocks, False for NONE

        >>> T = Pytromino([(0, 0), (0, -1), (-1, 0), (1, 0)], Color.PURPLE.value, Pytromino.Types.T) # type T
        >>> T # Checkout the __repr__(self) below if you're curious
        <Pytromino [(0, 0), (0, -1), (-1, 0), (1, 0)], (146, 44, 140), Types.T, (0, 0) >
        >>> right_shift_1 = Pytromino.shift_right_fn(1)
        >>> positive_x = lambda pos: pos[0] > 0
        >>> T.validated_apply(right_shift_1, False, positive_x)
        False
        >>> T # No change!
        <Pytromino [(0, 0), (0, -1), (-1, 0), (1, 0)], (146, 44, 140), Types.T, (0, 0) >
        >>> always_true = lambda pos: True
        >>> T.validated_apply(right_shift_1, False, always_true)
        True
        >>> T # Notice the change in center_pos ------------------------------ below
        <Pytromino [(1, 0), (1, -1), (0, 0), (2, 0)], (146, 44, 140), Types.T, (1, 0) >
        >>> I = Pytromino([(0, 0), (-1, 0), (1, 0), (2, 0)], Color.CYAN.value, Pytromino.Types.I, center_rot=(0.5, 0.5)) #Type I
        >>> I
        <Pytromino [(0, 0), (-1, 0), (1, 0), (2, 0)], (43, 172, 226), Types.I, (0.5, 0.5) >
        >>> I.validated_apply(I.rotate_block_90_cw, True, always_true) # This is a rotation
        True
        >>> I # Notice center_pos is NOT changed --------------------------------------------- below
        <Pytromino [(1.0, 0.0), (1.0, -1.0), (1.0, 1.0), (1.0, 2.0)], (43, 172, 226), Types.I, (0.5, 0.5) >
        """
        y = [fn(x) for x in self._blocks_pos]
        for i in range(0, len(self._blocks_pos)):
            if validator(y[i]) == False:
                return(False)
        self._blocks_pos = y
        if is_rotation == False:
            self._center_rot = fn(self._center_rot)
        for i in range(0, len(self._blocks_pos)):
            if validator(self._blocks_pos[i]) == False:
                return(False)
        else:
            return(True)




# ---------------------------------------------------------------------------- #
# --------------------------- Helpers: Not Required -------------------------- #
# ---------------------------------------------------------------------------- #

    def get_unique_rows(self):
        """ Returns a list of rows spanned by this pytromino
        """
        s = set()
        for pos in self._blocks_pos:
            s.add(pos[1])
        return list(s)

    def place_at(self, coordinate):
        """ Place this Pytromino at coordinate, can only be called ONCE
            in an instance's lifetime

        coordinate: (x, y) coordinate
        """
        if not self._placed:
            self.validated_apply(
                lambda pos: (
                    pos[0] + coordinate[0], 
                    pos[1] + coordinate[1]
                ),
                False
            )
            self._placed = True

    def is_placed(self):
        return self._placed

    def get_blocks_pos(self):
        """ Returns a COPY of blocks_pos
        """
        return self._blocks_pos[:]

    def get_color(self):
        """ Returns the color of the Pytromino
        """
        return self._color

    def get_type(self):
        return self._type

    def __repr__(self):
        return f"<Pytromino {self._blocks_pos}, {self._color}, {self._type}, {self._center_rot} >"

def pytromino_factory(pytromino_type):
    if pytromino_type == Pytromino.Types.I: # cyan
        return Pytromino([(0, 0), (-1, 0), (1, 0), (2, 0)],
                    Color.CYAN.value,
                    pytromino_type,
                    center_rot=(0.5, 0.5))
    elif pytromino_type == Pytromino.Types.O: # yellow
        return Pytromino([(0, 0), (0, -1), (1, -1), (1, 0)],
                    Color.YELLOW.value,
                    pytromino_type,
                    center_rot=(0.5, -0.5))
    elif pytromino_type == Pytromino.Types.L: # orange
        return Pytromino([(0, 0), (-1, 0), (1, 0), (1, -1)],
                    Color.ORANGE.value,
                    pytromino_type)
    elif pytromino_type == Pytromino.Types.S: # green
        return Pytromino([(0, 0), (-1, 0), (0, -1), (1, -1)],
                    Color.GREEN.value,
                    pytromino_type)
    elif pytromino_type == Pytromino.Types.T: # purple
        return Pytromino([(0, 0), (0, -1), (-1, 0), (1, 0)],
                    Color.PURPLE.value,
                    pytromino_type)
    elif pytromino_type == Pytromino.Types.J: # blue
        return Pytromino([(0, 0), (-1, -1), (-1, 0), (1, 0)],
                    Color.BLUE.value,
                    pytromino_type)
    elif pytromino_type == Pytromino.Types.Z: # red
        return Pytromino([(0, 0), (0, -1), (-1, -1), (1, 0)],
                    Color.RED.value,
                    pytromino_type)
    else:
        raise ValueError(f'Unknown block type: "{pytromino_type}"')


class Holder:
    """An object that can hold 1 item at a time,
        when closed, the item can not be stored or replaced
    """

    def __init__(self):
        """Create an instance of Holder
        
        >>> holder = Holder()
        >>> holder.is_open()
        True
        >>> holder.store(1)
        >>> holder.get_item()
        1
        >>> holder.close()
        >>> holder.get_item()
        1
        >>> holder.is_open()
        False
        >>> holder.open()
        >>> holder.is_open()
        True
        """
        self._item = None
        self._can_store = True

# ---------------------------------------------------------------------------- #
# --------------------------------- Required --------------------------------- #
# ---------------------------------------------------------------------------- #

    def store(self, item):
        """hold an item, or replace existing item.

        Parameters
        ----------
        item (any):
            the item to hold
        """
        assert self._can_store, "holder is closed"
        self._item = item 

    def open(self):
        """Open *this* holder to be able to store/replace item
        """
        self._can_store = True

    def close(self):
        """Close *this* holder so that no new item can be stored,
            or the existing item cannot be replaced.
        """
        self._can_store = False

    def get_item(self):
        """Get the item currently being held,
            regardless whether the holder is closed

        Returns
        -------
        any: 
            the item currently being held
        """
        return(self._item)

    def is_open(self):
        """Check if *this* holder is currently open so that it can 
            store item, or replace existing item.

        Returns
        -------
        bool: 
            True if the holder can accept store/replace item,
            False otherwise
        """
        return(self._can_store)
