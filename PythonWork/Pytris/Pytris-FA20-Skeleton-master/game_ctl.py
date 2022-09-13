from models import Pytromino, Holder, pytromino_factory
from pygame.locals import *
from random import seed, choice
from collections import deque
# To be deleted
from board import Board
from view import PytrisViewManager
class PytrisController:

    def __init__(self, board : Board, gui : PytrisViewManager, max_fps=60, a=None):
        """
        Parameters
        ----------
        board : Board
            An initialized Board object

        gui : PytrisViewManager
            An initialized PytrisViewManager object

        max_fps : int
            Upper limit on in game FPS. Default 30
        """
        self._board = board
        self._gui = gui
        self._fps = max_fps

        self._cur_pytromino = None
        self._pytromino_types = list(Pytromino.Types)
        self._pytro_start_coord = (4, 0)

        self._num_cols = board.get_num_cols()
        self._num_rows = board.get_num_rows()
        self._num_nextup = gui.get_num_nextup()
        self._pyg = gui.get_pygame()
        self._holder = Holder()
        self._empty_cell_color = self._gui.get_rect_color()
        # Seed PRNG before creating nextup
        seed(a)
        self._nextup = deque(
            [self.get_random_pytromino_t() for _ in range(self._num_nextup)],
            maxlen=self._num_nextup
        )
        # Initialize FPS clock
        self._fps_clock = self._pyg.time.Clock()
        # Blocking none essential events from interfering
        self._pyg.event.set_blocked(None) # block everything first
        self._pyg.event.set_allowed([QUIT, KEYDOWN]) # then whitelist

        self._start_speed = 1 # 1 row / sec
        self._speed_incr = 0.1 # + 0.1 row / sec
        self._score = 0
        self._game_over = False
        self._level = 1

# ============================================================================ #
# ================================= Main Menu ================================ #
# ============================================================================ #

    def show_main_menu(self):
        run = True
        self._gui.init_window()
        self._gui.draw_text_center("PRESS ANY KEY TO START")
        self._gui.render()
        while run:
            for event in self._pyg.event.get():
                if event.type == QUIT:
                    run = False
                    break
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                        break
                    self.start_game()
                    self._gui.draw_text_center("GAME OVER")
                    self._gui.render()
                    self._pyg.time.wait(1000)
                    run = False
                    break
            self._fps_clock.tick(self._fps)
        self._pyg.quit()

# ============================================================================ #
# ================================ Game Logic ================================ #
# ============================================================================ #

    def start_game(self):
        cur_speed = self._start_speed
        prev_time = self._pyg.time.get_ticks()
        self._score = 0
        self._game_over = False
        self._level = 1
        self._gui.init_window()
        self._init_new_pytromino()

        while not self._game_over:
            for event in self._pyg.event.get():
                if event.type == QUIT:
                    self._game_over = True
                    break
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self._game_over = True
                        break
                    elif event.key == K_c:
                        self._hold_pytromino()
                    else:
                        self._handle_movements(event.key)

            self._fps_clock.tick(self._fps)
            # Automatic shift down 1
            cur_time = self._pyg.time.get_ticks()
            if cur_time - prev_time >= 1000/cur_speed:
                success = self._move_cur_pytromino(Pytromino.shift_down_fn(1))
                # Pytromino can't go down anymore
                if not success:
                    # Freeze position to board
                    self._conclude_cur_pytromino_turn()
                    # Check for row clearance(s)
                    self._check_row_clearance()
                    # Initialize life of the next pytromino
                    self._init_new_pytromino()
                prev_time = cur_time

# ============================================================================ #
# =========================== Additional Functions =========================== #
# ============================================================================ #

    def _init_new_pytromino(self):
        if self._game_over: return
        self._cur_pytromino = self._get_new_pytromino()
        self._cur_pytromino.place_at(self._pytro_start_coord)
        # Check if new piece can be placed, if not, game over
        on_board_blocks = self._cur_pytromino.filter_blocks_pos(
            self._board.valid_coordinate
        )
        for pos in on_board_blocks:
            if self._board[pos] != self._empty_cell_color:
                self._game_over = True
                return
        self._draw_cur_pytromino()

    def _conclude_cur_pytromino_turn(self):
        if self._game_over: return
        self._holder.open()
        # Freezing current pytromino in place
        blocks_pos = self._cur_pytromino.get_blocks_pos()
        color = self._cur_pytromino.get_color()
        for pos in blocks_pos:
            if self._board.valid_coordinate(pos):
                self._board[pos] = color
            else:
                self._game_over = True

    def _check_row_clearance(self):
        if self._game_over: return
        unique_rows = self._cur_pytromino.get_unique_rows()
        cleared_rows = []
        # Figure out rows to be cleared
        for row_index in unique_rows:
            row = self._board.get_row(row_index)
            empty_cells = [item for item in row if item == self._empty_cell_color]
            if len(empty_cells) == 0:
                cleared_rows.append(row_index)
        # Clear the rows
        for row_index in sorted(cleared_rows, reverse=True):
            self._board.delete_row(row_index)
        # Add new rows to top of the board
        for _ in range(len(cleared_rows)):
            self._board.insert_row_at(0, 
                [self._empty_cell_color for _ in range(self._num_cols)])
        if cleared_rows:
            # Each cleared row is worth 100 points for now
            self._increment_score_by(100 * len(cleared_rows))
            # Redraw all board squares
            for x in range(self._num_cols):
                for y in range(self._num_rows):
                    coord = (x, y)
                    self._gui.draw_rectangle_in_main(
                        coord, 
                        self._board[coord]
                    )
            # Render display
            self._gui.render()
        

    def _draw_cur_pytromino(self, color=None):
        assert self._cur_pytromino.is_placed(), \
            f'Current Pytromino not placed: {self._cur_pytromino}'
        if not color:
            color = self._cur_pytromino.get_color()

        valid_blocks = self._cur_pytromino.filter_blocks_pos(
            self._board.valid_coordinate
        )

        self._gui.draw_rectangles_in(
            PytrisViewManager.Grid.MID, 
            valid_blocks, 
            color
        )
        # For better UX, render rightaway
        self._gui.render()

    def _cur_pytromino_block_validator(self, pos):
        if pos[1] < 0:
            return 0 <= pos[0] < self._num_cols
        return self._board.valid_coordinate(pos) \
            and self._board[pos] == self._empty_cell_color
        
    def _move_cur_pytromino(self, fn, is_rotation=False):
        assert self._cur_pytromino.is_placed()
        src_pos = self._cur_pytromino.filter_blocks_pos(
            self._board.valid_coordinate
        )
        success = self._cur_pytromino.validated_apply(
            fn, 
            is_rotation,
            validator=self._cur_pytromino_block_validator,
        )
        if success:
            dest_pos = self._cur_pytromino.filter_blocks_pos(
                self._board.valid_coordinate
            )
            self._gui.move_rectangles_in(
                PytrisViewManager.Grid.MID, 
                src_pos, 
                dest_pos,
                self._cur_pytromino.get_color()
            )
            # For better UX, render movement rightaway
            self._gui.render()
        return success
        
    def _handle_movements(self, key):
        fn = None
        is_rotation = False
        if key == K_DOWN:
            fn = Pytromino.shift_down_fn(1)
        elif key == K_LEFT:
            fn = Pytromino.shift_left_fn(1)
        elif key == K_RIGHT:
            fn = Pytromino.shift_right_fn(1)
        elif key == K_UP:
            is_rotation = True
            fn = self._rotate_block_90_cw
        else:
            if key == K_f:
                print(self._fps_clock.get_fps())
            if key == K_b:
                print(self._board)
            return
        success = self._move_cur_pytromino(fn, is_rotation)
        if key == K_DOWN and success:
            self._increment_score_by(1)

    def _rotate_block_90_cw(self, pos):
        res = self._cur_pytromino.rotate_block_90_cw(pos)
        res = (int(res[0]), int(res[1]))
        return res

    def _increment_score_by(self, num):
        self._score += num
        self._gui.update_score(self._score)
        self._gui.render()

    def get_random_pytromino_t(self):
        return choice(self._pytromino_types)

    def _get_new_pytromino(self):
        pytromino_t = self._nextup.popleft()
        self._nextup.append(self.get_random_pytromino_t())

        x = 1
        y = 2
        self._gui.init_pytro_nextup()
        for i, t in enumerate(self._nextup):
            center = (x, 4 * i + y)
            display_pytro = pytromino_factory(t)
            display_pytro.place_at(center)
            for coord in display_pytro.get_blocks_pos():
                self._gui.draw_rectangle_in_nextup(coord, display_pytro.get_color())
        self._gui.render()
        return pytromino_factory(pytromino_t)

    def _hold_pytromino(self):
        can_hold = self._holder.is_open()
        if can_hold:
            next_pytromino_t = self._holder.get_item()
            if not next_pytromino_t: # holder is empty
                # Reflect the change on holder display
                self._gui.init_pytro_holder()
                display_pytro = pytromino_factory(self._cur_pytromino.get_type())
                display_pytro.place_at((1, 2))
                for coord in display_pytro.get_blocks_pos():
                    self._gui.draw_rectangle_in_holder(coord, display_pytro.get_color())
                self._gui.render()

                self._holder.store(self._cur_pytromino.get_type())
                self._draw_cur_pytromino(self._empty_cell_color)
                self._holder.close()
                self._init_new_pytromino()
            else: # switch cur_pytromino type with the one in holder
                # 1. Make sure the switched pytromino can be placed
                cur_pytromino_center = self._cur_pytromino.get_blocks_pos()[0]
                next_pytromino = pytromino_factory(next_pytromino_t)
                next_pytromino.place_at(cur_pytromino_center)
                for pos in next_pytromino.get_blocks_pos():
                    if not self._cur_pytromino_block_validator(pos):
                        return False
                # Reflect the change on holder display
                self._gui.init_pytro_holder()
                display_pytro = pytromino_factory(self._cur_pytromino.get_type())
                display_pytro.place_at((1, 2))
                for coord in display_pytro.get_blocks_pos():
                    self._gui.draw_rectangle_in_holder(coord, display_pytro.get_color())
                self._gui.render()
                # Store the type
                self._holder.store(self._cur_pytromino.get_type())
                # Coverup the current pytromino colors
                self._draw_cur_pytromino(self._empty_cell_color)
                # Make the switch
                self._cur_pytromino = next_pytromino
                # Draw the replacement pytrominos
                self._draw_cur_pytromino()
                self._gui.render()
                # Close holder
                self._holder.close()
        return can_hold
