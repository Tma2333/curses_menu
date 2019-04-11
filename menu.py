import curses

class Menu:
    def __init__ (self, size_y, size_x, start_y, start_x, box = False, item_num = 3, warp = False):
        self._y = size_x
        self._x = size_x
        self._ys = start_y
        self._xs = start_x 
        self._box = box
        self._n = item_num

        self._position = 0
        self.Items = []
        for i in range(item_num):
            self.Items.append({'item_name':'{}'.format(i), 'function':self._empty, 'start_y':i+1, 'start_x':1, 'break':False})

        self._flag_warp = warp
        self._flag_exit = False
        self._flag_exec = False

    def _nevgation (self, key):
        if key == curses.KEY_UP:
            if self._position == 0 and self._flag_warp:
                self._position = self._n-1
            elif self._position == 0:
                self._position = 0
            else:
                self._position -= 1
        elif key == curses.KEY_DOWN:
            if self._position == self._n-1 and self._flag_warp:
                self._position = 0
            elif self._position == self._n-1:
                self._position == self._n-1
            else:
                self._position += 1
        elif key == ord('q'):
            self._flag_exit = True
        elif key in [ord('\n'), curses.KEY_ENTER]:
            self._flag_exec = True
    
    def _loop (self, stdscr):
        self._menu = curses.newwin(self._y, self._x, self._ys, self._xs)
        if self._box:
            self._menu.box()

        curses.curs_set(False)
        self._menu.refresh()
        self._menu.keypad(True)
        key = 0

        while True:
            if self._flag_exit:
                break
            if self._flag_exec:
                self.Items[self._position]['function']()
                self._flag_exec = False
                if self.Items[self._position]['break']:
                    break
                        
            for index, item in enumerate(self.Items):
                if index == self._position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                self._menu.addstr(item['start_y'], item['start_x'], item['item_name'], mode)

            key = self._menu.getch()
            self._nevgation(key)

    def _empty (self):
        pass
        
    def add_item (self, num, item_name, function, start_y = None, start_x = None, breaking = False):
        start_y, start_x = num+1, 1
        self.Items[num]['item_name'] = item_name
        self.Items[num]['function'] = function
        self.Items[num]['start_y'] = start_y
        self.Items[num]['start_x'] = start_x
        self.Items[num]['break'] = breaking

    def display (self):
        curses.wrapper(self._loop)

    def status (self):
        pass

    


        

        