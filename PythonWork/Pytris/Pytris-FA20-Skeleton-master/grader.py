from sys import argv

try:
    from models import Holder
    from models import Pytromino
    from board import Board
    from colors import Color
except ImportError as err:
    print(err)
    exit(1)

try:
    TESTS = {
        '1': Holder.__init__,
        
        '2A': Board.get_col,
        '2B': Board.get_item,
        '2C': Board.set_item,
        '2D': Board.insert_row_at,
        '2E': Board.valid_coordinate,
        
        '3A': Pytromino.rotate_block_90_cw,
        '3B': Pytromino.filter_blocks_pos,
        '3C': Pytromino.shift_down_fn,
        '3D': Pytromino.shift_left_fn,
        '3E': Pytromino.shift_right_fn,
        '3F': Pytromino.validated_apply,
    }
    from doctest import run_docstring_examples
    
    if len(argv) < 2:
        for obj in TESTS.values():
            run_docstring_examples(obj, globals())
        exit(0)

    t = argv[1]
    if t in TESTS:
        obj = TESTS[t]
        run_docstring_examples(obj, globals())
    else:
        print(f'Unrecognized Question: {t}')
        exit(1)
except Exception as err:
    print(err)
    exit(1)
