import curses


# Constant


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
        self._default_verify = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                                'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                                'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                                'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                                'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', ' ', '\n','!', '@', '#', '$', '%', '^',
                                '&', '*', '(', ')', '-', '+', '/', '<', '>', '.',
                                '?', '{', '}', '[', ']', ':', ';', '\"', '\'', '~',
                                '`')

        # Variable: Data 
        self._position = 0
        self.Items = []
        for i in range(item_num):
            self.Items.append({'item_name':'{}'.format(i), 'mode':'simple', 'function':self._empty, 'start_y':i+1, 'start_x':1, 'break':False})
        self._return_path = None
        self._text = {}

        # Variable: Flag/counter
        self._flag_warp = warp          # flag to indicate if up and down arrow wrap around
        self._flag_exit = False         # flag to indicate if menu is in exit state
        self._flag_exec = False         # flag to indicate if a function is needed to be 
        self._flag_link = False         # flag to indicate if the menu is a linked by a parent menu
        self._count_text = 0            # counter to track user added text

    def _edit (self):
        key = 0
        entry = ''
        curses.curs_set(1)
        n = 0

        self._menu.addstr(self.Items[self._position]['edit_y'], self.Items[self._position]['edit_x'], ' '*len(self.Items[self._position]['edit_target'][0]))
        self._menu.move(self.Items[self._position]['edit_y'], self.Items[self._position]['edit_x'])

        while True:
            key = self._menu.getkey()

            if key in ['KEY_BACKSPACE', '\b', '\x7f'] and n > 0:
                n -= 1
                self._menu.addstr(self.Items[self._position]['edit_y'], self.Items[self._position]['edit_x']+n, ' ')
                self._menu.move(self.Items[self._position]['edit_y'], self.Items[self._position]['edit_x']+n)
                entry = entry[0:-1]

            if key == '\n':
                break

            if self._edit_verify (key):
                self._menu.addstr(self.Items[self._position]['edit_y'], self.Items[self._position]['edit_x']+n, key)
                n += 1
                self._menu.move(self.Items[self._position]['edit_y'], self.Items[self._position]['edit_x']+n)

                entry += key

        curses.curs_set(0)
        self.Items[self._position]['edit_target'][0] = entry

    
    def _edit_verify (self, ch):
        if ch in self._default_verify:
            return True
        else:
            return False


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

        # add text
        if self._count_text:
            for i in range(self._count_text):
                self._menu.addstr(self._text[i][0], self._text[i][1], self._text[i][2], self._text[i][3][0])

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

                if item['mode'] == 'edit':
                    self._menu.addstr(item['edit_y'], item['edit_x'], ' '*len(item['edit_target'][0]))
                    self._menu.addstr(item['edit_y'], item['edit_x'], item['edit_target'][0])
            # key entry and check
            key = self._menu.getch()
            self._nevgation(key)
        stdscr.erase()


    def _error_headling (self, error_code):
        if error_code == 101:
            raise ModeError('ERROR 101: Mode does not exist. Available mode: {}'.format(self._mode_list))
        elif error_code == 102:
            raise ModeError('ERROR 102: menu_obj (required by link mode) missing or incorrect')
        elif error_code == 103:
            raise ModeError('ERROR 103: edit_target (required by edit mode) missing')
        elif error_code == 104:
            raise ModeError('ERROR 104: edit_target must be a list that containt only one string')


    def _empty (self):
        pass
        
    def add_item (self, num, item_name, mode = 'simple', function = None, start_y = None, start_x = None, breaking = False, 
                                        menu_obj = None, edit_target = None, edit_verify = None, edit_y = None, edit_x = None):
        if mode not in self._mode_list:
            self._error_headling(101)

        # default config:
        if function == None:
            function = self._empty
        if start_y == None:
            start_y = num+1
        if start_x == None:
            start_x = 1
        if edit_verify == None:
            edit_verify = self._edit_verify
        if edit_y == None:
            edit_y = start_y
        if edit_x == None:
            edit_x = start_x + len(item_name) + 1

        # assign items
        self.Items[num]['item_name'] = item_name

        # simple mode: execute user function
        if mode == 'simple':
            self.Items[num]['mode'] = 'simple'
            self.Items[num]['function'] = function
            self.Items[num]['start_y'] = start_y
            self.Items[num]['start_x'] = start_x
            self.Items[num]['break'] = breaking

        # link mode: link to a sub menu
        elif mode == 'link':
            if not type(menu_obj) == Menu:
                self._error_headling(102)
            self.Items[num]['mode'] = 'link'
            self.Items[num]['start_y'] = start_y
            self.Items[num]['start_x'] = start_x
            self.Items[num]['break'] = True
            # assign the function to the object display
            self.Items[num]['function'] = menu_obj.display
            menu_obj._flag_link = True
            menu_obj._return_path = self.display
        
        # edit mode: edit a variable
        elif mode == 'edit':
            if edit_target == None:
                self._error_headling(103)

            if not type(edit_target) == type([]) or not len(edit_target) == 1 or not type(edit_target[0]) == type(''):
                self._error_headling(104)

            self.Items[num]['mode'] = 'edit'
            self.Items[num]['start_y'] = start_y
            self.Items[num]['start_x'] = start_x
            self.Items[num]['break'] = False
            self.Items[num]['function'] = self._edit
            self.Items[num]['edit_target'] = edit_target
            self.Items[num]['edit_verify'] = edit_verify
            self.Items[num]['edit_y'] = edit_y
            self.Items[num]['edit_x'] = edit_x

        # exit mode: exit the current menu
        elif mode == 'exit':
            self.Items[num]['mode'] = 'exit'
            self.Items[num]['start_y'] = start_y
            self.Items[num]['start_x'] = start_x
            self.Items[num]['break'] = True
            self.Items[num]['function'] = self._empty


    def set_color (self, ):
        pass

    
    def add_text (self, start_y, start_x, text, *attr):
        self._text[self._count_text] = [start_y, start_x, text, attr]
        self._count_text += 1


    def display (self):
        # wrapper for safe curses operation 
        curses.wrapper(self._loop)

        if self.Items[self._position]['break'] and self._flag_exec:
            self._flag_exec = False
            self.Items[self._position]['function']()
            
        if not self._return_path == None:
            self._flag_exit = False
            self._return_path()


class Error (Exception):
    pass


class ModeError (Error):
    def __init__ (self, message):
        self.message = message


        