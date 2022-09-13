from itertools import product
from enum import Enum, auto
from pathlib import Path

class PytrisViewManager:

    class Grid(Enum):
        LEFT = auto()
        MID = auto()
        RIGHT = auto()

    def __init__(self, pyg, num_cols=10, num_rows=20, window_size=(800, 640),
        bg_color=(0, 0, 25), rect_size=(25, 25), rect_color=(0, 0, 0),
        margin=1, margin_color=(172, 172, 172), num_nextup=4):
        """ The Graphical User Interface for Pytris

        Parameters
        ----------
        pyg : pygame
            An initialized pygame object

        num_cols : int
            Number of columns to display. Default 10

        num_rows : int
            Number of rows to display. Default 20

        window_size : (int, int)
            A tuple/list of WIDTH, HEIGHT of the display window in pixels.
            Default (800, 640) a 3:2 aspect ratio

        bg_color : (int, int, int)
            RGB values to define the color of the entire window. 
            Default (0, 0, 0)

        rect_size : (int, int)
            A tuple/list of WIDTH, HEIGHT of rectangles. Default (30, 30)

        rect_color : (int, int, int)
            RGB values to define the color of each rectangle.
            Default (255, 255, 255)

        margin : int
            Space between each neighboring rectangle. Default 1

        margin_color : (int, int, int)
            RGB values to define the color of margin lines between rectangles.
            Default (172, 172, 172)
        
        num_nextup : int
            Number of nextup pytrominos to display on the right. Default 4
        """
        # Arguments
        self._pyg = pyg
        self._num_cols = num_cols
        self._num_rows = num_rows
        self._window_vect = pyg.Vector2(window_size)
        self._bg_color = bg_color
        self._rect_vect = pyg.Vector2(rect_size)
        self._rect_color = rect_color
        self._margin_vect = pyg.Vector2(margin)
        self._margin_color = margin_color
        self._num_nextup = num_nextup # display 4 next-up pytrominos
        # Additional
        self._pyg.display.set_caption('Pytris')
        self._surface = pyg.display.set_mode(window_size)
        self.default_text_color = (255, 255, 255)
        # Main stage in the middle
        self._main_grid_topleft = self._window_vect // 2 - self._calc_grid_vect(
                                                    num_cols, num_rows) // 2
        # The holder on the left
        self._left_blade = 1/6
        self._pytro_grid_len = 4
        self._pytro_grid_vect = self._calc_grid_vect(
            self._pytro_grid_len, self._pytro_grid_len
        )
        self._holder_center = self._pyg.Vector2(
            int(self._window_vect.x * self._left_blade), 
            int(self._window_vect.y * 1 / 6) + 40
        )
        self._holder_topleft = self._holder_center - self._pytro_grid_vect // 2
        # The nextup on the right
        self._right_blade = 5/6
        self._nextup_grid_vect = self._calc_grid_vect(
            self._pytro_grid_len, self._pytro_grid_len * self._num_nextup
        )
        self._nextup_center = self._pyg.Vector2(
            int(self._window_vect.x * self._right_blade),
            int(self._window_vect.y * 1 / 2)
        )
        self._nextup_topleft = self._nextup_center - self._nextup_grid_vect // 2
        # Fonts
        new_tetris_font = Path(__file__).parent.joinpath('assets/fonts/newTetris.ttf')
        tetris_font = Path(__file__).parent.joinpath('assets/fonts/Tetris.ttf')
        try:
            self._main_font = self._pyg.font.Font(str(new_tetris_font), 50)
            self._game_font = self._pyg.font.Font(str(tetris_font), 30)
        except Exception as err:
            print(f"Failed to load custom fonts, using system defaults. {err}")
            self._main_font = self._pyg.font.SysFont('ariel', 50)
            self._game_font = self._pyg.font.SysFont('ariel', 30)
        self._number_font = self._pyg.font.SysFont('ariel', 50)
        # Aggregate all updates
        self._updated_rects = []

# --------------------------------- Open APIs -------------------------------- #

    def init_window(self):
        """ Initializes and draws the surface of the overall window.
            This also represents the lowest level of surface, and other
            surface(s) can be blit() on top of it.
        """
        # Fill window with background color
        self.fill_background()
        # Display game grid
        self.init_main_stage()
        # Display score board
        self.update_score(0)
        # Display hold grid
        self.init_pytro_holder()
        # Display nextup grid
        self.init_pytro_nextup()
    
    def fill_background(self):
        self._updated_rects.append(
            self._surface.fill(self._bg_color)
        )

    def init_main_stage(self, text_color=None):
        if not text_color:
            text_color = self.default_text_color
        self.draw_grid_for(
            self.Grid.MID, 
            self._num_cols, 
            self._num_rows,
            display_margin=True,
            text='MAIN STAGE',
            text_color=text_color
        )

    def init_pytro_holder(self, text_color=None):
        if not text_color:
            text_color = self.default_text_color
        self.draw_grid_for(
            self.Grid.LEFT, 
            self._pytro_grid_len, 
            self._pytro_grid_len,
            text='HOLD',
            text_color=text_color
        )
        
    def init_pytro_nextup(self, text_color=None):
        if not text_color:
            text_color = self.default_text_color
        self.draw_grid_for(
            self.Grid.RIGHT, 
            self._pytro_grid_len, 
            self._pytro_grid_len * self._num_nextup,
            text='NEXT',
            text_color=text_color
        )

    def update_score(self, score, text_color=(255, 255, 255)):
        score_text_center = self._pyg.Vector2(
            int(self._window_vect.x * self._left_blade),
            int(self._window_vect.y * 4 / 6)
        )
        score_text_surface = self._game_font.render('SCORE', False, text_color)
        score_text_size = self._pyg.Vector2(score_text_surface.get_size())
        score_center = self._pyg.Vector2(score_text_center.x, score_text_center.y + 30)
        score_surface = self._number_font.render(str(score), True, text_color)
        score_size = self._pyg.Vector2(score_surface.get_size())
        score_topleft = score_center - score_size // 2

        # Overwrite the score area with background color first
        rects = [self._pyg.draw.rect(self._surface, self._bg_color, 
                    score_surface.get_rect(topleft=score_topleft))]
        rects.extend(self._surface.blits([
            (score_text_surface, score_text_center - score_text_size // 2),
            (score_surface, score_topleft)
        ]))
        self._updated_rects.extend(rects)

    def render(self):
        """ Actually update the display for everything that's been
            drawn to screen since the last update. Will do nothing
            if no update has occurred
        """
        if self._updated_rects:
            self._pyg.display.update(self._updated_rects)
            self._updated_rects = []

    def draw_grid_for(self, grid, num_cols, num_rows, display_margin=True, 
                            text=None, text_color=None):
        self.draw_rectangles_in(
            grid,
            product(range(num_cols), range(num_rows)),  
            self._rect_color
        )

        if display_margin:
            self.draw_margin_for(grid, num_cols, num_rows, self._margin_color)
        
        if text:
            if not text_color:
                text_color = self.default_text_color
            center_vect, topleft_vect = self._select_grid_center_topleft(grid)

            text_center = self._pyg.Vector2(
                center_vect.x,
                topleft_vect.y - 20
            )
            text_surface = self._game_font.render(text, False, text_color)
            text_size = self._pyg.Vector2(text_surface.get_size())
            rect = self._surface.blit(
                text_surface, text_center - text_size // 2
            )
            self._updated_rects.append(rect)

    def draw_rectangles_in(self, grid, coordinate_iter, color):
        _, topleft_vect = self._select_grid_center_topleft(grid)
        for coord in coordinate_iter:
            self._draw_rect_at(coord, topleft_vect, color)

    def move_rectangles_in(self, grid, src_iter, dest_iter, color):
        self.draw_rectangles_in(grid, src_iter, self._rect_color)
        self.draw_rectangles_in(grid, dest_iter, color)

    def draw_margin_for(self, grid, num_cols, num_rows, color):
        grid_vect = self._calc_grid_vect(num_cols, num_rows)
        _, topleft_vect = self._select_grid_center_topleft(grid)
        # Draw margin lines
        margin_offset = self._margin_vect // 2
        # Horizontal margin lines
        for y in range(num_rows + 1):
            y_val = topleft_vect.y + y * (self._rect_vect.y + 
                        self._margin_vect.y) + margin_offset.y
            rect = self._pyg.draw.line(
                self._surface,
                color,
                (topleft_vect.x, y_val),
                (topleft_vect.x + grid_vect.x - 1, y_val),
                int(self._margin_vect.y)
            )
            self._updated_rects.append(rect)
        # Vertical margin lines
        for x in range(num_cols + 1):
            x_val = topleft_vect.x + x * (self._rect_vect.x + 
                        self._margin_vect.x) + margin_offset.x
            rect = self._pyg.draw.line(
                self._surface,
                color,
                (x_val, topleft_vect.y),
                (x_val, topleft_vect.y + grid_vect.y - 1),
                int(self._margin_vect.x)
            )
            self._updated_rects.append(rect)

    def draw_text_center(self, msg, color=(255, 255, 255)):
        """ Display centered message OVER window
        """
        text_surface = self._main_font.render(msg, True, color)
        text_size = self._pyg.Vector2(text_surface.get_size())
        rect = self._surface.blit(text_surface, self._window_vect // 2 - text_size // 2)
        self._updated_rects.append(rect)

    def draw_rectangle_in_main(self, coordinate, color):
        self._draw_rect_at(coordinate, self._main_grid_topleft, color)

    def draw_rectangle_in_holder(self, coordinate, color):
        self._draw_rect_at(coordinate, self._holder_topleft, color)

    def draw_rectangle_in_nextup(self, coordinate, color):
        self._draw_rect_at(coordinate, self._nextup_topleft, color)

    def get_pygame(self):
        return self._pyg

    def get_num_nextup(self):
        return self._num_nextup

    def get_rect_color(self):
        return self._rect_color

    def updated(self):
        return len(self._updated_rects) > 0

# ----------------------------- Helper Functions ----------------------------- #

    def _calc_grid_vect(self, num_cols, num_rows):
        grid_dim = self._pyg.Vector2(num_cols, num_rows)
        return grid_dim.elementwise() * \
            (self._rect_vect + self._margin_vect) + self._margin_vect

    def _select_grid_center_topleft(self, grid):
        if grid is self.Grid.MID:
            return self._window_vect // 2, self._main_grid_topleft
        elif grid is self.Grid.LEFT:
            return self._holder_center, self._holder_topleft
        elif grid is self.Grid.RIGHT:
            return self._nextup_center, self._nextup_topleft
        else:
            raise ValueError('Unknown grid')

    def _draw_rect_at(self, coordinate, topleft_vect, color):
        coord = self._pyg.Vector2(coordinate)
        rectangle = self._pyg.Rect(
            topleft_vect + (self._margin_vect + self._rect_vect)
                            .elementwise() * coord + self._margin_vect,
            self._rect_vect
        )
        self._updated_rects.append(
            self._pyg.draw.rect(self._surface, color, rectangle)
        )
