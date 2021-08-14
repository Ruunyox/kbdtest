from kbdtest.tui import *
from kbdtest.interface import *


def main():
    screen, rows, cols = curses_init()
    kbdisp = KeyboardDisplay(rows, cols)
    ch = None
    kbdisp.interface.start()
    while(ch != ord('Q')):
        ch = screen.getch()
        kbdisp.draw(screen)
        if curses.is_term_resized(rows, cols):
           screen.clear()
           screen.refresh()
           kbdisp.interface.stop()
           keys_pressed = kbdisp.interface.keys_pressed
           screen, rows, cols, ch, kbdisp = term_resize()
           kbdisp.interface.keys_pressed = keys_pressed
    kbdisp.interface.stop()
    curses.endwin()

if __name__ == '__main__':
    main()
