#! /usr/bin/python3

import menu
import sys

def example_one ():
    main_menu = menu.Menu(30, 50, 0, 0, box=True, item_num=5, warp=True)
    sub_menu = menu.Menu(30, 50, 0, 0, box=False, item_num=3, warp=False)

    main_menu.add_item(0, )
