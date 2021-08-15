import numpy as np
from pynput import keyboard

class KeyboardInterface():

    def __init__(self):
        """
        Constructor for the interface to the keyboard. This class and its methods
        use pynput as a listening backend to capture keyboard input.
        """
        ky = 6
        kx = 17
        self.listener = keyboard.Listener(on_press=self.key_press,
                                          on_release=self.key_release)
        self.last_key_pressed = None
        self.state = np.zeros((ky,kx), dtype=bool)
        self.keys_pressed = set([])
        read_layout_1 = np.array(
                      [["esc","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","","print_screen","scroll_lock","pause"],
                       ["`","1","2","3","4","5","6","7","8","9","0","-","=","\\","insert","home","page_up"],
                       ["tab","q","w","e","r","t","y","u","i","o","p","[","]","backspace","del","end","page_down"],
                       ["caps_lock","a","s","d","f","g","h","j","k","l",";","'","enter","","","num_lock",""],
                       ["shift","z","x","c","v","b","n","m",",",".","/","","shift","","","up",""],
                       ["","ctrl","alt","cmd","","","space","","","cmd","alt_r","","","","left","down","right"]]
                      )
        read_layout_2 = np.array(
                      [["esc","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","","print_screen","scroll_lock","pause"],
                       ["~","!","@","#","$","%","^","&","*","(",")","_","+","|","insert","home","page_up"],
                       ["tab","Q","W","E","R","T","Y","U","I","O","O","{","}","backspace","del","end","page_down"],
                       ["caps_lock","A","S","D","F","G","H","J","K","L",":","\"","enter","","","num_lock",""],
                       ["shift","Z","X","C","V","B","N","M","<",">","?","","shift","","","up",""],
                       ["","ctrl","alt","cmd","","","space","","","cmd","alt_r","","","","left","down","right"]]
                      )
        self.read_layout = np.stack([read_layout_1, read_layout_2])

        self.state_map = {}
        self.generate_state_map()

    def generate_state_map(self):
        """
        Method to populate the state map for the keyboard. This maps the captured string input
        from the listener to a tuple of indices for the corresponding visual string in in the
        graphic keyboard layout matrix.
        """
        for layer in self.read_layout:
            for i, row in enumerate(layer):
                for j, col in enumerate(layer[i]):
                    key = layer[i][j]
                    self.state_map[key] = (i, j)

    def state_on(self, char):
        """
        Method that toggles a state on in the keyboard state matrix.
        """
        idx1, idx2 = self.state_map[char]
        self.state[idx1][idx2] = True

    def state_off(self, char):
        """
        Method that toggles a state off in the keyboard state matrix
        """
        idx1, idx2 = self.state_map[char]
        self.state[idx1][idx2] = False

    def key_press(self, key):
        """
        Method for handling key press events. This method simply
        updates the state matrix, the last key pressed, and the
        set of pressed keys.

        Parameters:
        ----------
        key: pynput keyboard.key object
            The key currently being pressed down
        """
        if hasattr(key, 'char'):
           if key.char in self.state_map.keys():
               self.state_on(key.char)
               self.keys_pressed.add(key.char)
               self.last_key_pressed = key.char
        else:
           if key.name in self.state_map.keys():
               self.state_on(key.name)
               self.keys_pressed.add(key.name)
               self.last_key_pressed = key.name

    def key_release(self, key):
        """
        Method for handling key release events. This method simply
        updates the state matrix.

        Parameters:
        ----------
        key: pynput keyboard.key object
            The key currently being released
        """
        if hasattr(key, 'char'):
           if key.char in self.state_map.keys():
               self.state_off(key.char)
        else:
           if key.name in self.state_map.keys():
               self.state_off(key.name)

    def start(self):
        """
        Wrapper method for starting the pynput keyboard listener
        """
        self.listener.start()

    def stop(self):
        """
        Wrapper method for starting the pynput keyboard listener
        """
        self.listener.stop()
