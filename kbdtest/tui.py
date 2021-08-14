import curses
import numpy as np
from os import popen
from kbdtest.interface import KeyboardInterface


def curses_init():
    """
    Function for initializing the ncurses backend for
    drawing characters to the screen.

    Returns:
    -------
    screen: curses.window object
        Window representing the current terminal window
    rows: int
        Number of rows in the screen
    cols: int
        Number of columns in the screen
    """
    rows, cols = popen('stty size','r').read().split()
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1,0,7)
    curses.init_pair(2,7,0)
    curses.init_pair(3,-1,15)
    curses.init_pair(4,-1,4)
    curses.init_pair(5,0,2) # percentages
    screen.keypad(1)
    screen.nodelay(True)
    screen.idcok(False)
    screen.idlok(False)
    return screen, int(rows), int(cols)

def term_resize():
    """
    Function for reinitializing the terminal window and
    the graphic keyboard when a terminal resize is detected.

    Returns:
    -------
    screen: curses.window object
        The new window representing the resized terminal window
    rows: int
        The number of rows of the resized window
    cols: int
        The number of columns of the resized window
    ch: int
        The new character for getch() calls in the runtime loop
    kbdisp: KeyboardDisplay object
        A graphical keyboard for the new window
    """
    screen, rows, cols = curses_init()
    kbdisp = KeyboardDisplay(rows, cols)
    ch = None
    kbdisp.interface.start()
    return screen, rows, cols, ch, kbdisp

class KeyboardDisplay():

    def __init__(self, sizey, sizex):
        """
        Constructor for the graphic keyboard display.

        Parameters:
        ----------
        sizey: int
            Number of rows of the current executing terminal window
        sizex int
            Number of columns of the current executing terminal window
        """

        if sizey < 20 or sizex < 70:
            raise RuntimeError("Terminal is too small to draw the graphic keyboard.")
            curses.endwin()
            exit()

        self.draw_layout = np.array(
                      [["ESC", "F1 ", "F2 ", "F3 ", "F4 ", "F5 ", "F6 ", "F7 ", "F8 ", "F9 ", "F10", "F11", "F12", "   ", "PRT", "SCL", "PS "],
                       [" ` ", " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 ", " 0 ", " - ", " + ", " \ ", "INS", "HOM", "PGU"],
                       ["TAB", " Q ", " W ", " E ", " R ", " T ", " Y ", " U ", " I ", " O ", " P ", " [ ", " ] ", "BS ", "DEL", "END", "PGD"],
                       ["CAP", " A ", " S ", " D ", " F ", " G ", " H ", " J ", " K ", " L ", " ; ", " ' ", "ENT", "   ", "   ", "NML", "   "],
                       ["SFT", " Z ", " X ", " C ", " V ", " B ", " N ", " M ", " , ", " . ", " / ", "   ", "SFT", "   ", "   ", "UP ", "   "],
                       ["FN" , "CTR", "ALT", "CMD", "   ", "   ", "SPC", "   ", "   ", "CMD", "ALT", "   ", "   ", "   ", "LFT", "DN ", "RGT"]]
                      )
        self.interface = KeyboardInterface()
        ky = 6
        kx = 17
        bky = 7
        bkx = 18
        self.spacey = 2
        self.spacex = 4
        self.window = curses.newwin(ky*self.spacey, kx*self.spacex, int((sizey - ky*self.spacey)/2), int((sizex - kx*self.spacex)/2))
        self.window_border = curses.newwin(bky*self.spacey, bkx*self.spacex, int((sizey - bky*self.spacey)/2), int((sizex - bkx*self.spacex)/2))
        self.window.bkgd(curses.color_pair(1))
        self.window_border.bkgd(curses.color_pair(3))
        self.keywindow = curses.newwin(1, (kx*self.spacex), int((sizey - ky*self.spacey)/2)-3, int((sizex - kx*self.spacex)/2)-1)


    def right_pad_string(self, string):
        """
        Method for right padding strings. This avoids having to clear or
        redraw the entire last key indicator window.

        Parameters:
        ---------- string: string
            String denoting the last key pressed.

        Returns:
        -------
            The original string padded on the right by 12 space characters
        """
        return string + "            "

    def keywindow_update(self):
        """
        Method for drawing the last key indicator
        """
        if self.interface.last_key_pressed != None:
            self.keywindow.addstr(0, 1, "Last key pressed: ")
            self.keywindow.addstr(0, 20 , self.right_pad_string(self.interface.last_key_pressed))
            self.keywindow.refresh()

    def draw(self, screen):
        """
        Method for drawing the graphic keyboard and the last key indicator.

        Parameters:
        ----------
        screen: curses.window object
            The window in which the keyboard graphic should be drawn in
        """
        for i, row in enumerate(self.draw_layout):
            for j, string in enumerate(row):
                if set(self.interface.read_layout[:,i,j]).intersection(self.interface.keys_pressed):
                    self.window.attron(curses.color_pair(5))
                    self.window.addstr(self.spacey*i, self.spacex*j, string)

                if self.interface.state[i][j]:
                    self.window.attron(curses.A_REVERSE)
                    self.window.addstr(self.spacey*i, self.spacex*j, string)
                else:
                    self.window.attroff(curses.A_REVERSE)
                    self.window.addstr(self.spacey*i, self.spacex*j, string)
                self.window.attron(curses.color_pair(1))

        self.keywindow_update()
        self.window_border.refresh()
        self.window.refresh()
        screen.refresh()
