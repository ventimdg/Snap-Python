from enum import Enum, unique

@unique
class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    CYAN = (43, 172, 226)
    YELLOW = (253, 225, 2)
    ORANGE = (247, 150, 34)
    GREEN = (77, 184, 72)
    PURPLE = (146, 44, 140)
    BLUE = (0, 90, 156)
    RED = (238, 40, 51)
