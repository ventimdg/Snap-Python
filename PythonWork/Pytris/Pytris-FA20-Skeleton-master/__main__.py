def main():
    import sys
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        print("Program requires python 3.6+")
        exit(1)
    try:
        import pygame
    except Exception:
        print("Failed to import pygame")
        exit(1)

    try:
        from view import PytrisViewManager
        from board import Board
        from game_ctl import PytrisController
        from colors import Color
    except Exception:
        print("Missing one of view.py board.py models.py or game_ctl.py")
        exit(1)

    pygame.init()

    GUI = PytrisViewManager(pygame)
    BOARD = Board(cell_item=(0, 0, 0))
    
    Pytris = PytrisController(BOARD, GUI)
    Pytris.show_main_menu()

if __name__ == "__main__":
    main()
