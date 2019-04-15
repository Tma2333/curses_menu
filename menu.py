import curses

class Menu:
    def __init__ (self, size_y, size_x, start_y, start_x, box = False, item_num = 3, warp = False):
        # Variable: Parameter
        self._y = size_x
        self._x = size_x
        self._ys = start_y
        self._xs = start_x 
        self._box = box
        self._n = item_num
        self._mode_list = ('simple', 'link', 'edit', 'exit')

        # Variable: Data 
        self._position = 0
        self.Items = []
        for i in range(item_num):
            self.Items.append({'item_name':'{}'.format(i), 'mode':'simple', 'function':self._empty, 'start_y':i+1, 'start_x':1, 'break':False})
        self._return_path = None

        # Variable: Flag
        self._flag_warp = warp          # flag to indicate if up and down arrow wrap around
        self._flag_exit = False         # flag to indicate if menu is in exit state
        self._flag_exec = False         # flag to indicate if a function is needed to be 
        self._flag_link = False         # flag to indicate if the menu is a linked by a parent menu

    def _nevgation (self, key):
        # nevigation check:key up check
        if key == curses.KEY_UP:
            if self._position == 0 and self._flag_warp:
                self._position = self._n-1
            elif self._position == 0:
                self._position = 0
            else:
                self._position -= 1
        # nevigation check:key down check
        elif key == curses.KEY_DOWN:
            if self._position == self._n-1 and self._flag_warp:
                self._position = 0
            elif self._position == self._n-1:
                self._position == self._n-1
            else:
                self._position += 1
        # action check: exit check
        elif key == ord('q'):
            self._flag_exit = True
        # action check: enter check
        elif key in [ord('\n'), curses.KEY_ENTER]:
            self._flag_exec = True
    
    def _loop (self, stdscr):
        # create new window object
        self._menu = curses.newwin(self._y, self._x, self._ys, self._xs)
        if self._box:
            self._menu.box()

        # parameter setting for menu
        curses.curs_set(False)
        self._menu.refresh()
        self._menu.keypad(True)
        key = 0

        # display loop
        while True:
            # state check 
            if self._flag_exit:
                break
            if self._flag_exec:
                if self.Items[self._position]['break']:
                    break
                else:
                    self._flag_exec = False
                    self.Items[self._position]['function']()

            # item rendering loop
            for index, item in enumerate(self.Items):
                if index == self._position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                self._menu.addstr(item['start_y'], item['start_x'], item['item_name'], mode)

            # key entry and check
            key = self._menu.getch()
            self._nevgation(key)


    def _error_headling (self, error_code):
        if error_code == 101:
            raise ModeError('ERROR 101: Mode does not exist. Available mode: {}'.format(self._mode_list))
        elif error_code == 102:
            raise ModeError('ERROR 102: menu_obj (required by link mode) missing or incorrect')


    def _empty (self):
        pass
        
    def add_item (self, num, item_name, mode = 'simple', function = None, start_y = None, start_x = None, breaking = False, menu_obj = None):
        if mode not in self._mode_list:
            self._error_headling(101)

        # default config:
        if function == None:
            function = self._empty
        if start_y == None:
            start_y = num+1
        if start_x == None:
            start_x = 1

        # assign items
        self.Items[num]['item_name'] = item_name

        if mode == 'simple':
            self.Items[num]['function'] = function
            self.Items[num]['start_y'] = start_y
            self.Items[num]['start_x'] = start_x
            self.Items[num]['break'] = breaking

        elif mode == 'link':
            if not type(menu_obj) == Menu:
                self._error_headling(102)
            self.Items[num]['start_y'] = start_y
            self.Items[num]['start_x'] = start_x
            self.Items[num]['break'] = True
            # assign the function to the object display
            self.Items[num]['function'] = menu_obj.display
            menu_obj._flag_link = True
            menu_obj._return_path = self.display


    def display (self):
        # wrapper for safe curses operation 
        curses.wrapper(self._loop)

        if self.Items[self._position]['break'] and self._flag_exec:
            self._flag_exec = False
            self.Items[self._position]['function']()
            
        if not self._return_path == None:
            self._flag_exit = False
            self._return_path()

    def status (self):
        pass


class Error (Exception):
    pass


class ModeError (Error):
    def __init__ (self, message):
        self.message = message


        