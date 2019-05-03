#! /usr/bin/python3

import menu
import sys


class printing:
    def __init__ (self, string):
        self.a_string = string
    
    def printing (self):
        print(self.a_string[0])

def goodbye ():
    print ('Good Bye!')

def example_one ():
    # create a 50x30 main menu with box around and 5 items
    main_menu = menu.Menu(20, 50, 0, 0, box=True, item_num=5, warp=True)
    # create a 50x30 sub menu with no box and 3 items
    sub_menu = menu.Menu(20, 50, 0, 0, box=False, item_num=3, warp=False)

    # when selected, the menu exit and print Good Bye
    main_menu.add_item(0, 'Print Good Bye!', 'simple', function=goodbye, breaking=True)

    # when selected, enter sub menu
    main_menu.add_item(1, 'Sub menu', 'link', menu_obj=sub_menu)

    # when selected, edit the string
    a_string = ['Hello!']
    main_menu.add_item(2, 'String: ', 'edit', edit_target=a_string)

    # when selected, print the string (Due to currently does not allow function with argument, use a class as work around)
    out = printing(a_string)
    main_menu.add_item(3, 'Print above', 'simple', function=out.printing, breaking=True)

    # when selected, exit the main menu
    main_menu.add_item(4, 'Exit', 'exit')

    # place holder 
    sub_menu.add_item(0, 'Welcome to', 'simple', start_y=10, start_x=12)
    sub_menu.add_item(1, 'Nothing', 'simple', start_y=12, start_x=10)
    sub_menu.add_item(2, 'Return', 'exit', start_y=14, start_x=14)

    main_menu.display()

if __name__ == "__main__":
    example_one()
